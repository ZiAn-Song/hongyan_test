from datetime import datetime

from pydantic import BaseModel, Field


class TeamMemberResponse(BaseModel):
    id: int
    member_name: str
    role: str

    model_config = {"from_attributes": True}


class TeamCreateRequest(BaseModel):
    team_name: str = Field(..., min_length=2, max_length=100)
    leader_name: str = Field(..., min_length=2, max_length=50)
    leader_contact: str | None = Field(None, max_length=20)
    leader_email: str | None = Field(None, max_length=100)
    student_id: str | None = Field(None, max_length=20)
    university: str | None = Field(None, max_length=100)
    team_specialty: str = Field(..., max_length=50)
    team_description: str | None = Field(None)
    teacher_name: str | None = Field(None, max_length=50)
    teacher_contact: str | None = Field(None, max_length=20)


class TeamResponse(BaseModel):
    id: int
    team_name: str
    leader_name: str
    leader_contact: str | None = None
    leader_email: str | None = None
    student_id: str | None = None
    university: str | None = None
    team_specialty: str
    team_description: str | None = None
    teacher_name: str | None = None
    teacher_contact: str | None = None
    created_at: datetime
    members: list[TeamMemberResponse] = []

    model_config = {"from_attributes": True}


class TeamListResponse(BaseModel):
    items: list[TeamResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
