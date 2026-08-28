from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class CurrentUser(BaseModel):
    id: int
    user_type: str
    name: str | None = None
    role: str | None = None


def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        user_type = payload.get("type")
        name = payload.get("name")
        role = payload.get("role")
        if user_id is None or user_type is None:
            raise credentials_exception
        return CurrentUser(id=int(user_id), user_type=user_type, name=name, role=role)
    except (JWTError, ValueError):
        raise credentials_exception


def require_admin(
    current: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    if not current.role or current.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此操作需要管理员权限",
        )
    return current


def get_current_personal_user(
    current: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    if current.user_type != "personal":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此操作需要个人用户权限",
        )
    return current


def get_current_enterprise_user(
    current: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    if current.user_type != "enterprise":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此操作需要政企用户权限",
        )
    return current
