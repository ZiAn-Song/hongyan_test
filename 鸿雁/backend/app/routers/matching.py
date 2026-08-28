from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.matching_service import match_supplies_for_demand, match_demands_for_supply

router = APIRouter()


@router.get("/demands/{demand_id}/supplies")
def get_matching_supplies(
    demand_id: str,
    top_k: int = Query(5, ge=1, le=20),
    subject_type: str | None = Query(None, description="按主体类型筛选"),
    db: Session = Depends(get_db),
):
    result = match_supplies_for_demand(db, demand_id, top_k=top_k, subject_type=subject_type)
    if not result["demand"]:
        raise HTTPException(status_code=404, detail=f"需求 {demand_id} 不存在")
    return result


@router.get("/supplies/{supply_id}/demands")
def get_matching_demands(
    supply_id: str,
    top_k: int = Query(5, ge=1, le=20),
    province: str | None = Query(None, description="按省份筛选"),
    db: Session = Depends(get_db),
):
    result = match_demands_for_supply(db, supply_id, top_k=top_k, province=province)
    if not result["supply"]:
        raise HTTPException(status_code=404, detail=f"供给 {supply_id} 不存在")
    return result


# ================= v2：三级漏斗完整匹配（跨类型统一排序 + DeepSeek 研判）=================
from fastapi import Query as FQuery

from app.services.matching_service import match_all_for_demand


@router.get("/v2/demands/{demand_id}/match")
def match_v2(
    demand_id: str,
    top_k: int = FQuery(8, ge=1, le=20),
    use_llm: bool = FQuery(True, description="是否启用 DeepSeek 第三级研判"),
    subject_type: str | None = FQuery(None, description="按主体类型筛选"),
    db: Session = Depends(get_db),
):
    """三级漏斗智能匹配（跨类型统一排序）

    第一级：SQL 载入内地供给 + 山大人才
    第二级：关键词+标签加权 × 三因子动态可信度
    第三级：DeepSeek 研判（评分/理由/风险/建议），失败自动降级规则模式
    附：历史范式参考（已完成成果可复制协作点）
    """
    result = match_all_for_demand(db, demand_id, top_k=top_k, use_llm=use_llm,
                                  subject_type=subject_type)
    if not result["demand"]:
        raise HTTPException(status_code=404, detail=f"需求 {demand_id} 不存在")
    return result
