from sqlalchemy import Column, String, DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import relationship

from db.db import Base
from .Enums import PaymentStatusEnum

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(String(12), primary_key=True)
    customer_id = Column(String(12), ForeignKey('customers.id'))
    payment_status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
    event_id = Column(String(12), ForeignKey("events.id"), nullable=False)
    payment_id = Column(String(12), ForeignKey("payment_info.id"), nullable=True, unique=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(String(12), ForeignKey("users.id"), nullable=True)

    customer = relationship("Customer", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")
    payment_info = relationship("PaymentInfo", foreign_keys=[payment_id])
    tickets = relationship("Ticket", back_populates="booking", cascade="all, delete-orphan")
    user = relationship("User", back_populates="bookings")

    def __repr__(self):
        return f"<Booking(id={self.id}, customer_id='{self.customer_id}', event_i:d='{self.event_id}')>"