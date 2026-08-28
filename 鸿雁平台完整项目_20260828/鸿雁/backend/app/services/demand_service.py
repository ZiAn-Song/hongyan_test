from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.demand import Demand
from app.schemas.demand import DemandCreateRequest
from app.utils.dependencies import CurrentUser


def list_demands(
    db: Session,
    category: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    query = db.query(Demand).order_by(Demand.created_at.desc())

    if category:
        all_demands = query.all()
        filtered = [
            d for d in all_demands
            if d.target_majors and category in d.target_majors
        ]
        total = len(filtered)
        start = (page - 1) * page_size
        demands = filtered[start:start + page_size]
    else:
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


def get_demand(db: Session, demand_id: int) -> Demand:
    demand = db.query(Demand).filter(Demand.id == demand_id).first()
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"需求 {demand_id} 不存在",
        )
    return demand


def create_demand(
    db: Session,
    data: DemandCreateRequest,
    current_user: CurrentUser,
) -> Demand:
    company = None
    company_name = data.org_name

    if current_user.user_type == "enterprise":
        company = db.query(Company).filter(Company.id == current_user.id).first()
        if company:
            company_name = company.org_name

    demand = Demand(
        company_id=current_user.id if current_user.user_type == "enterprise" else None,
        company_name=company_name,
        internship_location=data.internship_location,
        estimated_time=data.estimated_time,
        requirements_content=data.requirements_content,
        target_majors=data.target_majors,
        org_type=data.org_type,
        org_name=data.org_name,
        contact_info=data.contact_info,
    )
    db.add(demand)
    db.commit()
    db.refresh(demand)
    return demand
