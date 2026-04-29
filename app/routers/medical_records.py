import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.medical_record import MedicalRecord
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/medical-records", tags=["Medical Records"])


@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
def create_medical_record(record: MedicalRecordCreate, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == record.appointment_id).first()
    if not appt:
        logger.warning(f"Failed to create medical record: Appointment {record.appointment_id} not found")
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appt.status != AppointmentStatus.completed:
        logger.warning(f"Failed to create medical record: Appointment {record.appointment_id} status is {appt.status}")
        raise HTTPException(status_code=400, detail="Medical records can only be created for completed appointments")
    if db.query(MedicalRecord).filter(MedicalRecord.appointment_id == record.appointment_id).first():
        logger.warning(f"Failed to create medical record: Record already exists for appointment {record.appointment_id}")
        raise HTTPException(status_code=400, detail="Medical record already exists for this appointment")
    db_record = MedicalRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    logger.info(f"Created medical record with ID: {db_record.id} for appointment: {record.appointment_id}")
    return db_record


@router.get("/appointment/{appointment_id}", response_model=MedicalRecordResponse)
def get_medical_record(appointment_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.appointment_id == appointment_id).first()
    if not record:
        logger.warning(f"Medical record not found for appointment: {appointment_id}")
        raise HTTPException(status_code=404, detail="Medical record not found for this appointment")
    return record


@router.get("/", response_model=List[MedicalRecordResponse])
def list_medical_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(MedicalRecord).offset(skip).limit(limit).all()
