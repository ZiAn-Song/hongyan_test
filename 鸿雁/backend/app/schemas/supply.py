from datetime import datetime

from pydantic import BaseModel


class SupplyResponse(BaseModel):
    """内地供给响应模型"""
    id: int
    supply_id: str
    provider: str
    location: str | None = None
    subject_type: str | None = None
    services: str | None = None
    tech_advantages: str | None = None
    use_cases: str | None = None
    border_fit: str | None = None
    delivery_mode: str | None = None
    contact: str | None = None
    source_level: str | None = None
    publish_date: str | None = None
    source_url: str | None = None
    verification_status: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SupplyListResponse(BaseModel):
    items: list[SupplyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
