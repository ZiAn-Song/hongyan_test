from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.matching_service import match_supplies_for_demand, match_demands_for_supply

router = APIRouter()


@router.get("/demands/{demand_id}/supplies")
def get_matching_supplies(
    demand_id: str,
    top_k: int = Query(5, ge=1, le=20),
    subject_type: str | None = Query(None, description="按主体类型筛选"),
    db: Session = Depends(get_db),
):
    result = match_supplies_for_demand(db, demand_id, top_k=top_k, subject_type=subject_type)
    if not result["demand"]:
        raise HTTPException(status_code=404, detail=f"需求 {demand_id} 不存在")
    return result


@router.get("/supplies/{supply_id}/demands")
def get_matching_demands(
    supply_id: str,
    top_k: int = Query(5, ge=1, le=20),
    province: str | None = Query(None, description="按省份筛选"),
    db: Session = Depends(get_db),
):
    result = match_demands_for_supply(db, supply_id, top_k=top_k, province=province)
    if not result["supply"]:
        raise HTTPException(status_code=404, detail=f"供给 {supply_id} 不存在")
    return result
