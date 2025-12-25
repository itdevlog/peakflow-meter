from pydantic import BaseModel
from typing import Optional


class ZoneCalculationResponse(BaseModel):
    """
    Ответ с информацией о зоне для конкретного значения пикфлоу
    """
    value: int
    zone: str  # 'green', 'yellow', 'red'
    status_text: str  # текстовое описание статуса
    zone_boundaries: Optional[dict] = None  # границы зон для отображения