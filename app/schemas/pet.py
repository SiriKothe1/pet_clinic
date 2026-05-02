from pydantic import BaseModel
from typing import Optional
from datetime import date


class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    date_of_birth: Optional[date] = None
    owner_id: int


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    date_of_birth: Optional[date] = None
    owner_id: Optional[int] = None


class OwnershipTransferRequest(BaseModel):
    new_owner_id: int


class PetResponse(PetBase):
    id: int

    model_config = {"from_attributes": True}
