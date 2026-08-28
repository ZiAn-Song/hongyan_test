from datetime import datetime

from sqlalchemy import String, Integer, Text, Boolean, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContactThread(Base):
    """站内对接会话（类招聘 App 的沟通通道）。

    - 发起人对某个匹配结果（需求/供给/人才）发起对接意向；
    - target_user_id：对方是平台注册用户时填其 id（用户↔用户私聊）；
      案例库实体（无账号）为 NULL——会话作为对接意向单沉淀，管理员可见跟进。
    """
    __tablename__ = "contact_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_type: Mapped[str] = mapped_column(String(20), index=True)   # demand/supply/talent
    subject_id: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    subject_title: Mapped[str] = mapped_column(String(500))
    entity_contact: Mapped[str | None] = mapped_column(Text, nullable=True)  # 实体联系渠道快照
    entity_link: Mapped[str | None] = mapped_column(String(1000), nullable=True)  # 信源原文
    initiator_id: Mapped[int] = mapped_column(Integer, index=True)      # 发起人 users.id
    initiator_name: Mapped[str] = mapped_column(String(50), default="")
    target_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_message_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_contact_thread_initiator", "initiator_id", "subject_type", "subject_id"),
    )


class ContactMessage(Base):
    """会话消息。is_read：接收方已读标记（发送方发出的默认未读）。"""
    __tablename__ = "contact_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thread_id: Mapped[int] = mapped_column(Integer, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, index=True)
    sender_name: Mapped[str] = mapped_column(String(50), default="")
    content: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
