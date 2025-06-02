import enum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from db.db import Base
from sqlalchemy.orm import relationship

class RoleUser(enum.Enum):
    admin = 'admin'
    user = 'user'

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(String(12), primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    username = Column(String(10), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleUser), nullable=False, default=RoleUser.user)
    created_at = Column(DateTime, default=datetime.utcnow)

    #relasi tabel login history
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")