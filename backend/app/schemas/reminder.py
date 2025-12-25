from pydantic import BaseModel
from datetime import datetime, time
from typing import List, Optional


class ReminderBase(BaseModel):
    time_of_day: time
    days_of_week: List[int]  # массив дней недели (1-7, где 1 - понедельник)
    is_active: bool = True
    notification_type: str # 'telegram', 'email', 'both'


class ReminderCreate(ReminderBase):
    child_id: int


class ReminderUpdate(BaseModel):
    time_of_day: Optional[time] = None
    days_of_week: Optional[List[int]] = None
    is_active: Optional[bool] = None
    notification_type: Optional[str] = None


class ReminderResponse(ReminderBase):
    id: int
    child_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    user_id: int
    reminder_id: int
    message_text: str
    status: str  # 'pending', 'sent', 'failed'
    notification_channel: str  # 'telegram', 'email'


class NotificationCreate(NotificationBase):
    pass


class NotificationResponse(NotificationBase):
    id: int
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True