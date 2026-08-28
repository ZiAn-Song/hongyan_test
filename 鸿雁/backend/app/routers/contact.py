"""站内对接通道 API（类招聘 App 的沟通系统）。

- 发起对接：POST /threads（对某个匹配结果发送对接意向，幂等——同主体已有会话则追加消息）
- 我的会话：GET /threads（含未读数与最后一条预览）
- 会话消息：GET /threads/{id}/messages（拉取并标记对方消息已读）
- 回复：POST /threads/{id}/messages
- 未读角标：GET /unread-count
- 权限：会话参与者可见；管理员可见全部（负责跟进无平台账号的案例库实体对接）。
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, func, or_, case
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.contact import ContactThread, ContactMessage
from app.models.user import User
from app.utils.dependencies import get_current_user, CurrentUser

router = APIRouter()


class ThreadCreateRequest(BaseModel):
    subject_type: str = Field(..., pattern=r"^(demand|supply|talent)$")
    subject_id: str | None = None
    subject_title: str = Field(..., min_length=1, max_length=500)
    entity_contact: str | None = None
    entity_link: str | None = None
    message: str = Field(..., min_length=1, max_length=2000)
    target_user_id: int | None = None


class MessageCreateRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


def _thread_visible(t: ContactThread, me: CurrentUser) -> bool:
    return t.initiator_id == me.id or t.target_user_id == me.id or me.role == "admin"


@router.post("/threads")
def start_thread(body: ThreadCreateRequest,
                 me: CurrentUser = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    """发起对接：同主体已有会话则追加消息（幂等），否则新建会话。"""
    thread = db.execute(
        select(ContactThread).where(
            ContactThread.initiator_id == me.id,
            ContactThread.subject_type == body.subject_type,
            ContactThread.subject_id == (body.subject_id or ""),
        )
    ).scalars().first()

    now = datetime.now()
    if thread is None:
        thread = ContactThread(
            subject_type=body.subject_type,
            subject_id=body.subject_id or "",
            subject_title=body.subject_title,
            entity_contact=body.entity_contact,
            entity_link=body.entity_link,
            initiator_id=me.id,
            initiator_name=me.name or "",
            target_user_id=body.target_user_id,
            last_message_at=now,
        )
        db.add(thread)
        db.flush()

    db.add(ContactMessage(
        thread_id=thread.id, sender_id=me.id, sender_name=me.name or "",
        content=body.message, is_read=False))
    thread.last_message_at = now
    db.commit()
    return {"thread_id": thread.id, "message": "对接意向已发送"}


@router.get("/threads")
def list_threads(me: CurrentUser = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    """我的会话列表（管理员可见全部），按最后消息时间倒序，含未读数。"""
    query = db.execute(
        select(ContactThread).where(
            or_(ContactThread.initiator_id == me.id,
                ContactThread.target_user_id == me.id,
                me.role == "admin"))
    ).scalars().all()

    items = []
    for t in query:
        last = db.execute(
            select(ContactMessage).where(ContactMessage.thread_id == t.id)
            .order_by(ContactMessage.created_at.desc()).limit(1)
        ).scalars().first()
        unread = db.execute(
            select(func.count()).select_from(ContactMessage).where(
                ContactMessage.thread_id == t.id,
                ContactMessage.sender_id != me.id,
                ContactMessage.is_read == False,  # noqa: E712
            )
        ).scalar() or 0
        items.append({
            "id": t.id,
            "subject_type": t.subject_type,
            "subject_id": t.subject_id,
            "subject_title": t.subject_title,
            "entity_contact": t.entity_contact,
            "entity_link": t.entity_link,
            "initiator_id": t.initiator_id,
            "initiator_name": t.initiator_name,
            "is_mine": t.initiator_id == me.id,
            "last_message": last.content[:80] if last else "",
            "last_message_at": last.created_at.isoformat() if last else t.created_at.isoformat(),
            "unread": unread,
        })
    items.sort(key=lambda x: x["last_message_at"], reverse=True)
    return {"items": items, "total": len(items)}


@router.get("/unread-count")
def unread_count(me: CurrentUser = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    """头部角标：我参与会话中，别人发给我的未读消息总数。"""
    n = db.execute(
        select(func.count()).select_from(ContactMessage)
        .join(ContactThread, ContactMessage.thread_id == ContactThread.id)
        .where(
            or_(ContactThread.initiator_id == me.id,
                ContactThread.target_user_id == me.id,
                me.role == "admin"),
            ContactMessage.sender_id != me.id,
            ContactMessage.is_read == False,  # noqa: E712
        )
    ).scalar() or 0
    return {"unread": n}


@router.get("/threads/{thread_id}/messages")
def get_messages(thread_id: int, me: CurrentUser = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    thread = db.get(ContactThread, thread_id)
    if not thread or not _thread_visible(thread, me):
        raise HTTPException(status_code=404, detail="会话不存在")
    msgs = db.execute(
        select(ContactMessage).where(ContactMessage.thread_id == thread_id)
        .order_by(ContactMessage.created_at.asc())
    ).scalars().all()
    # 拉取即把对方发来的消息标记已读
    for m in msgs:
        if m.sender_id != me.id and not m.is_read:
            m.is_read = True
    db.commit()
    return {
        "thread": {
            "id": thread.id, "subject_type": thread.subject_type,
            "subject_id": thread.subject_id, "subject_title": thread.subject_title,
            "entity_contact": thread.entity_contact, "entity_link": thread.entity_link,
            "initiator_name": thread.initiator_name, "is_mine": thread.initiator_id == me.id,
        },
        "items": [{
            "id": m.id, "sender_id": m.sender_id, "sender_name": m.sender_name,
            "content": m.content, "created_at": m.created_at.isoformat(),
            "mine": m.sender_id == me.id,
        } for m in msgs],
    }


@router.post("/threads/{thread_id}/messages")
def send_message(thread_id: int, body: MessageCreateRequest,
                 me: CurrentUser = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    thread = db.get(ContactThread, thread_id)
    if not thread or not _thread_visible(thread, me):
        raise HTTPException(status_code=404, detail="会话不存在")
    db.add(ContactMessage(thread_id=thread_id, sender_id=me.id,
                          sender_name=me.name or "", content=body.content))
    thread.last_message_at = datetime.now()
    db.commit()
    return {"message": "已发送"}
