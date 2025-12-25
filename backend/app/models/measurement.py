from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP, INTEGER
from datetime import datetime


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("child_profiles.id"))
    value = Column(Integer)  # результат замера в л/мин
    timestamp = Column(TIMESTAMP(timezone=True))  # время с часовым поясом
    zone = Column(String)  # 'green', 'yellow', 'red'
    notes = Column(String)  # дополнительные заметки
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    child = relationship("ChildProfile", back_populates="measurements")