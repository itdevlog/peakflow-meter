from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import schemas, models
from ..database import get_db
from ..auth.security import get_current_user

router = APIRouter(
    tags=["measurements"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.MeasurementResponse)
async def create_measurement(
    measurement: schemas.MeasurementCreate,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Добавление нового замера"""
    # Проверяем, является ли пользователь родителем или ребенком
    # Если ребенок, то проверяем, что он добавляет замер для себя
    if current_user.role == "child":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.user_id == current_user.user_id
        ).first()
        if not child_profile or child_profile.id != measurement.child_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Children can only add measurements for themselves"
            )
    elif current_user.role == "parent":
        # Проверяем, что родитель добавляет замер для своего ребенка
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.id == measurement.child_id,
            models.ChildProfile.parent_id == current_user.user_id
        ).first()
        if not child_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Parents can only add measurements for their children"
            )
    
    # Создаем новый замер
    db_measurement = models.Measurement(
        child_id=measurement.child_id,
        value=measurement.value,
        timestamp=measurement.timestamp,
        notes=measurement.notes
    )
    
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    
    return db_measurement


@router.get("/", response_model=List[schemas.MeasurementResponse])
async def get_measurements(
    child_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение истории замеров для ребенка"""
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
    
    measurements = db.query(models.Measurement).filter(
        models.Measurement.child_id == child_id
    ).order_by(models.Measurement.timestamp.desc()).offset(skip).limit(limit).all()
    
    return measurements


@router.get("/latest", response_model=schemas.MeasurementResponse)
async def get_latest_measurement(
    child_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение последнего замера для ребенка"""
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
    
    latest_measurement = db.query(models.Measurement).filter(
        models.Measurement.child_id == child_id
    ).order_by(models.Measurement.timestamp.desc()).first()
    
    if not latest_measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No measurements found for this child"
        )
    
    return latest_measurement


@router.put("/{measurement_id}", response_model=schemas.MeasurementResponse)
async def update_measurement(
    measurement_id: int,
    measurement_update: schemas.MeasurementUpdate,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновление замера (только для родителя)"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can update measurements"
        )
    
    measurement = db.query(models.Measurement).filter(
        models.Measurement.id == measurement_id
    ).first()
    
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )
    
    # Проверяем, что родитель обновляет замер своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == measurement.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Обновляем только те поля, которые были переданы
    if measurement_update.value is not None:
        measurement.value = measurement_update.value
    if measurement_update.timestamp:
        measurement.timestamp = measurement_update.timestamp
    if measurement_update.zone:
        measurement.zone = measurement_update.zone
    if measurement_update.notes is not None:
        measurement.notes = measurement_update.notes
    
    db.commit()
    db.refresh(measurement)
    
    return measurement


@router.delete("/{measurement_id}")
async def delete_measurement(
    measurement_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удаление замера (только для родителя)"""
    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can delete measurements"
        )
    
    measurement = db.query(models.Measurement).filter(
        models.Measurement.id == measurement_id
    ).first()
    
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )
    
    # Проверяем, что родитель удаляет замер своего ребенка
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.id == measurement.child_id,
        models.ChildProfile.parent_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(measurement)
    db.commit()
    
    return {"message": "Measurement deleted successfully"}