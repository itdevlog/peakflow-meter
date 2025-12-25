"""
Модуль для интеграции с Telegram-ботом
"""
import asyncio
import logging
from typing import Dict, Any
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes,
    ConversationHandler
)
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas
from .utils.zone_calculator import calculate_zone_boundaries, determine_zone
from .config import settings

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для диалогов
MEASUREMENT_VALUE = 1

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд и сообщений"""
        # Обработчики команд
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("add", self.add_measurement))
        self.application.add_handler(CommandHandler("status", self.get_status))
        self.application.add_handler(CommandHandler("history", self.get_history))
        
        # Обработчик для ввода значения измерения
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_measurement_input)
        )
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        welcome_message = (
            f"Привет, {user.first_name}! 👋\n\n"
            "Я бот для отслеживания пикфлоу у детей. "
            "Я помогу вам быстро вносить результаты измерений "
            "и следить за состоянием здоровья.\n\n"
            "Доступные команды:\n"
            "/add - добавить результат измерения\n"
            "/status - текущий статус\n"
            "/history - история измерений\n"
            "/help - справка"
        )
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = (
            "📖 Справка по боту Пикфлоуметр\n\n"
            "Команды:\n"
            "/add - добавить результат измерения пикфлоу\n"
            "/status - показать текущий статус и последнее измерение\n"
            "/history - показать последние 5 измерений\n\n"
            "Как пользоваться:\n"
            "1. Используйте команду /add\n"
            "2. Введите значение в литрах в минуту (л/мин)\n"
            "3. Бот проанализирует результат и скажет, в какой зоне он находится\n\n"
            "Зоны:\n"
            "🟢 Зеленая - отличный результат\n"
            "🟡 Желтая - требует внимания\n"
            "🔴 Красная - требуется медицинская помощь"
        )
        await update.message.reply_text(help_text)
    
    async def add_measurement(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /add"""
        await update.message.reply_text(
            "Введите результат измерения пикфлоу (значение в л/мин):",
            reply_markup=ReplyKeyboardRemove()
        )
        # В реальной системе нужно будет реализовать состояние для ожидания ввода
        # Пока просто инструкция
        return MEASUREMENT_VALUE
    
    async def handle_measurement_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка ввода значения измерения"""
        user_message = update.message.text.strip()
        
        try:
            # Попытка преобразовать сообщение в число
            value = int(user_message)
            
            if value <= 0:
                await update.message.reply_text(
                    "❌ Значение должно быть положительным числом. "
                    "Попробуйте снова, используя команду /add"
                )
                return
            
            # В реальной системе здесь нужно получить профиль ребенка по chat_id
            # и сохранить измерение в базу данных
            db = SessionLocal()
            try:
                # Для демонстрации используем заглушку
                # В реальной системе нужно получить child_id по chat_id
                child_id = 1  # Заглушка
                
                # Получаем профиль ребенка для расчета зоны
                child_profile = db.query(models.ChildProfile).filter(
                    models.ChildProfile.id == child_id
                ).first()
                
                if child_profile:
                    # Рассчитываем зону для значения
                    boundaries = calculate_zone_boundaries(child_profile)
                    zone = determine_zone(value, boundaries)
                    
                    # Сохраняем измерение в базу
                    measurement = models.Measurement(
                        child_id=child_id,
                        value=value,
                        timestamp=datetime.utcnow(),
                        zone=zone
                    )
                    db.add(measurement)
                    db.commit()
                    
                    # Формируем сообщение в зависимости от зоны
                    zone_messages = {
                        "green": "🟢 Отличный результат! Продолжайте в том же духе.",
                        "yellow": "🟡 Умеренное значение. Следите за состоянием.",
                        "red": "🔴 Низкое значение. Рекомендуется обратиться к врачу."
                    }
                    
                    status_text = zone_messages.get(zone, "📊 Результат сохранен")
                    await update.message.reply_text(f"{status_text}\n\nЗначение: {value} л/мин")
                else:
                    await update.message.reply_text(
                        f"✅ Результат сохранен: {value} л/мин\n"
                        "(Информация о зоне недоступна - профиль ребенка не найден)"
                    )
                    
            except Exception as e:
                logger.error(f"Error saving measurement: {e}")
                await update.message.reply_text(
                    "❌ Произошла ошибка при сохранении измерения. Попробуйте позже."
                )
            finally:
                db.close()
                
        except ValueError:
            await update.message.reply_text(
                "❌ Пожалуйста, введите числовое значение. "
                "Например: 450\n"
                "Попробуйте снова, используя команду /add"
            )
    
    async def get_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /status"""
        db = SessionLocal()
        try:
            # В реальной системе нужно получить child_id по chat_id
            child_id = 1  # Заглушка
            
            # Получаем последнее измерение
            last_measurement = db.query(models.Measurement).filter(
                models.Measurement.child_id == child_id
            ).order_by(models.Measurement.timestamp.desc()).first()
            
            if last_measurement:
                # Получаем профиль ребенка для расчета зоны
                child_profile = db.query(models.ChildProfile).filter(
                    models.ChildProfile.id == child_id
                ).first()
                
                if child_profile:
                    boundaries = calculate_zone_boundaries(child_profile)
                    zone = determine_zone(last_measurement.value, boundaries)
                    
                    zone_emojis = {
                        "green": "🟢",
                        "yellow": "🟡", 
                        "red": "🔴"
                    }
                    
                    zone_names = {
                        "green": "Зеленая зона (отлично)",
                        "yellow": "Желтая зона (осторожно)",
                        "red": "Красная зона (тревожно)"
                    }
                    
                    status_message = (
                        f"{zone_emojis.get(zone, '📊')} Текущий статус:\n"
                        f"Последнее измерение: {last_measurement.value} л/мин\n"
                        f"Дата: {last_measurement.timestamp.strftime('%d.%m.%Y %H:%M')}\n"
                        f"Зона: {zone_names.get(zone, 'Неизвестно')}\n\n"
                        f"Следите за своим состоянием!"
                    )
                else:
                    status_message = (
                        f"📊 Последнее измерение: {last_measurement.value} л/мин\n"
                        f"Дата: {last_measurement.timestamp.strftime('%d.%m.%Y %H:%M')}\n\n"
                        "Информация о зоне недоступна - профиль ребенка не найден"
                    )
            else:
                status_message = "❌ Нет данных об измерениях. Используйте /add для добавления результата."
            
            await update.message.reply_text(status_message)
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            await update.message.reply_text("❌ Произошла ошибка при получении статуса.")
        finally:
            db.close()
    
    async def get_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /history"""
        db = SessionLocal()
        try:
            # В реальной системе нужно получить child_id по chat_id
            child_id = 1  # Заглушка
            
            # Получаем последние 5 измерений
            measurements = db.query(models.Measurement).filter(
                models.Measurement.child_id == child_id
            ).order_by(models.Measurement.timestamp.desc()).limit(5).all()
            
            if measurements:
                history_text = "📋 История последних измерений:\n\n"
                for measurement in measurements:
                    date_str = measurement.timestamp.strftime('%d.%m %H:%M')
                    history_text += f"• {measurement.value} л/мин - {date_str}\n"
            else:
                history_text = "❌ Нет данных об измерениях. Используйте /add для добавления результата."
            
            await update.message.reply_text(history_text)
            
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            await update.message.reply_text("❌ Произошла ошибка при получении истории.")
        finally:
            db.close()
    
    async def send_reminder(self, chat_id: int, message: str):
        """Отправка напоминания в чат"""
        try:
            await self.application.bot.send_message(chat_id=chat_id, text=message)
            return True
        except Exception as e:
            logger.error(f"Error sending reminder to {chat_id}: {e}")
            return False
    
    def run(self):
        """Запуск бота"""
        if not self.token:
            raise ValueError("Telegram bot token is not configured")
        
        logger.info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def create_telegram_bot():
    """Создание экземпляра Telegram бота"""
    if not settings.telegram_bot_token:
        logger.warning("Telegram bot token is not configured")
        return None
    
    bot = TelegramBot(settings.telegram_bot_token)
    return bot