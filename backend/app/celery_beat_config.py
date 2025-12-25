"""
Конфигурация планировщика задач Celery (Celery Beat)
"""
from celery import Celery
from celery.schedules import crontab
from .config import settings

# Настройка Celery
celery_app = Celery('peakflow_meter_scheduler')

# Настройка брокера (Redis)
celery_app.conf.broker_url = settings.redis_url
celery_app.conf.result_backend = settings.redis_url

# Настройка планировщика задач (Celery Beat)
celery_app.conf.beat_schedule = {
    # Проверка напоминаний каждую минуту (в реальной системе можно настроить на каждые 5-10 минут)
    'check-reminders-every-minute': {
        'task': 'app.tasks.check_and_send_reminders',
        'schedule': crontab(minute='*'),  # каждую минуту
    },
    # Ежедневная сводка в 20:00
    'daily-summary': {
        'task': 'app.tasks.check_daily_measurements',
        'schedule': crontab(hour=20, minute=0),  # каждый день в 20:00
    },
}

# Другие настройки Celery
celery_app.conf.timezone = 'UTC'
celery_app.conf.task_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_serializer = 'json'