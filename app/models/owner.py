from app.database import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)

    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
