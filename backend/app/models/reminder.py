from sqlalchemy import Column, Integer, Time, DateTime, ForeignKey, String, ARRAY, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("child_profiles.id"))
    time_of_day = Column(Time)  # время в формате HH:MM
    days_of_week = Column(ARRAY(Integer))  # массив дней недели (1-7)
    is_active = Column(Boolean, default=True)
    notification_type = Column(String)  # 'telegram', 'email', 'both'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    child = relationship("ChildProfile", back_populates="reminders")
    notifications = relationship("Notification", back_populates="reminder")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reminder_id = Column(Integer, ForeignKey("reminders.id"))
    message_text = Column(String)
    sent_at = Column(TIMESTAMP(timezone=True))
    status = Column(String)  # 'pending', 'sent', 'failed'
    notification_channel = Column(String)  # 'telegram', 'email'

    # Связи
    user = relationship("User")
    reminder = relationship("Reminder", back_populates="notifications")