from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LostFoundPetBase(BaseModel):
    report_type: str = Field(..., pattern="^(LOST|FOUND)$", description="Must be 'LOST' or 'FOUND'")
    pet_name: Optional[str] = None
    species: str
    breed: Optional[str] = None
    description: Optional[str] = None
    location: str
    contact_info: str


class LostFoundPetCreate(LostFoundPetBase):
    pass


class LostFoundPetUpdate(BaseModel):
    report_type: Optional[str] = Field(None, pattern="^(LOST|FOUND)$")
    pet_name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    contact_info: Optional[str] = None
    is_resolved: Optional[bool] = None


class LostFoundPetResponse(LostFoundPetBase):
    id: int
    date_reported: datetime
    is_resolved: bool

    model_config = {"from_attributes": True}
