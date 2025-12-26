from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables

# Инициализация FastAPI приложения
app = FastAPI(
    title="Пикфлоуметр API",
    description="API для медицинского трекера пикфлоу у детей",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц при запуске приложения
@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
async def root():
    return {"message": "Пикфлоуметр API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Подключение роутов
from app.auth.router import router as auth_router
from app.api.users import router as users_router
from app.api.measurements import router as measurements_router
from app.api.zones import router as zones_router
from app.api.reminders import router as reminders_router
from app.api.telegram import router as telegram_router

app.include_router(auth_router, prefix="/api", tags=["authentication"])
app.include_router(users_router, prefix="/api", tags=["users"])
app.include_router(measurements_router, prefix="/api", tags=["measurements"])
app.include_router(zones_router, prefix="/api", tags=["zones"])
app.include_router(reminders_router, prefix="/api", tags=["reminders"])
app.include_router(telegram_router)