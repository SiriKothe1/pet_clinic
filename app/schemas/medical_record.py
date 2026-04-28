from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MedicalRecordBase(BaseModel):
    appointment_id: int
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordResponse(MedicalRecordBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
