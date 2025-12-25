"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Настройки базы данных
    database_url: str = "postgresql+asyncpg://user:password@localhost/peakflow_db"
    
    # Настройки безопасности
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f709f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Настройки Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Настройки Telegram
    telegram_bot_token: Optional[str] = None
    
    # Режим отладки
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()