from datetime import datetime

from pydantic import BaseModel, Field


class DemandCreateRequest(BaseModel):
    internship_location: str = Field(..., max_length=300)
    estimated_time: str = Field(..., max_length=100)
    requirements_content: str = Field(..., min_length=10)
    target_majors: list[str] = Field(default_factory=list)
    org_type: str = Field(..., max_length=50)
    org_name: str = Field(..., max_length=200)
    contact_info: str = Field(..., max_length=50)


class DemandResponse(BaseModel):
    id: int
    company_id: int | None = None
    company_name: str
    internship_location: str | None = None
    estimated_time: str | None = None
    requirements_content: str | None = None
    target_majors: list | None = None
    org_type: str | None = None
    org_name: str | None = None
    contact_info: str | None = None
    status: str = "open"
    created_at: datetime

    model_config = {"from_attributes": True}


class DemandListResponse(BaseModel):
    items: list[DemandResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
