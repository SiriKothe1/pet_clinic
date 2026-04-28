from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    vet_id = Column(Integer, ForeignKey("vets.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    reason = Column(String(300), nullable=True)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled, nullable=False)

    pet = relationship("Pet", back_populates="appointments")
    vet = relationship("Vet", back_populates="appointments")
    medical_record = relationship("MedicalRecord", back_populates="appointment", uselist=False,
                                  cascade="all, delete-orphan")
