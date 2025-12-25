from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import schemas, models
from ..database import get_db
from ..auth.security import get_current_user
from ..tasks import send_reminder_notification

router = APIRouter(
    prefix="/reminders",
    tags=["reminders"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[schemas.ReminderResponse])
async def get_reminders(
    child_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение настроек напоминаний для ребенка"""
    # Проверяем права доступа
    if current_user.role == "child":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.user_id == current_user.user_id,
            models.ChildProfile.id == child_id
        ).first()
        if not child_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    elif current_user.role == "parent":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.id == child_id,
            models.ChildProfile.parent_id == current_user.user_id
        ).first()
        if not child_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    reminders = db.query(models.Reminder).filter(
        models.Reminder.child_id == child_id
    ).all()
    
    return reminders


@router.post("/", response_model=schemas.ReminderResponse)
async def create_reminder(
    reminder: schemas.ReminderCreate,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание нового напоминания"""
    # Проверяем, что только родитель может создавать напоминания
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create reminders"
        )
    
    # Проверяем, что родитель создает напоминание для своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == reminder.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Проверяем, что нет дублирующего напоминания (в то же время)
    existing_reminder = db.query(models.Reminder).filter(
        models.Reminder.child_id == reminder.child_id,
        models.Reminder.time_of_day == reminder.time_of_day
    ).first()
    
    if existing_reminder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reminder at this time already exists"
        )
    
    db_reminder = models.Reminder(
        child_id=reminder.child_id,
        time_of_day=reminder.time_of_day,
        days_of_week=reminder.days_of_week,
        is_active=reminder.is_active,
        notification_type=reminder.notification_type
    )
    
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    
    return db_reminder


@router.put("/{reminder_id}", response_model=schemas.ReminderResponse)
async def update_reminder(
    reminder_id: int,
    reminder_update: schemas.ReminderUpdate,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновление напоминания"""
    # Проверяем, что только родитель может обновлять напоминания
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can update reminders"
        )
    
    reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Проверяем, что родитель обновляет напоминание для своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == reminder.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Обновляем только те поля, которые были переданы
    if reminder_update.time_of_day is not None:
        reminder.time_of_day = reminder_update.time_of_day
    if reminder_update.days_of_week is not None:
        reminder.days_of_week = reminder_update.days_of_week
    if reminder_update.is_active is not None:
        reminder.is_active = reminder_update.is_active
    if reminder_update.notification_type is not None:
        reminder.notification_type = reminder_update.notification_type
    
    db.commit()
    db.refresh(reminder)
    
    return reminder


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удаление напоминания"""
    # Проверяем, что только родитель может удалять напоминания
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can delete reminders"
        )
    
    reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Проверяем, что родитель удаляет напоминание для своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == reminder.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(reminder)
    db.commit()
    
    return {"message": "Reminder deleted successfully"}


@router.post("/test/{reminder_id}")
async def test_reminder(
    reminder_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Тестирование отправки напоминания"""
    # Проверяем, что только родитель может тестировать напоминания
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can test reminders"
        )
    
    reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Проверяем, что родитель тестирует напоминание для своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == reminder.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Асинхронная отправка тестового уведомления
    task = send_reminder_notification.delay(reminder_id)
    
    return {
        "message": f"Test notification scheduled for reminder {reminder_id}",
        "task_id": task.id
    }


@router.get("/history/{reminder_id}")
async def get_reminder_history(
    reminder_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение истории отправки уведомлений для конкретного напоминания"""
    # Проверяем, что только родитель может просматривать историю
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view reminder history"
        )
    
    reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Проверяем, что родитель просматривает историю для своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == reminder.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    notifications = db.query(models.Notification).filter(
        models.Notification.reminder_id == reminder_id
    ).order_by(models.Notification.sent_at.desc()).offset(skip).limit(limit).all()
    
    return notifications


@router.put("/{reminder_id}/toggle")
async def toggle_reminder_status(
    reminder_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Включение/выключение напоминания"""
    # Проверяем, что только родитель может изменять статус напоминания
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can toggle reminder status"
        )
    
    reminder = db.query(models.Reminder).filter(
        models.Reminder.id == reminder_id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Проверяем, что родитель изменяет статус напоминания для своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == reminder.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Переключаем статус
    reminder.is_active = not reminder.is_active
    db.commit()
    db.refresh(reminder)
    
    status_text = "enabled" if reminder.is_active else "disabled"
    return {"message": f"Reminder {status_text}", "is_active": reminder.is_active}