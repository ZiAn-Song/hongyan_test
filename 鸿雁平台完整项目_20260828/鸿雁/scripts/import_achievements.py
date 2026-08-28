import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database import SessionLocal, Base, engine
from app.models.achievement import BorderDemand, MainlandSupply


def import_border_demands(db, data):
    count = 0
    for item in data:
        if db.query(BorderDemand).filter_by(demand_id=item["需求ID"]).first():
            continue
        db.add(BorderDemand(
            demand_id=item["需求ID"],
            title=item["需求标题"],
            province=item.get("省/自治区"),
            coverage=item.get("覆盖口径"),
            location_detail=item.get("地市/边境县/乡镇"),
            publisher=item.get("需求发布方"),
            pain_point=item.get("痛点/现状"),
            description=item.get("具体需求描述"),
            expected_goal=item.get("预期目标及合作方式"),
            stage=item.get("需求阶段"),
            supply_tags=item.get("适配供给标签"),
            contact=item.get("发布方官网/联系方式"),
            source_level=item.get("来源层级"),
            publish_date=item.get("发布日期"),
            source_url=item.get("原文链接"),
            verification_status=item.get("核验状态"),
        ))
        count += 1
    db.commit()
    return count


def import_mainland_supplies(db, data):
    count = 0
    for item in data:
        if db.query(MainlandSupply).filter_by(supply_id=item["供给ID"]).first():
            continue
        db.add(MainlandSupply(
            supply_id=item["供给ID"],
            provider=item["提供方"],
            location=item.get("所在地"),
            subject_type=item.get("主体类型"),
            services=item.get("可提供服务"),
            tech_advantages=item.get("核心技术优势"),
            use_cases=item.get("应用场景与案例"),
            border_fit=item.get("适配边疆需求"),
            delivery_mode=item.get("合作交付方式"),
            contact=item.get("联系方式"),
            source_level=item.get("来源层级"),
            publish_date=item.get("发布/更新日期"),
            source_url=item.get("官网/案例链接"),
            verification_status=item.get("核验状态"),
        ))
        count += 1
    db.commit()
    return count


def main():
    json_path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "..", "frontend", "public", "data", "achievements.json"
    ))
    print(f"读取: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        bd = import_border_demands(db, data.get("border_demands", []))
        ms = import_mainland_supplies(db, data.get("mainland_supply", []))
        print(f"边疆需求新增 {bd} 条，内地供给新增 {ms} 条")
        print(f"总计: 边疆需求 {db.query(BorderDemand).count()} 条，内地供给 {db.query(MainlandSupply).count()} 条")
    finally:
        db.close()


if __name__ == "__main__":
    main()
