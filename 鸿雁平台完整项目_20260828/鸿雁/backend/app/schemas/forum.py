from datetime import datetime

from pydantic import BaseModel, Field


class PostCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    content: str = Field(..., min_length=5)
    category: str = Field("最新", max_length=20)
    team: str | None = Field(None, max_length=100)
    location: str | None = Field(None, max_length=200)


class CommentCreateRequest(BaseModel):
    content: str = Field(..., min_length=2)


class CommentResponse(BaseModel):
    id: int
    post_id: int
    author_id: int | None = None
    author_name: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PostResponse(BaseModel):
    id: int
    author_id: int | None = None
    author_name: str
    title: str
    content: str
    category: str
    team: str | None = None
    location: str | None = None
    views: int = 0
    likes: int = 0
    created_at: datetime
    comments: list[CommentResponse] = []

    model_config = {"from_attributes": True}


class PostListResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
