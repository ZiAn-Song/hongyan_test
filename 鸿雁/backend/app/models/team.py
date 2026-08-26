from datetime import datetime

from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_name: Mapped[str] = mapped_column(String(100), index=True)
    leader_name: Mapped[str] = mapped_column(String(50))
    leader_contact: Mapped[str | None] = mapped_column(String(20), nullable=True)
    leader_email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    student_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    university: Mapped[str | None] = mapped_column(String(100), nullable=True)
    team_specialty: Mapped[str] = mapped_column(String(50), index=True)
    team_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    teacher_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    teacher_contact: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    members: Mapped[list["TeamMember"]] = relationship(back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    member_name: Mapped[str] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(20), default="member")

    team: Mapped["Team"] = relationship(back_populates="members")
    user: Mapped["User | None"] = relationship(back_populates="team_memberships", foreign_keys=[user_id])
