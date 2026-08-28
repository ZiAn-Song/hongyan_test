from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.matching_service import match_supplies_for_demand, match_demands_for_supply
from app.models.achievement import BorderDemand

router = APIRouter()


@router.get("/demands/{demand_id}/supplies")
def get_matching_supplies(
    demand_id: str,
    top_k: int = Query(5, ge=1, le=20),
    subject_type: str | None = Query(None, description="按主体类型筛选"),
    db: Session = Depends(get_db),
):
    result = match_supplies_for_demand(db, demand_id, top_k=top_k, subject_type=subject_type)
    if not result["demand"]:
        raise HTTPException(status_code=404, detail=f"需求 {demand_id} 不存在")
    return result


@router.get("/supplies/{supply_id}/demands")
def get_matching_demands(
    supply_id: str,
    top_k: int = Query(5, ge=1, le=20),
    province: str | None = Query(None, description="按省份筛选"),
    db: Session = Depends(get_db),
):
    result = match_demands_for_supply(db, supply_id, top_k=top_k, province=province)
    if not result["supply"]:
        raise HTTPException(status_code=404, detail=f"供给 {supply_id} 不存在")
    return result


# ================= v2：三级漏斗完整匹配（跨类型统一排序 + DeepSeek 研判）=================
from fastapi import Query as FQuery

from app.services.matching_service import match_all_for_demand


@router.get("/v2/demands/{demand_id}/match")
def match_v2(
    demand_id: str,
    top_k: int = FQuery(8, ge=1, le=20),
    use_llm: bool = FQuery(True, description="是否启用 DeepSeek 第三级研判"),
    subject_type: str | None = FQuery(None, description="按主体类型筛选"),
    db: Session = Depends(get_db),
):
    """三级漏斗智能匹配（跨类型统一排序）

    第一级：SQL 载入内地供给 + 山大人才
    第二级：关键词+标签加权 × 三因子动态可信度
    第三级：DeepSeek 研判（评分/理由/风险/建议），失败自动降级规则模式
    附：历史范式参考（已完成成果可复制协作点）
    """
    result = match_all_for_demand(db, demand_id, top_k=top_k, use_llm=use_llm,
                                  subject_type=subject_type)
    if not result["demand"]:
        raise HTTPException(status_code=404, detail=f"需求 {demand_id} 不存在")
    return result


# ================= v2 双向自由对接（真实使用逻辑）=================
from pydantic import BaseModel as _BaseModel


class FreeMatchRequest(_BaseModel):
    text: str
    top_k: int = 8
    use_llm: bool = True


@router.post("/v2/freestyle")
def freestyle_match(body: FreeMatchRequest, db: Session = Depends(get_db)):
    """需求方路径：自由描述需求 → DeepSeek 解析 → 三级漏斗匹配资源库"""
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="需求描述不能为空")
    from app.services.matching_service import match_freetext_for_demand
    return match_freetext_for_demand(db, body.text.strip(),
                                     top_k=body.top_k, use_llm=body.use_llm)


@router.post("/v2/reverse")
def reverse_match(body: FreeMatchRequest, db: Session = Depends(get_db)):
    """供给方路径：输入能力画像 → 反向匹配边疆需求库 + 历史范式"""
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="能力画像不能为空")
    from app.services.matching_service import match_profile_for_demands
    return match_profile_for_demands(db, body.text.strip(),
                                     top_k=body.top_k, use_llm=body.use_llm)


@router.get("/border-demands")
def list_border_demands(province: str | None = None,
                        db: Session = Depends(get_db)):
    """边疆需求轻量列表（地图可视化用）：点击省份返回该省需求。"""
    from sqlalchemy import select as _select
    q = db.execute(
        _select(BorderDemand).where(BorderDemand.demand_id != None)  # noqa: E711
    ).scalars().all()
    items = [{
        "demand_id": d.demand_id, "title": d.title, "province": d.province,
        "stage": d.stage, "supply_tags": d.supply_tags,
        "pain_point": (d.pain_point or d.description or "")[:120],
    } for d in q if (not province or (d.province and province in d.province))]
    return {"items": items, "total": len(items)}
