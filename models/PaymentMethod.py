from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from db.db import Base


class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id = Column(String(12), primary_key=True,index=True)
    card_number = Column(String(255), nullable=True)
    bank_name = Column(String(50), nullable=True)
    card_type = Column(String(50), nullable=True)
    expired_month = Column(Integer, nullable=True)
    expired_year = Column(Integer, nullable=True)
    placeholder_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign Keys
    user_id = Column(String(12), ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="payment_methods")
    payment_infos = relationship("PaymentInfo", back_populates="payment_method")

    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, user_id='{self.user_id}', card_type='{self.card_type}')>"