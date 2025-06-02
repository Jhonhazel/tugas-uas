from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from db.db import Base
from sqlalchemy.orm import relationship

class LoginHistory(Base):
    __tablename__ = 'login_history'
    id = Column(String(12), primary_key=True)
    user_id = Column(String(12), ForeignKey('users.id'))
    logout_date = Column(DateTime, nullable=True)
    device_id = Column(String(12))

    user = relationship("User", back_populates="login_history")