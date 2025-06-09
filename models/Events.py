from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from db.db import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(String(12), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    current_capacity = Column(Integer, nullable=False, default=0)
    tikets_count = Column(Integer, nullable=False, default=0)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    venue_address = Column(String(255), nullable=False)
    is_fullybooked = Column(Boolean, nullable=False, default=False)

    user_id = Column(String(12), ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="events")

    bookings = relationship("Booking", back_populates="event")
    tickets = relationship("Ticket", back_populates="event")

    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}')>"
