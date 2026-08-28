#!/usr/bin/env python3
"""批量构建资源向量索引（L2 语义召回底座）

前置：.env 里 EMBEDDING_API_KEY 填入火山方舟 ARK_API_KEY
用法（backend/ 下执行）: python scripts/build_embeddings.py
幂等：同一 source 已有同模型向量则跳过；文本变化时重建。
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from app.config import settings
from app.database import SessionLocal
from app.models import BorderDemand, MainlandSupply, SduTalent, ResourceEmbedding
from app.services.embedding_service import (
    build_resource_text_demand, build_resource_text_supply,
    build_resource_text_talent, embed_text)


def digest(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def upsert(db, source_type: str, source_id: str, text: str) -> bool:
    dg = digest(text)
    exists = db.query(ResourceEmbedding).filter(
        ResourceEmbedding.source_type == source_type,
        ResourceEmbedding.source_id == source_id).first()
    if exists and exists.content_digest == dg and exists.model == settings.EMBEDDING_MODEL:
        return False  # 未变化，跳过
    vec = embed_text(text)
    if not vec:
        return False
    if exists:
        exists.embedding = json.dumps(vec)
        exists.model = settings.EMBEDDING_MODEL
        exists.content_digest = dg
    else:
        db.add(ResourceEmbedding(source_type=source_type, source_id=source_id,
                                 model=settings.EMBEDDING_MODEL,
                                 embedding=json.dumps(vec), content_digest=dg))
    return True


def main():
    if not settings.EMBEDDING_API_KEY or settings.EMBEDDING_API_KEY.startswith("填入"):
        print("错误：.env 中 EMBEDDING_API_KEY 未配置（填入火山方舟 ARK_API_KEY）")
        sys.exit(1)
    db = SessionLocal()
    n_new = n_skip = n_fail = 0

    for d in db.query(BorderDemand).all():
        if upsert(db, "demand", d.demand_id, build_resource_text_demand(d)):
            n_new += 1
        else:
            n_skip += 1
        db.commit()

    for s in db.query(MainlandSupply).all():
        if upsert(db, "supply", s.supply_id, build_resource_text_supply(s)):
            n_new += 1
        else:
            n_skip += 1
        db.commit()

    for t in db.query(SduTalent).all():
        tid = f"TAL-{t.id:03d}"
        if upsert(db, "talent", tid, build_resource_text_talent(t)):
            n_new += 1
        else:
            n_skip += 1
        db.commit()

    total = db.query(ResourceEmbedding).count()
    print(f'向量构建完成：新增 {n_new} | 未变化+失败 {n_skip} | 库内共 {total} 条向量')
    db.close()


if __name__ == "__main__":
    main()
