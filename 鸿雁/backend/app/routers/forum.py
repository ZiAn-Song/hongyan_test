from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.forum import (
    PostCreateRequest,
    CommentCreateRequest,
    PostResponse,
    PostListResponse,
    CommentResponse,
)
from app.services.forum_service import (
    list_posts,
    get_post,
    create_post,
    create_comment,
)
from app.utils.dependencies import get_current_user, CurrentUser

router = APIRouter()


@router.get("/posts", response_model=PostListResponse)
def list_posts_api(
    category: str | None = Query(None, description="按分类筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    return list_posts(db, category, page, page_size)


@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post_api(post_id: int, db: Session = Depends(get_db)):
    return get_post(db, post_id)


@router.post("/posts", response_model=PostResponse, status_code=201)
def create_post_api(
    data: PostCreateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return create_post(db, data, current_user)


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment_api(
    post_id: int,
    data: CommentCreateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return create_comment(db, post_id, data, current_user)
