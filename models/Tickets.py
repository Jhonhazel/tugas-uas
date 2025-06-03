from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from db.db import Base

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(String(12), primary_key=True)
    price = Column(Float, nullable=False)

    booking_id = Column(String(12), ForeignKey("bookings.id"), nullable=False)
    event_id = Column(String(12), ForeignKey("events.id"), nullable=False)

    booking = relationship("Booking", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket(id={self.id}, price={self.price}, booking_id='{self.booking_id}')>"