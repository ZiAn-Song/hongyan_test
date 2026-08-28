from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.demand import DemandResponse, DemandListResponse
from app.services.demand_service import list_demands, get_demand

router = APIRouter()


@router.get("/", response_model=DemandListResponse)
def list_demands_api(
    province: str | None = Query(None, description="按省份筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    return list_demands(db, province, page, page_size)


@router.get("/{demand_id}", response_model=DemandResponse)
def get_demand_api(demand_id: str, db: Session = Depends(get_db)):
    return get_demand(db, demand_id)
