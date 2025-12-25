"""
Модуль для асинхронных задач (Celery)
"""
from celery import Celery
from .config import settings
from .reminder_scheduler import ReminderScheduler
from .utils.notification_sender import NotificationSender
import asyncio

# Настройка Celery
celery_app = Celery('peakflow_meter')

# Настройка брокера (Redis)
celery_app.conf.broker_url = settings.redis_url
celery_app.conf.result_backend = settings.redis_url

# Другие настройки Celery
celery_app.conf.task_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_serializer = 'json'
celery_app.conf.timezone = 'UTC'


@celery_app.task
def send_reminder_notification(reminder_id: int):
    """
    Асинхронная задача для отправки напоминания
    """
    # Вызов асинхронной функции из синхронной задачи Celery
    result = asyncio.run(ReminderScheduler.send_reminder_notification_async(reminder_id))
    return {"status": "success" if result else "failed", "reminder_id": reminder_id}


@celery_app.task
def check_daily_measurements():
    """
    Асинхронная задача для проверки, были ли сделаны измерения за день
    и отправки напоминаний, если они не были выполнены
    """
    result = ReminderScheduler.check_daily_reminders()
    return {"status": "success", "message": "Daily measurements check completed", "task_result": str(result)}


@celery_app.task
def send_telegram_message(chat_id: int, message: str):
    """
    Асинхронная задача для отправки сообщения через Telegram
    """
    # В реальной системе здесь будет код для отправки
    # сообщения через Telegram Bot API
    
    # Асинхронный вызов функции отправки
    result = asyncio.run(NotificationSender.send_telegram_message(chat_id, message))
    
    return {"status": "success" if result else "failed", "chat_id": chat_id, "message": message}


@celery_app.task
def check_and_send_reminders():
    """
    Задача для проверки и отправки всех напоминаний в нужное время
    """
    result = ReminderScheduler.check_daily_reminders()
    return {"status": "completed", "message": "Reminder check completed", "result": str(result)}