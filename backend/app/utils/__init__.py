from passlib.context import CryptContext

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Возвращает хеш для пароля"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли введенный пароль хешированному паролю"""
    return pwd_context.verify(plain_password, hashed_password)


# Импортируем модули
from .zone_calculator import calculate_zone_boundaries, determine_zone

__all__ = [
    "get_password_hash",
    "verify_password",
    "calculate_zone_boundaries",
    "determine_zone"
]