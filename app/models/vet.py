from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Vet(Base):
    __tablename__ = "vets"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    specialty = Column(String(100), nullable=True)   # e.g. surgery, dermatology
    email = Column(String(100), unique=True, nullable=False, index=True)

    appointments = relationship("Appointment", back_populates="vet")
