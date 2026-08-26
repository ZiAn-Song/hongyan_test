from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    PersonalRegisterRequest,
    EnterpriseRegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    CompanyResponse,
)
from app.services.auth_service import (
    register_personal,
    register_enterprise,
    login,
    admin_login,
    student_login,
    enterprise_login,
)
from app.utils.dependencies import get_current_user, CurrentUser

router = APIRouter()


@router.post("/register/personal", response_model=UserResponse, status_code=201)
def register_personal_api(
    data: PersonalRegisterRequest,
    db: Session = Depends(get_db),
):
    return register_personal(db, data)


@router.post("/register/enterprise", response_model=CompanyResponse, status_code=201)
def register_enterprise_api(
    data: EnterpriseRegisterRequest,
    db: Session = Depends(get_db),
):
    return register_enterprise(db, data)


@router.post("/login", response_model=TokenResponse)
def login_api(data: LoginRequest, db: Session = Depends(get_db)):
    return login(db, data)


@router.post("/admin-login", response_model=TokenResponse)
def admin_login_api(db: Session = Depends(get_db)):
    return admin_login(db)


@router.post("/student-login", response_model=TokenResponse)
def student_login_api(db: Session = Depends(get_db)):
    return student_login(db)


@router.post("/enterprise-login", response_model=TokenResponse)
def enterprise_login_api(db: Session = Depends(get_db)):
    return enterprise_login(db)


@router.get("/me")
def get_me(current_user: CurrentUser = Depends(get_current_user)):
    return current_user
