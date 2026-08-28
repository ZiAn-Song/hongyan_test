import re

from sqlalchemy.orm import Session

from app.models.team import Team
from app.models.demand import Demand
from app.models.forum import ForumPost
from app.models.document import DocumentChunk

CHUNK_SIZE = 200


def _chunk_text(text: str, size: int = CHUNK_SIZE) -> list[str]:
    if not text or len(text) <= size:
        return [text] if text else []

    sentences = re.split(r"(?<=[。！？\n.!?])", text)
    sentences = [s for s in sentences if s.strip()]

    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) > size and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current += sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks


def _index_source(
    db: Session,
    source_type: str,
    source_id: int,
    content: str,
    metadata: dict | None = None,
) -> int:
    db.query(DocumentChunk).filter(
        DocumentChunk.source_type == source_type,
        DocumentChunk.source_id == source_id,
    ).delete()

    chunks = _chunk_text(content)
    for i, chunk in enumerate(chunks):
        doc = DocumentChunk(
            source_type=source_type,
            source_id=source_id,
            chunk_index=i,
            content=chunk,
            metadata_=metadata,
        )
        db.add(doc)

    return len(chunks)


def index_all(db: Session) -> dict:
    team_count = 0
    demand_count = 0
    post_count = 0
    total_chunks = 0

    for team in db.query(Team).all():
        content = f"团队名称：{team.team_name}\n"
        content += f"专业领域：{team.team_specialty}\n"
        if team.team_description:
            content += f"团队简介：{team.team_description}\n"
        if team.university:
            content += f"所属高校：{team.university}\n"
        if team.leader_name:
            content += f"队长：{team.leader_name}\n"

        total_chunks += _index_source(db, "team", team.id, content, {
            "team_name": team.team_name,
            "team_specialty": team.team_specialty,
        })
        team_count += 1

    for demand in db.query(Demand).all():
        content = f"需求方：{demand.company_name}\n"
        content += f"实践地点：{demand.internship_location or ''}\n"
        content += f"预计时间：{demand.estimated_time or ''}\n"
        if demand.requirements_content:
            content += f"需求描述：{demand.requirements_content}\n"
        if demand.target_majors:
            content += f"目标专业：{'、'.join(demand.target_majors)}\n"

        total_chunks += _index_source(db, "demand", demand.id, content, {
            "company_name": demand.company_name,
            "target_majors": demand.target_majors,
        })
        demand_count += 1

    for post in db.query(ForumPost).all():
        content = f"标题：{post.title}\n"
        content += f"内容：{post.content}\n"
        if post.team:
            content += f"团队：{post.team}\n"
        if post.location:
            content += f"地点：{post.location}\n"

        total_chunks += _index_source(db, "forum_post", post.id, content, {
            "title": post.title,
            "category": post.category,
        })
        post_count += 1

    db.commit()

    return {
        "indexed": total_chunks,
        "sources": {
            "teams": team_count,
            "demands": demand_count,
            "posts": post_count,
        },
        "message": f"成功索引 {total_chunks} 个文本分块",
    }


def search(db: Session, query: str, top_k: int = 5) -> list[dict]:
    chunks = db.query(DocumentChunk).all()
    if not chunks:
        return []

    query_keywords = [w.strip() for w in re.split(r"[\s，。、,.!?]+", query) if len(w.strip()) >= 2]
    if not query_keywords:
        query_keywords = [query]

    scored = []
    for chunk in chunks:
        score = 0
        for keyword in query_keywords:
            count = chunk.content.count(keyword)
            score += count
        if score > 0:
            scored.append({
                "content": chunk.content,
                "source_type": chunk.source_type,
                "source_id": chunk.source_id,
                "score": score,
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def get_context(db: Session, query: str, top_k: int = 5) -> str:
    results = search(db, query, top_k)
    if not results:
        return ""

    context_parts = []
    for i, r in enumerate(results, 1):
        context_parts.append(f"[{i}] ({r['source_type']}) {r['content']}")

    return "\n\n".join(context_parts)


def clear_index(db: Session) -> int:
    count = db.query(DocumentChunk).count()
    db.query(DocumentChunk).delete()
    db.commit()
    return count
