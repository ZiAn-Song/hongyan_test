from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BorderDemand(Base):
    """边疆需求侧"""
    __tablename__ = "border_demands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    demand_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(500), index=True)
    province: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    coverage: Mapped[str | None] = mapped_column(String(200), nullable=True)
    location_detail: Mapped[str | None] = mapped_column(String(300), nullable=True)
    publisher: Mapped[str | None] = mapped_column(String(300), nullable=True)
    pain_point: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    stage: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    supply_tags: Mapped[str | None] = mapped_column(String(500), nullable=True)
    contact: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    publish_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    verification_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class MainlandSupply(Base):
    """内地供给侧"""
    __tablename__ = "mainland_supplies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    supply_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    provider: Mapped[str] = mapped_column(String(500), index=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    subject_type: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    services: Mapped[str | None] = mapped_column(Text, nullable=True)
    tech_advantages: Mapped[str | None] = mapped_column(Text, nullable=True)
    use_cases: Mapped[str | None] = mapped_column(Text, nullable=True)
    border_fit: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_mode: Mapped[str | None] = mapped_column(String(300), nullable=True)
    contact: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    publish_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    verification_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
