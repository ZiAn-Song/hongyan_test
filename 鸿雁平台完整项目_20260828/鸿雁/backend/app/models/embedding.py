from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ResourceEmbedding(Base):
    """资源向量索引（L2 语义召回）。

    生产 PostgreSQL 时本表可平迁为 pgvector 的 vector 列；
    当前阶段 embedding 以 JSON 数组存储、Python 计算余弦（190 条毫秒级）。
    """
    __tablename__ = "resource_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_type: Mapped[str] = mapped_column(String(30), index=True)  # demand/supply/talent
    source_id: Mapped[str] = mapped_column(String(50), index=True)    # XQ-001 / GJ-001 / TAL-001
    model: Mapped[str] = mapped_column(String(100), default="")
    embedding: Mapped[str] = mapped_column(Text)                      # JSON 数组
    content_digest: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
