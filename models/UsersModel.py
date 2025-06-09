import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from db.db import Base

class RoleUser(enum.Enum):
    admin = 'admin'
    user = 'user'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    username = Column(String(10), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleUser), nullable=False, default=RoleUser.user)
    created_at = Column(DateTime, default=datetime.utcnow)