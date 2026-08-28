from datetime import datetime

from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Demand(Base):
    __tablename__ = "demands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), nullable=True, index=True)
    company_name: Mapped[str] = mapped_column(String(200), index=True)
    internship_location: Mapped[str | None] = mapped_column(String(300), nullable=True)
    estimated_time: Mapped[str | None] = mapped_column(String(100), nullable=True)
    requirements_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_majors: Mapped[list | None] = mapped_column(JSON, nullable=True)
    org_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    org_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    contact_info: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    company: Mapped["Company | None"] = relationship(back_populates="demands")
