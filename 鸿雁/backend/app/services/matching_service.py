"""
智能匹配服务 MVP
第一层：SQL硬性筛选（地域、主体类型）
第二层：关键词检索（文本分词匹配 + 标签匹配加权）
"""
import re
from sqlalchemy.orm import Session

from app.models.achievement import BorderDemand, MainlandSupply


def _extract_keywords(text: str) -> list[str]:
    if not text:
        return []
    words = [w.strip() for w in re.split(r"[\s，。、,.!?；;：:（）()【】\[\]\"'《》/\\\-—_]+", text) if len(w.strip()) >= 2]
    return list(set(words))


def _build_demand_text(demand: BorderDemand) -> str:
    parts = []
    if demand.pain_point:
        parts.append(demand.pain_point)
    if demand.description:
        parts.append(demand.description)
    if demand.expected_goal:
        parts.append(demand.expected_goal)
    if demand.supply_tags:
        parts.append(demand.supply_tags)
    return " ".join(parts)


def _build_supply_text(supply: MainlandSupply) -> str:
    parts = []
    if supply.services:
        parts.append(supply.services)
    if supply.tech_advantages:
        parts.append(supply.tech_advantages)
    if supply.use_cases:
        parts.append(supply.use_cases)
    if supply.border_fit:
        parts.append(supply.border_fit)
    return " ".join(parts)


def _keyword_score(keywords: list[str], text: str) -> float:
    if not keywords or not text:
        return 0.0
    score = 0.0
    for kw in keywords:
        count = text.count(kw)
        if count > 0:
            score += min(count, 5) * 1.0
    return score


def _demand_to_dict(demand: BorderDemand) -> dict:
    return {
        "demand_id": demand.demand_id,
        "title": demand.title,
        "province": demand.province,
        "publisher": demand.publisher,
        "stage": demand.stage,
        "supply_tags": demand.supply_tags,
        "pain_point": demand.pain_point,
        "description": demand.description,
        "expected_goal": demand.expected_goal,
        "contact": demand.contact,
        "source_url": demand.source_url,
    }


def _supply_to_dict(supply: MainlandSupply) -> dict:
    return {
        "supply_id": supply.supply_id,
        "provider": supply.provider,
        "location": supply.location,
        "subject_type": supply.subject_type,
        "services": supply.services,
        "tech_advantages": supply.tech_advantages,
        "use_cases": supply.use_cases,
        "border_fit": supply.border_fit,
        "delivery_mode": supply.delivery_mode,
        "contact": supply.contact,
        "source_url": supply.source_url,
    }


def match_supplies_for_demand(db: Session, demand_id: str, top_k: int = 5, subject_type: str | None = None) -> dict:
    """为边疆需求匹配内地供给方"""
    demand = db.query(BorderDemand).filter(BorderDemand.demand_id == demand_id).first()
    if not demand:
        return {"demand": None, "matches": [], "total": 0}

    # 第一层：SQL筛选
    query = db.query(MainlandSupply)
    if subject_type:
        query = query.filter(MainlandSupply.subject_type == subject_type)
    candidates = query.all()

    if not candidates:
        return {"demand": _demand_to_dict(demand), "matches": [], "total": 0,
                "filter_info": {"candidate_count": 0, "subject_type": subject_type}}

    # 第二层：关键词匹配
    query_text = _build_demand_text(demand)
    query_keywords = _extract_keywords(query_text)

    scored = []
    for supply in candidates:
        supply_text = _build_supply_text(supply)
        kw_score = _keyword_score(query_keywords, supply_text)

        # 标签匹配加权
        tag_score = 0.0
        if demand.supply_tags and supply.border_fit:
            demand_tags = [t.strip() for t in re.split(r"[/、，,;；]+", demand.supply_tags) if t.strip()]
            for tag in demand_tags:
                if tag in supply.border_fit:
                    tag_score += 3.0

        total = kw_score + tag_score
        if total > 0:
            scored.append({
                "supply": _supply_to_dict(supply),
                "score": round(total, 2),
                "keyword_score": round(kw_score, 2),
                "tag_score": round(tag_score, 2),
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return {
        "demand": _demand_to_dict(demand),
        "matches": scored[:top_k],
        "total": len(scored),
        "filter_info": {"candidate_count": len(candidates), "subject_type": subject_type,
                        "matched_count": len(scored)},
    }


def match_demands_for_supply(db: Session, supply_id: str, top_k: int = 5, province: str | None = None) -> dict:
    """为内地供给方匹配边疆需求"""
    supply = db.query(MainlandSupply).filter(MainlandSupply.supply_id == supply_id).first()
    if not supply:
        return {"supply": None, "matches": [], "total": 0}

    # 第一层：SQL筛选
    query = db.query(BorderDemand)
    if province:
        query = query.filter(BorderDemand.province == province)
    candidates = query.all()

    if not candidates:
        return {"supply": _supply_to_dict(supply), "matches": [], "total": 0,
                "filter_info": {"candidate_count": 0, "province": province}}

    # 第二层：关键词匹配
    query_text = _build_supply_text(supply)
    query_keywords = _extract_keywords(query_text)

    scored = []
    for demand in candidates:
        demand_text = _build_demand_text(demand)
        kw_score = _keyword_score(query_keywords, demand_text)

        tag_score = 0.0
        if supply.border_fit and demand.supply_tags:
            supply_tags = [t.strip() for t in re.split(r"[/、，,;；]+", supply.border_fit) if t.strip()]
            for tag in supply_tags:
                if tag in demand.supply_tags:
                    tag_score += 3.0

        total = kw_score + tag_score
        if total > 0:
            scored.append({
                "demand": _demand_to_dict(demand),
                "score": round(total, 2),
                "keyword_score": round(kw_score, 2),
                "tag_score": round(tag_score, 2),
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return {
        "supply": _supply_to_dict(supply),
        "matches": scored[:top_k],
        "total": len(scored),
        "filter_info": {"candidate_count": len(candidates), "province": province,
                        "matched_count": len(scored)},
    }
