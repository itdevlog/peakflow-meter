"""
API для обработки вебхуков от Telegram
"""
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
import hashlib
import hmac
import logging
from typing import Dict, Any
from telegram.ext import Application
import asyncio

from ..telegram_bot import create_telegram_bot

router = APIRouter(prefix="/telegram", tags=["telegram"])

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальная переменная для хранения бота
telegram_bot = create_telegram_bot()

@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Обработка вебхука от Telegram
    """
    try:
        # Получаем JSON-данные из запроса
        update_data = await request.json()
        
        # В реальной системе нужно проверить подпись вебхука
        # для обеспечения безопасности
        
        # Передаем обновление в приложение Telegram
        if telegram_bot and telegram_bot.application:
            # Создаем задачу для обработки обновления
            task = asyncio.create_task(
                telegram_bot.application.update_queue.put(update_data)
            )
            await task
            
            return JSONResponse(
                content={"status": "ok", "message": "Update received"},
                status_code=status.HTTP_200_OK
            )
        else:
            logger.error("Telegram bot is not initialized")
            return JSONResponse(
                content={"status": "error", "message": "Bot not initialized"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/set-webhook")
async def set_webhook():
    """
    Установка вебхука для Telegram бота
    """
    if not telegram_bot or not telegram_bot.application:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Telegram bot is not initialized"
        )
    
    try:
        # В реальной системе здесь нужно указать URL для вебхука
        # webhook_url = "https://yourdomain.com/api/telegram/webhook"
        # await telegram_bot.application.bot.set_webhook(webhook_url)
        
        # Для локальной разработки используем polling
        return JSONResponse(
            content={
                "status": "ok", 
                "message": "Webhook setup initiated (using polling in development)"
            },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set webhook"
        )


@router.get("/bot-info")
async def get_bot_info():
    """
    Получение информации о боте
    """
    if not telegram_bot or not telegram_bot.application:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Telegram bot is not initialized"
        )
    
    try:
        bot_info = await telegram_bot.application.bot.get_me()
        return {
            "id": bot_info.id,
            "username": bot_info.username,
            "first_name": bot_info.first_name,
            "is_bot": bot_info.is_bot
        }
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get bot info"
        )