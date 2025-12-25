"""
Модуль для отправки уведомлений
"""
import asyncio
import requests
from typing import Optional
from ..config import settings


class NotificationSender:
    """
    Класс для отправки уведомлений различными способами
    """
    
    @staticmethod
    async def send_telegram_message(chat_id: int, message: str) -> bool:
        """
        Отправка сообщения через Telegram
        """
        if not settings.telegram_bot_token:
            print("Telegram bot token not configured")
            return False
            
        try:
            url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    @staticmethod
    async def send_email(recipient: str, subject: str, body: str) -> bool:
        """
        Отправка email (заглушка, в реальной системе использовать SMTP)
        """
        # В реальной системе здесь будет реализация отправки email
        # через SMTP или сторонний сервис (например, SendGrid)
        print(f"Email to {recipient}: {subject}")
        print(body)
        return True # В реальной системе возвращать результат отправки
    
    @staticmethod
    async def send_notification(
        notification_type: str, 
        recipient: str, 
        message: str,
        subject: Optional[str] = None
    ) -> bool:
        """
        Универсальный метод отправки уведомлений
        """
        if notification_type == "telegram":
            # В реальной системе chat_id нужно будет получить из профиля пользователя
            # Здесь просто возвращаем результат как заглушку
            print(f"Sending Telegram notification to {recipient}: {message}")
            return True
        elif notification_type == "email":
            subject = subject or "Напоминание от Пикфлоуметра"
            return await NotificationSender.send_email(recipient, subject, message)
        elif notification_type == "both":
            # Отправляем и в Telegram, и на email
            telegram_success = True  # await NotificationSender.send_telegram_message(chat_id, message)
            email_success = await NotificationSender.send_email(recipient, subject or "Напоминание от Пикфлоуметра", message)
            return telegram_success and email_success
        else:
            return False