from pydantic import BaseModel, EmailStr
from typing import Optional


class VetBase(BaseModel):
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    email: EmailStr


class VetCreate(VetBase):
    pass


class VetUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialty: Optional[str] = None
    email: Optional[EmailStr] = None


class VetResponse(VetBase):
    id: int

    model_config = {"from_attributes": True}
