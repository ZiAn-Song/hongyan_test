from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.achievement import MainlandSupply


def list_supplies(
    db: Session,
    subject_type: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    query = db.query(MainlandSupply).order_by(MainlandSupply.created_at.desc())

    if subject_type:
        query = query.filter(MainlandSupply.subject_type == subject_type)

    total = query.count()
    supplies = (
        query.offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": supplies,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_supply(db: Session, supply_id: str) -> MainlandSupply:
    supply = db.query(MainlandSupply).filter(MainlandSupply.supply_id == supply_id).first()
    if not supply:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"供给 {supply_id} 不存在",
        )
    return supply
