from pydantic import BaseModel, Field
from datetime import datetime


class ArticleBase(BaseModel):
    title: str = Field(..., max_length=500)
    source: str = Field(..., max_length=50)
    source_url: str = Field(..., max_length=500)
    summary: str | None = None
    author: str | None = None
    category: str | None = None
    region: str | None = None


class ArticleResponse(ArticleBase):
    id: int
    content: str | None = None
    publish_date: datetime | None = None
    crawl_date: datetime | None = None
    status: str = "active"

    model_config = {"from_attributes": True}


class ArticleListResponse(BaseModel):
    items: list[ArticleResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CrawlTriggerRequest(BaseModel):
    source: str | None = Field(None, description="指定爬取源，为空则全部爬取")


class CrawlTriggerResponse(BaseModel):
    message: str
    crawled: int
    errors: list[str] = []
