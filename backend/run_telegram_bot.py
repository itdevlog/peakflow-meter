"""
Скрипт для запуска Telegram-бота
"""
import asyncio
import logging
from app.telegram_bot import create_telegram_bot
from app.config import settings

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Основная функция для запуска Telegram-бота"""
    logger.info("Initializing Telegram bot...")
    
    # Проверяем, что токен бота настроен
    if not settings.telegram_bot_token:
        logger.error("Telegram bot token is not configured in settings")
        logger.error("Please set TELEGRAM_BOT_TOKEN in your environment variables")
        return
    
    try:
        # Создаем экземпляр бота
        bot = create_telegram_bot()
        
        if bot:
            logger.info("Telegram bot initialized successfully")
            logger.info("Starting bot polling...")
            
            # Запускаем бота
            bot.run()
        else:
            logger.error("Failed to create Telegram bot instance")
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running Telegram bot: {e}")
        raise


if __name__ == '__main__':
    main()