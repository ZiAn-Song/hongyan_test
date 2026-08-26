from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.forum import ForumPost, ForumComment
from app.schemas.forum import PostCreateRequest, CommentCreateRequest
from app.utils.dependencies import CurrentUser


def list_posts(
    db: Session,
    category: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    query = db.query(ForumPost)
    if category:
        query = query.filter(ForumPost.category == category)

    total = query.count()
    posts = (
        query.order_by(ForumPost.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_post(db: Session, post_id: int) -> ForumPost:
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"帖子 {post_id} 不存在",
        )
    post.views += 1
    db.commit()
    db.refresh(post)
    return post


def create_post(
    db: Session,
    data: PostCreateRequest,
    current_user: CurrentUser,
) -> ForumPost:
    post = ForumPost(
        author_id=current_user.id,
        author_name=current_user.name or "匿名用户",
        title=data.title,
        content=data.content,
        category=data.category,
        team=data.team,
        location=data.location,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def create_comment(
    db: Session,
    post_id: int,
    data: CommentCreateRequest,
    current_user: CurrentUser,
) -> ForumComment:
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"帖子 {post_id} 不存在",
        )

    comment = ForumComment(
        post_id=post_id,
        author_id=current_user.id,
        author_name=current_user.name or "匿名用户",
        content=data.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
