from datetime import datetime
import json

from sqlalchemy import String, Integer, Text, DateTime, func, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DocumentChunk(Base):
    """
    RAG 文档分块表 - 存储文本分块及其向量嵌入。

    开发环境（SQLite）：embedding 存储为 JSON 字符串。
    生产环境（PostgreSQL + pgvector）：可将 embedding 列类型改为 vector，
    并添加 GIN 索引以支持高效相似度搜索。

    source_type 取值：
      - team: 团队描述
      - demand: 需求内容
      - forum_post: 论坛帖子
      - user_profile: 用户画像
    """

    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_type: Mapped[str] = mapped_column(String(30), index=True)
    source_id: Mapped[int] = mapped_column(Integer, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("ix_document_source", "source_type", "source_id"),
    )

    def set_embedding(self, vector: list[float]) -> None:
        self.embedding = json.dumps(vector)

    def get_embedding(self) -> list[float] | None:
        if self.embedding is None:
            return None
        return json.loads(self.embedding)
