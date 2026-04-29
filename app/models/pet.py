from app.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)   # e.g. dog, cat, bird
    breed = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)

    owner = relationship("Owner", back_populates="pets")
    appointments = relationship("Appointment", back_populates="pet", cascade="all, delete-orphan")
    vaccinations = relationship("Vaccination", back_populates="pet", cascade="all, delete-orphan")
