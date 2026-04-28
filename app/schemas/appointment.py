from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    pet_id: int
    vet_id: int
    scheduled_at: datetime
    reason: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    id: int
    status: AppointmentStatus

    model_config = {"from_attributes": True}
