from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # 'parent' или 'child'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Связи
    child_profile = relationship("ChildProfile", back_populates="user", uselist=False)
    parent_relations = relationship("ParentChildRelation", back_populates="parent")


class ChildProfile(Base):
    __tablename__ = "child_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("users.id"))  # ID родителя
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)  # Для расчета возраста
    height = Column(Integer)  # Рост в сантиметрах
    gender = Column(String)  # 'male' или 'female'
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    best_result = Column(Integer)  # Лучший показатель для расчета зон

    # Связи
    user = relationship("User", back_populates="child_profile")
    parent = relationship("User", foreign_keys=[parent_id])
    measurements = relationship("Measurement", back_populates="child")
    reminders = relationship("Reminder", back_populates="child")
    profile_settings = relationship("ProfileSettings", back_populates="child", uselist=False)


class ParentChildRelation(Base):
    __tablename__ = "parent_child_relations"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    child_id = Column(Integer, ForeignKey("child_profiles.id"))
    relationship_status = Column(String)  # 'active', 'pending', 'removed'
    created_at = Column(DateTime)

    # Связи
    parent = relationship("User", back_populates="parent_relations")
    child = relationship("ChildProfile")