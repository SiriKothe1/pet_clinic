import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.pet import Pet
from app.models.vet import Vet
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def book_appointment(appt: AppointmentCreate, db: Session = Depends(get_db)):
    if not db.query(Pet).filter(Pet.id == appt.pet_id).first():
        logger.warning(f"Failed to book appointment: Pet {appt.pet_id} not found")
        raise HTTPException(status_code=404, detail="Pet not found")
    if not db.query(Vet).filter(Vet.id == appt.vet_id).first():
        logger.warning(f"Failed to book appointment: Vet {appt.vet_id} not found")
        raise HTTPException(status_code=404, detail="Vet not found")
    db_appt = Appointment(**appt.model_dump())
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    logger.info(f"Booked appointment with ID: {db_appt.id} for pet: {appt.pet_id} with vet: {appt.vet_id}")
    return db_appt


@router.get("/", response_model=List[AppointmentResponse])
def list_appointments(
    skip: int = 0,
    limit: int = 100,
    status: AppointmentStatus | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Appointment)
    if status:
        query = query.filter(Appointment.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        logger.warning(f"Appointment not found: {appointment_id}")
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.put("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        logger.warning(f"Appointment not found for cancellation: {appointment_id}")
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.status != AppointmentStatus.scheduled:
        logger.warning(f"Failed to cancel appointment {appointment_id}: Status is {appt.status}")
        raise HTTPException(status_code=400, detail=f"Cannot cancel a {appt.status} appointment")
    appt.status = AppointmentStatus.cancelled
    db.commit()
    db.refresh(appt)
    logger.info(f"Cancelled appointment with ID: {appointment_id}")
    return appt


@router.put("/{appointment_id}/complete", response_model=AppointmentResponse)
def complete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        logger.warning(f"Appointment not found for completion: {appointment_id}")
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.status != AppointmentStatus.scheduled:
        logger.warning(f"Failed to complete appointment {appointment_id}: Status is {appt.status}")
        raise HTTPException(status_code=400, detail=f"Cannot complete a {appt.status} appointment")
    appt.status = AppointmentStatus.complet
    db.commit()
    db.refresh(appt)
    logger.info(f"Completed appointment with ID: {appointment_id}")
    return appt
