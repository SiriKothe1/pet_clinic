from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.pet import Pet
from app.models.vet import Vet
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def book_appointment(appt: AppointmentCreate, db: Session = Depends(get_db)):
    if not db.query(Pet).filter(Pet.id == appt.pet_id).first():
        raise HTTPException(status_code=404, detail="Pet not found")
    if not db.query(Vet).filter(Vet.id == appt.vet_id).first():
        raise HTTPException(status_code=404, detail="Vet not found")
    db_appt = Appointment(**appt.model_dump())
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
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
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.put("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.status != AppointmentStatus.scheduled:
        raise HTTPException(status_code=400, detail=f"Cannot cancel a {appt.status} appointment")
    appt.status = AppointmentStatus.cancelled
    db.commit()
    db.refresh(appt)
    return appt


@router.put("/{appointment_id}/complete", response_model=AppointmentResponse)
def complete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.status != AppointmentStatus.scheduled:
        raise HTTPException(status_code=400, detail=f"Cannot complete a {appt.status} appointment")
    appt.status = AppointmentStatus.completed
    db.commit()
    db.refresh(appt)
    return appt
