from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.demand import DemandCreateRequest, DemandResponse, DemandListResponse
from app.services.demand_service import list_demands, get_demand, create_demand
from app.utils.dependencies import get_current_enterprise_user, CurrentUser

router = APIRouter()


@router.get("/", response_model=DemandListResponse)
def list_demands_api(
    category: str | None = Query(None, description="按目标专业筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    return list_demands(db, category, page, page_size)


@router.get("/{demand_id}", response_model=DemandResponse)
def get_demand_api(demand_id: int, db: Session = Depends(get_db)):
    return get_demand(db, demand_id)


@router.post("/", response_model=DemandResponse, status_code=201)
def create_demand_api(
    data: DemandCreateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_enterprise_user),
):
    return create_demand(db, data, current_user)
