from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from ..database import SessionLocal
from ..models.user import User
from .. import schemas
from ..utils import verify_password
from ..config import settings

# Схема безопасности
security = HTTPBearer()

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


def authenticate_user(db, username: str, password: str):
    """Аутентифицирует пользователя по имени и паролю"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создает JWT токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(security)):
    """Получает текущего пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if username is None or user_id is None or role is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id, role=role)
    except JWTError:
        raise credentials_exception
    
    # Здесь нужно получить пользователя из базы данных
    # db = SessionLocal()
    # try:
    #     user = db.query(User).filter(User.id == token_data.user_id).first()
    #     if user is None:
    #         raise credentials_exception
    #     return user
    # finally:
    #     db.close()
    
    # Для упрощения возвращаем только данные токена
    return token_data


async def get_current_active_user(current_user: TokenData = Depends(get_current_user)):
    """Проверяет, активен ли пользователь"""
    # В продакшене нужно проверить, активен ли пользователь в базе
    return current_user