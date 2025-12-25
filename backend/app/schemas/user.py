from pydantic import BaseModel
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    role: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class ChildProfileBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    height: int
    gender: str


class ChildProfileCreate(ChildProfileBase):
    parent_id: int


class ChildProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    height: Optional[int] = None
    gender: Optional[str] = None
    best_result: Optional[int] = None


class ChildProfileResponse(ChildProfileBase):
    id: int
    user_id: int
    parent_id: int
    best_result: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True