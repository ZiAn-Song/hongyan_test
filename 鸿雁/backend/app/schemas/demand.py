from datetime import datetime

from pydantic import BaseModel, Field


class DemandResponse(BaseModel):
    """边疆需求响应模型"""
    id: int
    demand_id: str
    title: str
    province: str | None = None
    coverage: str | None = None
    location_detail: str | None = None
    publisher: str | None = None
    pain_point: str | None = None
    description: str | None = None
    expected_goal: str | None = None
    stage: str | None = None
    supply_tags: str | None = None
    contact: str | None = None
    source_level: str | None = None
    publish_date: str | None = None
    source_url: str | None = None
    verification_status: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class DemandListResponse(BaseModel):
    items: list[DemandResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
