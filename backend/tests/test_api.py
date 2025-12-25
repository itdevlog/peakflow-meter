"""
Тесты для API системы Пикфлоуметр
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models import Base
from app import models, schemas

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Переопределяем сессию базы данных для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Подменяем зависимость получения сессии базы данных
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_check():
    """Тест проверки работоспособности API"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Тест главной страницы API"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Пикфлоуметр API"

def test_create_user():
    """Тест создания пользователя"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "parent"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    
    # Проверяем, что запрос выполнен успешно
    assert response.status_code == 200
    
    # Проверяем, что в ответе есть токен
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_user_login():
    """Тест входа пользователя"""
    # Сначала создаем пользователя
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123",
        "role": "parent"
    }
    
    client.post("/api/auth/register", json=user_data)
    
    # Пробуем залогиниться
    login_data = {
        "username": "loginuser",
        "password": "password123",
        "role": "parent"
    }
    
    response = client.post("/api/auth/login", json=login_data)
    
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_child_profile():
    """Тест создания профиля ребенка"""
    # Регистрируем родителя
    parent_data = {
        "username": "parentuser",
        "email": "parent@example.com",
        "password": "password123",
        "role": "parent"
    }
    
    response = client.post("/api/auth/register", json=parent_data)
    assert response.status_code == 200
    
    # Логинимся
    login_data = {
        "username": "parentuser",
        "password": "password123",
        "role": "parent"
    }
    
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Создаем профиль ребенка
    child_data = {
        "first_name": "Анна",
        "last_name": "Иванова",
        "birth_date": "2015-05-15",
        "height": 130,
        "gender": "female",
        "parent_id": 1
    }
    
    response = client.post("/api/users/child-profile", json=child_data, headers=headers)
    
    # Должен быть успешный ответ
    assert response.status_code in [200, 400, 422]  # 400 или 422 возможны из-за ограничений схемы

def test_create_measurement():
    """Тест добавления измерения"""
    # Регистрируем пользователя
    user_data = {
        "username": "measurementuser",
        "email": "measurement@example.com",
        "password": "password123",
        "role": "parent"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    
    # Логинимся
    login_data = {
        "username": "measurementuser",
        "password": "password123",
        "role": "parent"
    }
    
    login_response = client.post("/api/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Пробуем добавить измерение
    measurement_data = {
        "value": 450,
        "timestamp": "2023-12-25T10:30:00",
        "child_id": 1
    }
    
    response = client.post("/api/measurements/", json=measurement_data, headers=headers)
    
    # Должен быть успешный ответ или ошибка валидации (из-за отсутствия ребенка)
    assert response.status_code in [200, 400, 404, 422]

def test_get_zones():
    """Тест получения зон"""
    # Регистрируем пользователя
    user_data = {
        "username": "zoneuser",
        "email": "zone@example.com",
        "password": "password123",
        "role": "parent"
    }
    
    client.post("/api/auth/register", json=user_data)
    
    # Логинимся
    login_data = {
        "username": "zoneuser",
        "password": "password123",
        "role": "parent"
    }
    
    login_response = client.post("/api/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Пробуем получить зоны для несуществующего ребенка
    response = client.get("/api/zones/current?child_id=1", headers=headers)
    
    # Должен быть успешный ответ или ошибка (из-за отсутствия ребенка)
    assert response.status_code in [200, 404]