from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from db.db import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String(12), primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    address = Column(String(255), nullable=False)
    gov_id = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(String(12), ForeignKey("users.id"), nullable=True)

    bookings = relationship("Booking", back_populates="customer")
    user = relationship("User", back_populates="customers")

    def __repr__(self):
        return f"<Customer(id={self.id}, email='{self.email}')>"