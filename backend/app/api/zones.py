from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from .. import schemas, models
from ..database import get_db
from ..auth.security import get_current_user
from ..utils.zone_calculator import calculate_zone_boundaries, determine_zone

router = APIRouter(
    tags=["zones"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/current", response_model=Dict[str, Any])
async def get_current_zone_boundaries(
    child_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение текущих границ зон для ребенка"""
    # Проверяем права доступа
    if current_user.role == "child":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.user_id == current_user.user_id,
            models.ChildProfile.id == child_id
        ).first()
    elif current_user.role == "parent":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.id == child_id,
            models.ChildProfile.parent_id == current_user.user_id
        ).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    boundaries = calculate_zone_boundaries(child_profile)
    
    return {
        "child_id": child_id,
        "boundaries": boundaries,
        "calculated_at": datetime.utcnow()
    }


@router.post("/determine", response_model=schemas.ZoneCalculationResponse)
async def determine_zone_for_value(
    value: int,
    child_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Определение зоны для конкретного значения пикфлоу"""
    # Проверяем права доступа
    if current_user.role == "child":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.user_id == current_user.user_id,
            models.ChildProfile.id == child_id
        ).first()
    elif current_user.role == "parent":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.id == child_id,
            models.ChildProfile.parent_id == current_user.user_id
        ).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    boundaries = calculate_zone_boundaries(child_profile)
    zone = determine_zone(value, boundaries)
    
    # Текстовое описание статуса
    status_text = ""
    if zone == "green":
        status_text = "Отличный результат! Все в порядке. Продолжайте следить за состоянием."
    elif zone == "yellow":
        status_text = "Умеренное значение. Следите за состоянием, обратите внимание на симптомы."
    else:
        status_text = "Низкое значение. Рекомендуется обратиться к врачу, особенно если есть симптомы."
    
    return schemas.ZoneCalculationResponse(
        value=value,
        zone=zone,
        status_text=status_text,
        zone_boundaries=boundaries
    )


@router.get("/status", response_model=Dict[str, str])
async def get_current_status(
    child_id: int,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение текущего статуса (цвет зоны) по последнему замеру"""
    # Проверяем права доступа
    if current_user.role == "child":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.user_id == current_user.user_id,
            models.ChildProfile.id == child_id
        ).first()
    elif current_user.role == "parent":
        child_profile = db.query(models.ChildProfile).filter(
            models.ChildProfile.id == child_id,
            models.ChildProfile.parent_id == current_user.user_id
        ).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Получаем последний замер
    latest_measurement = db.query(models.Measurement).filter(
        models.Measurement.child_id == child_id
    ).order_by(models.Measurement.timestamp.desc()).first()
    
    if not latest_measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No measurements found for this child"
        )
    
    boundaries = calculate_zone_boundaries(child_profile)
    zone = determine_zone(latest_measurement.value, boundaries)
    
    return {
        "zone": zone,
        "measurement_id": latest_measurement.id,
        "measurement_value": latest_measurement.value,
        "timestamp": latest_measurement.timestamp.isoformat()
    }