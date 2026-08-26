from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CrawledArticle(Base):
    __tablename__ = "crawled_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), index=True)
    source: Mapped[str] = mapped_column(String(50), index=True)
    source_url: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    author: Mapped[str | None] = mapped_column(String(100), nullable=True)
    publish_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    crawl_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)

    __table_args__ = (
        Index("ix_crawled_source_date", "source", "publish_date"),
    )
