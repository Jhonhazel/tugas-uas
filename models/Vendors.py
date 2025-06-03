from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from db.db import Base

class Vendor(Base):
    __tablename__ = 'vendors'

    id = Column(String(12), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    support_type = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=func.now())

    events = relationship("Event", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor(id={self.id}, name='{self.name}')>"