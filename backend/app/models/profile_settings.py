from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class ProfileSettings(Base):
    __tablename__ = "profile_settings"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("child_profiles.id"))
    zone_green_min = Column(Integer)  # минимальное значение зеленой зоны
    zone_yellow_min = Column(Integer)  # минимальное значение желтой зоны
    zone_red_min = Column(Integer)  # минимальное значение красной зоны
    calculation_method = Column(String)  # метод расчета зон (по возрасту/росту)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    child = relationship("ChildProfile", back_populates="profile_settings")