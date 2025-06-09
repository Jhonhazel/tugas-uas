from sqlalchemy import Column, String, Float, DateTime, func, Enum, ForeignKey, text
from sqlalchemy.orm import relationship

from db.db import Base
from .Enums import PaymentStatusEnum, DbPaymentStatusEnum


class PaymentInfo(Base):
    __tablename__ = "payment_info"

    id = Column(String(12), primary_key=True, index=True)
    status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
    tax = Column(Float, default=0.0)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())  # Sesuai diagram, createdAt tetap ada

    # Foreign Keys
    user_id = Column(String(12), ForeignKey("users.id"), nullable=True)
    payment_method_id = Column(String(12), ForeignKey("payment_method.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="payment_infos")
    payment_method = relationship("PaymentMethod", back_populates="payment_infos")

    # Relasi ke Booking
    booking = relationship("Booking", back_populates="payment_info", uselist=False)

    def __repr__(self):
        return f"<PaymentInfo(id={self.id}, amount={self.amount}, status='{self.status}')>"