"""
智能匹配服务 MVP
第一层：SQL硬性筛选（地域、主体类型）
第二层：关键词检索（文本分词匹配 + 标签匹配加权）
"""
import json
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


VEC_W = 12  # 向量相似度权重（余弦0~1，与标签同量级）

# ============================================================
# 以下为 v2 增强：三因子动态可信度 / 人才库跨类型统一排序 /
# DeepSeek 大模型研判(L3) / 历史范式参考
# ============================================================
import json as _json
from datetime import datetime

from app.models.achievement import CompletedAchievement
from app.models.embedding import ResourceEmbedding
from app.models.talent import SduTalent
from app.services.llm_service import call_llm_json
from app.services.embedding_service import cosine


def _source_weight(source_level: str | None) -> float:
    """因子一：来源权重（依据渠道可靠程度）"""
    s = source_level or ""
    if "高校" in s or "科研机构" in s:
        return 0.9
    if "中央" in s:
        return 0.9 if "一手" in s else 0.85
    if "政府官网" in s:
        return 0.8
    if "企业官网" in s:
        return 0.65
    if "媒体" in s:
        return 0.6
    return 0.5


def _timeliness(date_str: str | None) -> float:
    """因子二：时效分（信息新鲜度，半年1.0/一年0.7/更早0.4）"""
    if not date_str:
        return 0.4
    m = re.search(r"(20\d{2})", date_str)
    if not m:
        return 0.4
    try:
        year = int(m.group(1))
        now_year = datetime.now().year
        months = (now_year - year) * 12
        if months <= 6:
            return 1.0
        if months <= 12:
            return 0.7
        return 0.4
    except ValueError:
        return 0.4


def _verify_factor(verification_status: str | None) -> float:
    """因子三：核验分（默认资源入库前已初筛，中性0.6起步）"""
    s = verification_status or ""
    if "已核验" in s:
        return 1.0
    if "待核验" in s or "弱" in s:
        return 0.4
    return 0.6


def credibility(source_level: str | None, publish_date: str | None,
                verification_status: str | None,
                missing_timeliness: float = 0.4) -> dict:
    """三因子动态可信度合成：可信度 = 0.4×来源 + 0.3×时效 + 0.3×核验

    missing_timeliness：无发布日期时的时效替代值。
    企业/机构类资源无日期默认 0.4（偏旧保守）；高校科研团队无"发布日期"
    不代表过时，调用方应传 0.6 中性值，避免人才库被系统性压分。
    """
    src = _source_weight(source_level)
    tim = _timeliness(publish_date) if publish_date else missing_timeliness
    ver = _verify_factor(verification_status)
    score = round(0.4 * src + 0.3 * tim + 0.3 * ver, 3)
    return {"credibility": score, "source_weight": src,
            "timeliness": tim, "verification": ver}


def _talent_to_dict(t: SduTalent) -> dict:
    """山大人才转候选结构，字段与供给对齐以实现跨类型统一排序"""
    return {
        "supply_id": f"TAL-{t.id:03d}",
        "provider": f"{t.team}（{t.leader}）" if t.leader else t.team,
        "location": "山东·济南",
        "subject_type": "高校科研",
        "services": t.west_scene,
        "tech_advantages": t.core_tech,
        "use_cases": t.cases,
        "border_fit": "；".join(x for x in [t.west_scene, t.application] if x),
        "delivery_mode": t.maturity,
        "contact": f"{t.org} {t.source_url or ''}".strip()[:200],
        "source_url": t.source_url,
        "candidate_type": "talent",       # 山大人才
        "_extra": {"domain": t.domain, "field": t.field,
                   "patents": t.patents, "awards": t.awards},
    }


JUDGE_PROMPT = """你是东西部协作供需匹配研判引擎。

需求信息：
{demand}

候选资源：
{candidates}

对每个候选评估匹配度，输出 JSON 数组：
[{{"index":1,"match_score":0到100整数,"match_reason":"具体匹配点（引用需求痛点与资源实际能力）","risk":"潜在风险或'无明显风险'","suggestion":"对接建议"}}]

规则：
1. 完全匹配90+，部分匹配60-89，弱相关40-59；
2. match_reason 必须引用双方实际内容，不得空泛；
3. 按 match_score 降序输出全部候选。
只输出 JSON 数组。"""


def judge_with_llm(demand_dict: dict, candidates: list[dict],
                   top_n: int = 8) -> tuple[list[dict], str]:
    """第三级漏斗：DeepSeek 研判排序（成功返回 LLM 结果，失败回退原序并标记 rule 模式）"""
    if not candidates:
        return candidates, "empty"
    top = candidates[:top_n]
    cand_text = "\n".join(
        f"[{i+1}] {c.get('candidate_type','enterprise')} | {c.get('provider','')} | "
        f"服务: {str(c.get('services',''))[:120]} | 技术: {str(c.get('tech_advantages',''))[:100]} "
        f"| 边疆适配: {str(c.get('border_fit',''))[:80]}"
        for i, c in enumerate(top))
    demand_text = _json.dumps(demand_dict, ensure_ascii=False)
    result = call_llm_json([{"role": "user", "content": JUDGE_PROMPT.format(
        demand=demand_text, candidates=cand_text)}], temperature=0.2)
    if isinstance(result, list) and result:
        for j in result:
            idx = int(j.get("index", 0)) - 1
            if 0 <= idx < len(top):
                top[idx]["llm_match_score"] = j.get("match_score")
                top[idx]["llm_match_reason"] = j.get("match_reason")
                top[idx]["llm_risk"] = j.get("risk")
                top[idx]["llm_suggestion"] = j.get("suggestion")
        # 最终得分 = 0.7×LLM评分 + 0.3×规则分（归一）；LLM 漏评的候选用规则分兜底
        max_orig = max((c["score"] for c in top), default=1) or 1
        for c in top:
            orig_norm = c["score"] / max_orig * 100
            llm_s = c.get("llm_match_score")
            if llm_s is not None:
                try:
                    c["final_score"] = round(0.7 * float(llm_s) + 0.3 * orig_norm, 1)
                except (TypeError, ValueError):
                    c["final_score"] = round(orig_norm, 1)
            else:
                c["final_score"] = round(orig_norm, 1)
            c["judge_mode"] = "llm"
        top.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        return top, "llm"
    for c in top:
        c["judge_mode"] = "rule"
        c["final_score"] = c["score"]
    return top, "rule"


def find_reference_achievements(db: Session, demand: BorderDemand,
                                top_n: int = 3) -> list[dict]:
    """历史范式参考：从已完成成果库检索相似协作案例（含可复制协作点）"""
    query_text = _build_demand_text(demand)
    keywords = [w for w in _extract_keywords(query_text)] + \
               ([t.strip() for t in re.split(r"[/、，,;；]+", demand.supply_tags or "") if t.strip()])
    scored = []
    for ach in db.query(CompletedAchievement).all():
        text = " ".join(filter(None, [ach.title, ach.highlights, ach.work_done,
                                      ach.replicable_points]))
        score = _keyword_score(keywords, text)
        if score > 0:
            scored.append({
                "achievement_id": ach.achievement_id,
                "title": ach.title,
                "region": ach.region,
                "highlights": (ach.highlights or "")[:200],
                "replicable_points": ach.replicable_points,
                "reference_score": round(score, 2),
            })
    scored.sort(key=lambda x: x["reference_score"], reverse=True)
    return scored[:top_n]


def match_all_for_demand(db: Session, demand_id: str, top_k: int = 8,
                         use_llm: bool = True, subject_type: str | None = None) -> dict:
    """三级漏斗完整匹配（跨类型统一排序版）

    第一级：SQL 全量载入内地供给 + 山大人才（硬字段可扩展过滤）
    第二级：关键词打分 + 标签匹配加权 × 三因子动态可信度 → 排序取 Top-K
    第三级：DeepSeek 大模型研判（评分+理由+风险+建议），失败自动降级规则模式
    附：历史范式参考（已完成成果的可复制协作点）
    """
    demand = db.query(BorderDemand).filter(BorderDemand.demand_id == demand_id).first()
    if not demand:
        return {"demand": None, "matches": [], "total": 0}

    # --- 向量索引装载（无向量时自动降级为纯关键词+标签）---
    emb_map = {}
    for e in db.query(ResourceEmbedding).all():
        try:
            emb_map[(e.source_type, e.source_id)] = json.loads(e.embedding)
        except json.JSONDecodeError:
            continue
    demand_vec = emb_map.get(('demand', demand.demand_id))

    def _vec_sim(source_type: str, source_id: str) -> float:
        if not demand_vec:
            return 0.0
        v = emb_map.get((source_type, source_id))
        return cosine(demand_vec, v) if v else 0.0

    # --- 第一级 ---
    supplies = db.query(MainlandSupply).all()
    talents = db.query(SduTalent).all()
    l1_count = len(supplies) + len(talents)

    # --- 第二级 ---
    query_keywords = _extract_keywords(_build_demand_text(demand)) + \
                     ([t.strip() for t in re.split(r"[/、，,;；]+", demand.supply_tags or "") if t.strip()])

    scored = []
    for supply in supplies:
        text = _build_supply_text(supply)
        kw = _keyword_score(query_keywords, text)
        tag = 0.0
        if demand.supply_tags and supply.border_fit:
            for t in [x.strip() for x in re.split(r"[/、，,;；]+", demand.supply_tags) if x.strip()]:
                if t in supply.border_fit:
                    tag += 3.0
        base = kw + tag + VEC_W * _vec_sim('supply', supply.supply_id)
        cred = credibility(supply.source_level, supply.publish_date, supply.verification_status)
        if base > 0:
            d = _supply_to_dict(supply)
            d.update({"candidate_type": "enterprise", "score": round(base * cred["credibility"], 2),
                      "keyword_score": round(kw, 2), "tag_score": round(tag, 2), **cred})
            scored.append(d)
    for talent in talents:
        td = _talent_to_dict(talent)
        text = " ".join(filter(None, [td["services"], td["tech_advantages"],
                                      td["border_fit"], td["_extra"]["field"]]))
        kw = _keyword_score(query_keywords, text)
        tag = 0.0
        if demand.supply_tags and td["border_fit"]:
            for t in [x.strip() for x in re.split(r"[/、，,;；]+", demand.supply_tags) if x.strip()]:
                if t in td["border_fit"]:
                    tag += 3.0
        base = kw + tag + VEC_W * _vec_sim('talent', f"TAL-{talent.id:03d}")
        cred = credibility(talent.source_note and "高校/科研机构官网" or "",
                           "", "已核验", missing_timeliness=0.6)
        if base > 0:
            td.update({"score": round(base * cred["credibility"], 2),
                       "keyword_score": round(kw, 2), "tag_score": round(tag, 2), **cred})
            scored.append(td)

    if subject_type:
        scored = [s for s in scored if s.get("subject_type") == subject_type]
    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:top_k]
    l2_count = len(scored)

    # --- 第三级 ---
    demand_dict = _demand_to_dict(demand)
    if use_llm:
        top, judge_mode = judge_with_llm(demand_dict, top)
    else:
        for c in top:
            c["judge_mode"] = "off"
            c["final_score"] = c["score"]
        judge_mode = "off"

    references = find_reference_achievements(db, demand) if use_llm else []

    return {
        "demand": demand_dict,
        "matches": top,
        "total": len(scored),
        "filter_info": {"level1_candidates": l1_count, "level2_matched": l2_count,
                        "returned": len(top), "judge_mode": judge_mode},
        "history_reference": references,
    }
