from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.team import TeamCreateRequest, TeamResponse, TeamListResponse
from app.services.team_service import list_teams, get_team, create_team
from app.utils.dependencies import get_current_personal_user, CurrentUser

router = APIRouter()


@router.get("/", response_model=TeamListResponse)
def list_teams_api(
    category: str | None = Query(None, description="按专业领域筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    return list_teams(db, category, page, page_size)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team_api(team_id: int, db: Session = Depends(get_db)):
    return get_team(db, team_id)


@router.post("/", response_model=TeamResponse, status_code=201)
def create_team_api(
    data: TeamCreateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_personal_user),
):
    return create_team(db, data, current_user)
