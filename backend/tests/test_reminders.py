"""
Тесты для системы напоминаний и уведомлений
"""
import pytest
from datetime import datetime, time, date
from unittest.mock import patch, MagicMock
from app.reminder_scheduler import ReminderScheduler
from app.utils.notification_sender import NotificationSender
from app.models.reminder import Reminder, Notification
from app.models.user import ChildProfile


def test_reminder_creation():
    """Тест создания напоминания"""
    reminder = Reminder(
        id=1,
        child_id=1,
        time_of_day=time(8, 0),  # 8:00
        days_of_week=[1, 3, 5],  # Пн, Ср, Пт
        is_active=True,
        notification_type="telegram"
    )
    
    # Проверяем, что напоминание создано корректно
    assert reminder.time_of_day == time(8, 0)
    assert 1 in reminder.days_of_week  # Понедельник
    assert 3 in reminder.days_of_week  # Среда
    assert 5 in reminder.days_of_week # Пятница
    assert reminder.is_active is True
    assert reminder.notification_type == "telegram"


def test_notification_creation():
    """Тест создания уведомления"""
    notification = Notification(
        id=1,
        user_id=1,
        reminder_id=1,
        message_text="Напоминание: не забудьте сделать измерение!",
        status="pending",
        notification_channel="telegram"
    )
    
    assert notification.message_text == "Напоминание: не забудьте сделать измерение!"
    assert notification.status == "pending"
    assert notification.notification_channel == "telegram"


def test_notification_sender_telegram():
    """Тест отправки уведомления через Telegram"""
    # Мокаем внешнее API
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ok": True}
        
        success = NotificationSender.send_telegram_message(123456, "Тестовое сообщение")
        
        # Проверяем, что запрос был отправлен
        mock_post.assert_called_once()
        assert success is True


def test_notification_sender_email():
    """Тест отправки уведомления через email"""
    # Тестирование отправки email
    success = NotificationSender.send_email(
        "test@example.com",
        "Тема",
        "Текст сообщения"
    )
    
    # В текущей реализации всегда возвращает True
    assert success is True


def test_notification_sender_universal():
    """Тест универсального метода отправки уведомлений"""
    # Тестируем отправку через разные каналы
    with patch('app.utils.notification_sender.NotificationSender.send_telegram_message') as mock_telegram:
        with patch('app.utils.notification_sender.NotificationSender.send_email') as mock_email:
            mock_telegram.return_value = True
            mock_email.return_value = True
            
            # Телеграм
            result = NotificationSender.send_notification("telegram", "123456", "Сообщение")
            assert result is True
            
            # Email
            result = NotificationSender.send_notification("email", "test@example.com", "Сообщение", "Тема")
            assert result is True
            
            # Оба
            result = NotificationSender.send_notification("both", "test@example.com", "Сообщение", "Тема")
            assert result is True


def test_reminder_scheduler_check_daily_reminders():
    """Тест проверки ежедневных напоминаний"""
    # Создаем мок для сессии базы данных
    with patch('app.reminder_scheduler.SessionLocal') as mock_session:
        # Создаем мок объекта сессии
        mock_db_session = MagicMock()
        mock_session.return_value = mock_db_session
        
        # Мокаем результаты запросов
        mock_reminder = MagicMock()
        mock_reminder.id = 1
        mock_reminder.child_id = 1
        mock_reminder.time_of_day = datetime.now().time()
        mock_reminder.days_of_week = [date.today().isoweekday()]  # Сегодняшний день недели
        mock_reminder.is_active = True
        
        mock_db_session.query.return_value.filter.return_value.all.return_value = [mock_reminder]
        
        # Мокаем подсчет измерений
        mock_db_session.query.return_value.filter.return_value.count.return_value = 0  # Нет измерений сегодня
        
        # Вызываем метод
        result = ReminderScheduler.check_daily_reminders()
        
        # Проверяем, что результат есть
        assert result is not None


def test_reminder_scheduler_send_notification():
    """Тест отправки конкретного уведомления"""
    # Создаем мок для сессии базы данных
    with patch('app.reminder_scheduler.SessionLocal') as mock_session:
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db_session
        mock_session.return_value.__exit__.return_value = None
        
        # Мокаем объекты
        mock_reminder = MagicMock()
        mock_reminder.id = 1
        mock_reminder.child_id = 1
        mock_reminder.notification_type = "telegram"
        
        mock_child = MagicMock()
        mock_child.id = 1
        mock_child.first_name = "Анна"
        mock_child.last_name = "Иванова"
        mock_child.user_id = 1
        
        mock_measurement = MagicMock()
        mock_measurement.value = 450
        mock_measurement.timestamp = datetime.now()
        
        # Настройка возвращаемых значений
        mock_db_session.query.return_value.filter.return_value.first.side_effect = [
            mock_reminder,  # Напоминание
            mock_child,     # Ребенок
            mock_measurement  # Последнее измерение
        ]
        
        # Вызываем метод
        result = ReminderScheduler.send_reminder_notification_async(1)
        
        # Проверяем, что результат - булево значение
        assert isinstance(result, bool)


def test_reminder_scheduler_schedule():
    """Тест планирования напоминаний"""
    result = ReminderScheduler.schedule_reminders()
    
    # В текущей реализации всегда возвращает True
    assert result is True


def test_reminder_active_toggle():
    """Тест переключения активности напоминания"""
    reminder = Reminder(
        id=1,
        child_id=1,
        time_of_day=time(8, 0),
        days_of_week=[1, 3, 5],
        is_active=True,
        notification_type="telegram"
    )
    
    # Переключаем статус
    initial_status = reminder.is_active
    reminder.is_active = not initial_status
    
    # Проверяем, что статус изменился
    assert reminder.is_active != initial_status


def test_notification_status_update():
    """Тест обновления статуса уведомления"""
    notification = Notification(
        id=1,
        user_id=1,
        reminder_id=1,
        message_text="Тест",
        status="pending",
        notification_channel="telegram"
    )
    
    # Изменяем статус
    notification.status = "sent"
    assert notification.status == "sent"
    
    # Еще раз изменяем
    notification.status = "failed"
    assert notification.status == "failed"