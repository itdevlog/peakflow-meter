from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MeasurementBase(BaseModel):
    value: int
    timestamp: datetime
    zone: Optional[str] = None
    notes: Optional[str] = None


class MeasurementCreate(MeasurementBase):
    child_id: int


class MeasurementUpdate(BaseModel):
    value: Optional[int] = None
    timestamp: Optional[datetime] = None
    zone: Optional[str] = None
    notes: Optional[str] = None


class MeasurementResponse(MeasurementBase):
    id: int
    child_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True