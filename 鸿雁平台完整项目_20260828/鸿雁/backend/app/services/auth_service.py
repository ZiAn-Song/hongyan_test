from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.company import Company
from app.schemas.auth import (
    PersonalRegisterRequest,
    EnterpriseRegisterRequest,
    LoginRequest,
)
from app.utils.security import get_password_hash, verify_password, create_access_token


def register_personal(db: Session, data: PersonalRegisterRequest) -> User:
    existing = db.query(User).filter(User.student_id == data.student_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该学号已注册",
        )

    user = User(
        student_id=data.student_id,
        full_name=data.full_name,
        password_hash=get_password_hash(data.password),
        role="student",
        gender=data.gender,
        university=data.university,
        contact=data.contact,
        email=data.email,
        major=data.major,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def register_enterprise(db: Session, data: EnterpriseRegisterRequest) -> Company:
    existing = db.query(Company).filter(Company.org_email == data.org_email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已注册",
        )

    company = Company(
        org_name=data.org_name,
        org_type=data.org_type,
        admin_location=data.admin_location,
        admin_code=data.admin_code,
        org_email=data.org_email,
        contact_person=data.contact_person,
        contact_phone=data.contact_phone,
        password_hash=get_password_hash(data.password),
        org_profile=data.org_profile,
        additional_info=data.additional_info,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def login(db: Session, data: LoginRequest) -> dict:
    if data.user_type == "personal":
        user = db.query(User).filter(User.student_id == data.account).first()
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="学号或密码错误",
            )
        role = user.role if user.role else ("admin" if user.student_id == "admin" else "student")
        token = create_access_token(
            subject=str(user.id),
            extra_data={"type": "personal", "name": user.full_name, "role": role},
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_type": "personal",
            "user_id": user.id,
            "name": user.full_name,
            "role": role,
        }

    company = db.query(Company).filter(Company.org_email == data.account).first()
    if not company or not verify_password(data.password, company.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
        )
    token = create_access_token(
        subject=str(company.id),
        extra_data={"type": "enterprise", "name": company.org_name, "role": "enterprise"},
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_type": "enterprise",
        "user_id": company.id,
        "name": company.org_name,
        "role": "enterprise",
    }


def admin_login(db: Session) -> dict:
    """管理员快速登录：自动创建或查找管理员账户，返回 JWT token。"""
    admin = db.query(User).filter(User.student_id == "admin").first()
    if not admin:
        admin = User(
            student_id="admin",
            full_name="管理员",
            password_hash=get_password_hash("admin123456"),
            role="admin",
            university="系统管理员",
            major="管理员",
            contact="00000000000",
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    elif not admin.role or admin.role != "admin":
        admin.role = "admin"
        db.commit()
        db.refresh(admin)

    token = create_access_token(
        subject=str(admin.id),
        extra_data={"type": "personal", "name": admin.full_name, "role": "admin"},
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_type": "personal",
        "user_id": admin.id,
        "name": admin.full_name,
        "role": "admin",
    }


def student_login(db: Session) -> dict:
    """学生快速登录：自动创建或查找学生账户，返回 JWT token。"""
    student = db.query(User).filter(User.student_id == "student").first()
    if not student:
        student = User(
            student_id="student",
            full_name="学生用户",
            password_hash=get_password_hash("student123456"),
            role="student",
            university="测试大学",
            major="测试专业",
            contact="00000000000",
        )
        db.add(student)
        db.commit()
        db.refresh(student)
    elif not student.role or student.role != "student":
        student.role = "student"
        db.commit()
        db.refresh(student)

    token = create_access_token(
        subject=str(student.id),
        extra_data={"type": "personal", "name": student.full_name, "role": "student"},
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_type": "personal",
        "user_id": student.id,
        "name": student.full_name,
        "role": "student",
    }


def enterprise_login(db: Session) -> dict:
    """政企快速登录：自动创建或查找政企账户，返回 JWT token。"""
    company = db.query(Company).filter(Company.org_email == "enterprise@test.com").first()
    if not company:
        company = Company(
            org_name="测试政企单位",
            org_type="企业",
            org_email="enterprise@test.com",
            contact_person="联系人",
            contact_phone="00000000000",
            password_hash=get_password_hash("enterprise123456"),
            org_profile="这是一家测试用的政企单位，用于系统功能验证。" + "x" * 30,
        )
        db.add(company)
        db.commit()
        db.refresh(company)

    token = create_access_token(
        subject=str(company.id),
        extra_data={"type": "enterprise", "name": company.org_name, "role": "enterprise"},
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_type": "enterprise",
        "user_id": company.id,
        "name": company.org_name,
        "role": "enterprise",
    }
