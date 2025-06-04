from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class LoginHistory(Base):
    __tablename__ = 'login_history'
    id = Column(String(12), primary_key=True)
    user_id = Column(String(12), ForeignKey('users.id'))
    logout_date = Column(DateTime, nullable=True)
    device_id = Column(String(12))

    user = relationship("User", back_populates="login_history", passive_deletes=True)

    def __repr__(self):
        return f"<LoginHistory(id={self.id}, user_id='{self.user_id}'"