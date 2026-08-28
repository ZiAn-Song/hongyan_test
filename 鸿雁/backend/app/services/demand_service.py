from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.achievement import BorderDemand


def list_demands(
    db: Session,
    province: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    query = db.query(BorderDemand).order_by(BorderDemand.created_at.desc())

    if province:
        query = query.filter(BorderDemand.province == province)

    total = query.count()
    demands = (
        query.offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": demands,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_demand(db: Session, demand_id: str) -> BorderDemand:
    demand = db.query(BorderDemand).filter(BorderDemand.demand_id == demand_id).first()
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"需求 {demand_id} 不存在",
        )
    return demand
