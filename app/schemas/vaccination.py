from pydantic import BaseModel
from typing import Optional
from datetime import date


class VaccinationBase(BaseModel):
    name: str
    date_administered: date
    next_due_date: Optional[date] = None


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationUpdate(BaseModel):
    name: Optional[str] = None
    date_administered: Optional[date] = None
    next_due_date: Optional[date] = None


class VaccinationResponse(VaccinationBase):
    id: int
    pet_id: int

    model_config = {"from_attributes": True}
