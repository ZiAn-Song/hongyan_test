from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.supply import SupplyResponse, SupplyListResponse
from app.services.supply_service import list_supplies, get_supply

router = APIRouter()


@router.get("/", response_model=SupplyListResponse)
def list_supplies_api(
    subject_type: str | None = Query(None, description="按主体类型筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    return list_supplies(db, subject_type, page, page_size)


@router.get("/{supply_id}", response_model=SupplyResponse)
def get_supply_api(supply_id: str, db: Session = Depends(get_db)):
    return get_supply(db, supply_id)
