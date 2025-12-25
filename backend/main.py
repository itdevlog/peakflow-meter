from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Пикфлоуметр API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Подключение роутов
from app.auth import router as auth_router
from app.api import users, measurements, zones, reminders
from app.api.telegram import router as telegram_router

app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(measurements.router, prefix="/api/measurements", tags=["measurements"])
app.include_router(zones.router, prefix="/api/zones", tags=["zones"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(telegram_router)