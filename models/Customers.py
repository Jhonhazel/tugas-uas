from sqlalchemy import Column, String, DateTime, func
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

    bookings = relationship("Booking", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.id}, email='{self.email}')>"