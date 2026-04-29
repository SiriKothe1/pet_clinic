import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.vet import Vet
from app.models.appointment import Appointment
from app.schemas.vet import VetCreate, VetUpdate, VetResponse
from app.schemas.appointment import AppointmentResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/vets", tags=["Vets"])


@router.post("/", response_model=VetResponse, status_code=status.HTTP_201_CREATED)
def create_vet(vet: VetCreate, db: Session = Depends(get_db)):
    if db.query(Vet).filter(Vet.email == vet.email).first():
        logger.warning(f"Failed to create vet: Email {vet.email} already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    db_vet = Vet(**vet.model_dump())
    db.add(db_vet)
    db.commit()
    db.refresh(db_vet)
    logger.info(f"Created vet with ID: {db_vet.id}")
    return db_vet


@router.get("/", response_model=List[VetResponse])
def list_vets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Vet).offset(skip).limit(limit).all()


@router.get("/{vet_id}", response_model=VetResponse)
def get_vet(vet_id: int, db: Session = Depends(get_db)):
    vet = db.query(Vet).filter(Vet.id == vet_id).first()
    if not vet:
        logger.warning(f"Vet not found: {vet_id}")
        raise HTTPException(status_code=404, detail="Vet not found")
    return vet


@router.put("/{vet_id}", response_model=VetResponse)
def update_vet(vet_id: int, updates: VetUpdate, db: Session = Depends(get_db)):
    vet = db.query(Vet).filter(Vet.id == vet_id).first()
    if not vet:
        logger.warning(f"Vet not found for update: {vet_id}")
        raise HTTPException(status_code=404, detail="Vet not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(vet, field, value)
    db.commit()
    db.refresh(vet)
    logger.info(f"Updated vet with ID: {vet_id}")
    return vet


@router.delete("/{vet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vet(vet_id: int, db: Session = Depends(get_db)):
    vet = db.query(Vet).filter(Vet.id == vet_id).first()
    if not vet:
        logger.warning(f"Vet not found for deletion: {vet_id}")
        raise HTTPException(status_code=404, detail="Vet not found")
    db.delete(vet)
    db.commit()
    logger.info(f"Deleted vet with ID: {vet_id}")


@router.get("/{vet_id}/appointments", response_model=List[AppointmentResponse])
def get_vet_appointments(vet_id: int, db: Session = Depends(get_db)):
    vet = db.query(Vet).filter(Vet.id == vet_id).first()
    if not vet:
        raise HTTPException(status_code=404, detail="Vet not found")
    return db.query(Appointment).filter(Appointment.vet_id == vet_id).all()
