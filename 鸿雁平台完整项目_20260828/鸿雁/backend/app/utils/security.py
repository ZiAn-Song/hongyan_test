import bcrypt
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import settings


def _truncate(password: str) -> bytes:
    encoded = password.encode("utf-8")
    return encoded[:72] if len(encoded) > 72 else encoded


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_truncate(plain_password), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(_truncate(password), bcrypt.gensalt()).decode("utf-8")


def create_access_token(subject: str, extra_data: dict | None = None) -> str:
    to_encode = {"sub": subject}
    if extra_data:
        to_encode.update(extra_data)

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
