from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_, delete
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.crawler import CrawledArticle
from app.schemas.crawler import (
    ArticleListResponse,
    ArticleResponse,
    CrawlTriggerResponse,
)
from app.services.crawler_service import run_crawler, SOURCES
from app.utils.dependencies import get_current_user, CurrentUser, require_admin

router = APIRouter()


@router.get("/articles", response_model=ArticleListResponse)
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    source: str | None = Query(None, description="按信源筛选"),
    keyword: str | None = Query(None, description="关键词搜索"),
    start_date: str | None = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: str | None = Query(None, description="结束日期 YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    query = select(CrawledArticle).where(CrawledArticle.status == "active")

    if source:
        source_name = SOURCES.get(source, {}).get("name", source)
        query = query.where(CrawledArticle.source == source_name)

    if keyword:
        kw = f"%{keyword}%"
        query = query.where(
            or_(
                CrawledArticle.title.ilike(kw),
                CrawledArticle.summary.ilike(kw),
                CrawledArticle.content.ilike(kw),
            )
        )

    if start_date:
        try:
            dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.where(CrawledArticle.publish_date >= dt)
        except ValueError:
            pass

    if end_date:
        try:
            dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.where(CrawledArticle.publish_date <= dt)
        except ValueError:
            pass

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    query = query.order_by(CrawledArticle.publish_date.desc().nullslast())
    query = query.offset((page - 1) * page_size).limit(page_size)
    items = db.execute(query).scalars().all()

    return ArticleListResponse(
        items=[ArticleResponse.model_validate(a) for a in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/articles/today", response_model=ArticleListResponse)
def list_today_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """获取当天爬取的文章；当天无数据则返回最近一次采集的文章。"""
    today = datetime.now().strftime("%Y-%m-%d")
    query = select(CrawledArticle).where(
        CrawledArticle.status == "active",
        func.date(CrawledArticle.crawl_date) == today,
    ).order_by(CrawledArticle.crawl_date.desc())

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0

    if total == 0:
        latest_date = db.execute(
            select(func.date(CrawledArticle.crawl_date))
            .where(CrawledArticle.status == "active")
            .order_by(CrawledArticle.crawl_date.desc())
            .limit(1)
        ).scalar()

        if latest_date:
            query = select(CrawledArticle).where(
                CrawledArticle.status == "active",
                func.date(CrawledArticle.crawl_date) == latest_date,
            ).order_by(CrawledArticle.crawl_date.desc())
            total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    query = query.offset((page - 1) * page_size).limit(page_size)
    items = db.execute(query).scalars().all()

    return ArticleListResponse(
        items=[ArticleResponse.model_validate(a) for a in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.execute(
        select(CrawledArticle).where(CrawledArticle.id == article_id)
    ).scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article


@router.get("/sources")
def get_sources():
    return {
        "sources": [
            {"key": k, "name": v["name"], "url": v["url"]}
            for k, v in SOURCES.items()
        ]
    }


@router.post("/trigger", response_model=CrawlTriggerResponse)
def trigger_crawl(
    source: str | None = None,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
):
    """手动触发爬取（仅管理员）。"""
    crawled, errors = run_crawler(db, source)
    return CrawlTriggerResponse(
        message=f"爬取完成，新增 {crawled} 条文章",
        crawled=crawled,
        errors=errors,
    )


@router.delete("/articles/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """删除单篇文章（需登录）。"""
    article = db.execute(
        select(CrawledArticle).where(CrawledArticle.id == article_id)
    ).scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(article)
    db.commit()
    return {"message": "已删除", "id": article_id}


@router.delete("/articles")
def clear_all_articles(
    source: str | None = Query(None, description="按信源清空，为空则清空全部"),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """清空文章（需登录）。可按信源清空或全部清空。"""
    stmt = delete(CrawledArticle)
    if source:
        source_name = SOURCES.get(source, {}).get("name", source)
        stmt = stmt.where(CrawledArticle.source == source_name)
        db.execute(stmt)
        db.commit()
        return {"message": f"已清空 {source_name} 的全部文章"}
    else:
        count = db.execute(select(func.count()).select_from(CrawledArticle)).scalar() or 0
        db.execute(stmt)
        db.commit()
        return {"message": f"已清空全部文章（共 {count} 条）"}
