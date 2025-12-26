from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Для синхронной работы с PostgreSQL - заменяем asyncpg на psycopg2
sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")

engine = create_engine(
    sync_db_url,
    echo=True  # Установите в False в продакшене
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """Создание таблиц в базе данных"""
    # Импортируем модели чтобы они были зарегистрированы в Base
    from . import models
    Base.metadata.create_all(bind=engine)

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()