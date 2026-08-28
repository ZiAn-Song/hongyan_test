import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine
from app.models.user import User
from app.models.company import Company
from app.models.team import Team, TeamMember
from app.models.demand import Demand
from app.models.forum import ForumPost, ForumComment
from app.models.document import DocumentChunk
from app.utils.security import get_password_hash

DATA_DIR = Path(__file__).resolve().parent.parent / "鸿雁" / "data"


def clear_all(db):
    db.query(DocumentChunk).delete()
    db.query(ForumComment).delete()
    db.query(ForumPost).delete()
    db.query(TeamMember).delete()
    db.query(Team).delete()
    db.query(Demand).delete()
    db.query(Company).delete()
    db.query(User).delete()
    db.commit()


def migrate_users(db):
    filepath = DATA_DIR / "Personal_Information.json"
    if not filepath.exists():
        print("  [SKIP] Personal_Information.json not found")
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for record in data.get("users", []):
        student_id = record.get("studentId", "").strip()
        if not student_id:
            continue

        existing = db.query(User).filter(User.student_id == student_id).first()
        if existing:
            continue

        gender = "男" if record.get("gender") else "女"

        user = User(
            student_id=student_id,
            full_name=record.get("fullName", ""),
            password_hash=get_password_hash(record.get("password", "123456")),
            gender=gender,
            university=record.get("university", ""),
            contact=record.get("contact", ""),
            email=record.get("email", "") or None,
            major=record.get("major", "") or None,
        )
        db.add(user)
        count += 1

    db.commit()
    return count


def migrate_companies(db):
    filepath = DATA_DIR / "Company_Information.json"
    if not filepath.exists():
        print("  [SKIP] Company_Information.json not found")
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for record in data.get("Company", []):
        org_name = record.get("Company_Name", "").strip()
        if not org_name:
            continue

        company = Company(
            org_name=org_name,
            org_type="政府机构",
            admin_location=record.get("Location", ""),
            admin_code=record.get("Code", ""),
            org_email=record.get("Email", "") or None,
            contact_person="",
            contact_phone=record.get("Contact_Information", ""),
            password_hash=get_password_hash(record.get("password", "123456")),
            org_profile=record.get("Company_Profile", ""),
        )
        db.add(company)
        count += 1

    db.commit()
    return count


def migrate_demands(db):
    filepath = DATA_DIR / "Corporate_Announcement.json"
    if not filepath.exists():
        print("  [SKIP] Corporate_Announcement.json not found")
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for record in data.get("Demand", []):
        company_name = record.get("Company_Name", "")
        company = db.query(Company).filter(Company.org_name == company_name).first()

        demand = Demand(
            company_id=company.id if company else None,
            company_name=company_name,
            internship_location=record.get("Internship_Location", ""),
            estimated_time=record.get("Estimated_Time", ""),
            requirements_content=record.get("Requirements_Content", ""),
            target_majors=record.get("Target_Major", []),
            org_type=record.get("orgType", ""),
            org_name=record.get("orgName", ""),
            contact_info=record.get("contactInfo", ""),
        )
        db.add(demand)
        count += 1

    db.commit()
    return count


def migrate_teams(db):
    filepath = DATA_DIR / "Team_Announcement.json"
    if not filepath.exists():
        print("  [SKIP] Team_Announcement.json not found")
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    team_count = 0
    member_count = 0

    for record in data.get("TEAM", []):
        team_name = record.get("teamName", "").strip()
        if not team_name:
            continue

        team = Team(
            team_name=team_name,
            leader_name=record.get("leaderName", ""),
            leader_contact=record.get("leaderContact", ""),
            leader_email=record.get("leaderEmail", ""),
            student_id=record.get("studentId", ""),
            university=record.get("university", ""),
            team_specialty=record.get("teamSpecialty", ""),
            team_description=record.get("teamDescription", ""),
            teacher_name=record.get("teacherName", ""),
            teacher_contact=record.get("teacherContact", ""),
        )
        db.add(team)
        db.flush()

        for i, member_name in enumerate(record.get("memberNames", [])):
            member = TeamMember(
                team_id=team.id,
                member_name=member_name,
                role="leader" if i == 0 else "member",
            )
            db.add(member)
            member_count += 1

        team_count += 1

    db.commit()
    return team_count, member_count


def main():
    print("=" * 50)
    print("鸿雁平台 - 数据迁移脚本")
    print("=" * 50)

    db = SessionLocal()

    print("\n[0] 清除现有数据...")
    clear_all(db)
    print("  Done")

    print("\n[1] 迁移个人用户 (Personal_Information.json)...")
    user_count = migrate_users(db)
    print(f"  Migrated: {user_count} users")

    print("\n[2] 迁移政企用户 (Company_Information.json)...")
    company_count = migrate_companies(db)
    print(f"  Migrated: {company_count} companies")

    print("\n[3] 迁移需求公告 (Corporate_Announcement.json)...")
    demand_count = migrate_demands(db)
    print(f"  Migrated: {demand_count} demands")

    print("\n[4] 迁移团队 (Team_Announcement.json)...")
    team_count, member_count = migrate_teams(db)
    print(f"  Migrated: {team_count} teams, {member_count} members")

    print("\n[5] 验证数据完整性...")
    print(f"  Users:    {db.query(User).count()}")
    print(f"  Companies: {db.query(Company).count()}")
    print(f"  Demands:  {db.query(Demand).count()}")
    print(f"  Teams:    {db.query(Team).count()}")
    print(f"  Members:  {db.query(TeamMember).count()}")

    db.close()
    print("\n" + "=" * 50)
    print("Data migration completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
