from app.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    name = Column(String(100), nullable=False)
    date_administered = Column(Date, nullable=False)
    next_due_date = Column(Date, nullable=True)

    pet = relationship("Pet", back_populates="vaccinations")
