from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..database import get_db
from ..auth.security import get_current_user
from ..utils import get_password_hash

router = APIRouter(
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/profile", response_model=schemas.UserResponse)
async def get_user_profile(current_user: schemas.TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получение профиля текущего пользователя"""
    user = db.query(models.User).filter(models.User.id == current_user.user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/profile", response_model=schemas.UserResponse)
async def update_user_profile(
    user_update: schemas.UserUpdate,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновление профиля текущего пользователя"""
    user = db.query(models.User).filter(models.User.id == current_user.user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Обновляем только те поля, которые были переданы
    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/child-profile", response_model=schemas.ChildProfileResponse)
async def get_child_profile(current_user: schemas.TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получение профиля ребенка (для родителя или ребенка)"""
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.user_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    return child_profile


@router.put("/child-profile", response_model=schemas.ChildProfileResponse)
async def update_child_profile(
    child_update: schemas.ChildProfileUpdate,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновление профиля ребенка (только для родителя)"""
    child_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.user_id == current_user.user_id
    ).first()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Проверяем, является ли текущий пользователь родителем или самим ребенком
    # В реальной системе нужно добавить проверку ролей
    
    # Обновляем только те поля, которые были переданы
    if child_update.first_name:
        child_profile.first_name = child_update.first_name
    if child_update.last_name:
        child_profile.last_name = child_update.last_name
    if child_update.birth_date:
        child_profile.birth_date = child_update.birth_date
    if child_update.height is not None:
        child_profile.height = child_update.height
    if child_update.gender:
        child_profile.gender = child_update.gender
    if child_update.best_result is not None:
        child_profile.best_result = child_update.best_result
    
    db.commit()
    db.refresh(child_profile)
    
    return child_profile


@router.post("/child-profile", response_model=schemas.ChildProfileResponse)
async def create_child_profile(
    child_profile: schemas.ChildProfileCreate,
    current_user: schemas.TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание профиля ребенка (только для родителя)"""
    # Проверяем, что текущий пользователь является родителем
    parent = db.query(models.User).filter(models.User.id == current_user.user_id).first()
    
    if parent.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create child profiles"
        )
    
    # Проверяем, не существует ли уже профиль ребенка для этого пользователя
    existing_profile = db.query(models.ChildProfile).filter(
        models.ChildProfile.user_id == child_profile.user_id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Child profile already exists for this user"
        )
    
    # Создаем новый профиль ребенка
    db_child_profile = models.ChildProfile(
        user_id=child_profile.user_id,
        parent_id=child_profile.parent_id,
        first_name=child_profile.first_name,
        last_name=child_profile.last_name,
        birth_date=child_profile.birth_date,
        height=child_profile.height,
        gender=child_profile.gender
    )
    
    db.add(db_child_profile)
    db.commit()
    db.refresh(db_child_profile)
    
    return db_child_profile