from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base


class LostFoundPet(Base):
    __tablename__ = "lost_found_pets"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(10), nullable=False)  # "LOST" or "FOUND"
    pet_name = Column(String(50), nullable=True)      # May be unknown for FOUND
    species = Column(String(50), nullable=False)
    breed = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    location = Column(String(200), nullable=False)
    contact_info = Column(String(200), nullable=False)
    date_reported = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)
