from sqlalchemy import Column, String, Float, DateTime, func, Enum, ForeignKey
from sqlalchemy.orm import relationship

from db.db import Base
from .Enums import PaymentStatus

class PaymentInfo(Base):
    __tablename__ = 'payment_info'

    id = Column(String(12), primary_key=True)
    method = Column(String(255), nullable=False)
    bank_name = Column(String(255), nullable=True)
    card_number = Column(String(255), nullable=True)
    tax = Column(Float, default=0.0)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    payment_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(String(12), ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="payment_infos")

    def __repr__(self):
        return f"<PaymentInfo(id={self.id}, amount={self.amount}, status='{self.status}')>"