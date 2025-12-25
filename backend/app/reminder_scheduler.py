"""
Модуль для планирования и отправки напоминаний
"""
from datetime import datetime, time, date
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from .utils.notification_sender import NotificationSender
from .utils.zone_calculator import calculate_zone_boundaries, determine_zone
from .tasks import send_telegram_message, send_reminder_notification
from celery import group
import asyncio


class ReminderScheduler:
    """
    Класс для управления напоминаниями и их отправкой
    """
    
    @staticmethod
    def check_daily_reminders():
        """
        Проверяет, нужно ли отправить напоминания в текущий день
        """
        db = SessionLocal()
        try:
            # Получаем текущий день недели (1-7, где 1 - понедельник)
            current_weekday = date.today().isoweekday()
            current_time = datetime.now().time().replace(microsecond=0)  # Только время, без микросекунд
            
            # Находим все активные напоминания, которые должны сработать сегодня в это время
            active_reminders = db.query(models.Reminder).filter(
                models.Reminder.is_active == True,
                models.Reminder.time_of_day == current_time,
                models.Reminder.days_of_week.any(current_weekday)
            ).all()
            
            # Создаем задачи для отправки напоминаний
            reminder_tasks = []
            for reminder in active_reminders:
                # Проверяем, было ли уже измерение сегодня
                from sqlalchemy import and_, func
                today_start = datetime.combine(date.today(), time.min)
                today_end = datetime.combine(date.today(), time.max)
                
                measurement_count = db.query(models.Measurement).filter(
                    and_(
                        models.Measurement.child_id == reminder.child_id,
                        models.Measurement.timestamp >= today_start,
                        models.Measurement.timestamp <= today_end
                    )
                ).count()
                
                # Если измерение еще не было сделано, отправляем напоминание
                if measurement_count == 0:
                    # В реальной системе нужно получить chat_id из профиля ребенка или родителя
                    # Пока используем заглушку
                    reminder_tasks.append(send_reminder_notification.s(reminder.id))
            
            # Выполняем все задачи
            if reminder_tasks:
                job = group(reminder_tasks)
                result = job.apply_async()
                return result
            
        finally:
            db.close()
    
    @staticmethod
    async def send_reminder_notification_async(reminder_id: int):
        """
        Асинхронная отправка конкретного напоминания
        """
        db = SessionLocal()
        try:
            # Получаем информацию о напоминании
            reminder = db.query(models.Reminder).filter(
                models.Reminder.id == reminder_id
            ).first()
            
            if not reminder:
                print(f"Reminder with ID {reminder_id} not found")
                return False
            
            # Получаем информацию о ребенке
            child = db.query(models.ChildProfile).filter(
                models.ChildProfile.id == reminder.child_id
            ).first()
            
            if not child:
                print(f"Child with ID {reminder.child_id} not found")
                return False
            
            # Получаем последний результат измерения для персонализации сообщения
            last_measurement = db.query(models.Measurement).filter(
                models.Measurement.child_id == child.id
            ).order_by(models.Measurement.timestamp.desc()).first()
            
            # Создаем персонализированное сообщение
            child_name = f"{child.first_name} {child.last_name}"
            message = f"Напоминание: {child_name}, пришло время сделать измерение пикфлоу!\n"
            
            if last_measurement:
                # Определяем, в какой зоне был последний результат
                boundaries = calculate_zone_boundaries(child)
                zone = determine_zone(last_measurement.value, boundaries)
                
                zone_messages = {
                    "green": "Ваш последний результат был отличным! Продолжайте в том же духе.",
                    "yellow": "Ваш последний результат был в желтой зоне. Обратите внимание на свое состояние.",
                    "red": "Ваш последний результат был в красной зоне. Рекомендуется обратиться к врачу."
                }
                
                message += f"{zone_messages.get(zone, '')}\n"
            
            message += "Пожалуйста, не забудьте сделать сегодняшнее измерение."
            
            # В реальной системе здесь нужно получить данные для отправки уведомления
            # (например, chat_id для Telegram или email)
            # Пока используем заглушку
            
            # Возвращаем результат отправки (в реальной системе будет результат отправки уведомления)
            print(f"Sending reminder to child {child.id}: {message}")
            
            # Создаем запись уведомления в базе данных
            notification = models.Notification(
                user_id=child.user_id, # Отправляем родителю
                reminder_id=reminder.id,
                message_text=message,
                status="pending",  # В реальной системе статус будет обновляться после отправки
                notification_channel=reminder.notification_type
            )
            
            db.add(notification)
            db.commit()
            
            # В реальной системе здесь будет отправка уведомления через соответствующий канал
            # await NotificationSender.send_notification(
            #     notification_type=reminder.notification_type,
            #     recipient=recipient_info,
            #     message=message
            # )
            
            # Обновляем статус уведомления
            notification.status = "sent"
            notification.sent_at = datetime.utcnow()
            db.commit()
            
            return True
            
        except Exception as e:
            print(f"Error sending reminder notification: {e}")
            # В случае ошибки обновляем статус уведомления
            if 'notification' in locals():
                notification.status = "failed"
                db.commit()
            return False
        finally:
            db.close()
    
    @staticmethod
    def schedule_reminders():
        """
        Метод для планирования напоминаний (интеграция с планировщиком)
        """
        # В реальной системе этот метод будет интегрироваться с планировщиком задач
        # например, с помощью Celery Beat
        print("Reminder scheduler initialized")
        return True