from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.team import Team, TeamMember
from app.schemas.team import TeamCreateRequest
from app.utils.dependencies import CurrentUser


def list_teams(
    db: Session,
    category: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    query = db.query(Team)
    if category:
        query = query.filter(Team.team_specialty == category)

    total = query.count()
    teams = (
        query.order_by(Team.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": teams,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_team(db: Session, team_id: int) -> Team:
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"团队 {team_id} 不存在",
        )
    return team


def create_team(db: Session, data: TeamCreateRequest, current_user: CurrentUser) -> Team:
    team = Team(
        team_name=data.team_name,
        leader_name=data.leader_name,
        leader_contact=data.leader_contact,
        leader_email=data.leader_email,
        student_id=data.student_id,
        university=data.university,
        team_specialty=data.team_specialty,
        team_description=data.team_description,
        teacher_name=data.teacher_name,
        teacher_contact=data.teacher_contact,
    )
    db.add(team)
    db.flush()

    member = TeamMember(
        team_id=team.id,
        user_id=current_user.id if current_user.user_type == "personal" else None,
        member_name=data.leader_name,
        role="leader",
    )
    db.add(member)
    db.commit()
    db.refresh(team)
    return team
