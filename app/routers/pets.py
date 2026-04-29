import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.pet import Pet
from app.models.owner import Owner
from app.models.vaccination import Vaccination
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.schemas.vaccination import VaccinationCreate, VaccinationUpdate, VaccinationResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pets", tags=["Pets"])


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    if not db.query(Owner).filter(Owner.id == pet.owner_id).first():
        logger.warning(f"Failed to create pet: Owner {pet.owner_id} not found")
        raise HTTPException(status_code=404, detail="Owner not found")
    db_pet = Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    logger.info(f"Created pet with ID: {db_pet.id} for owner: {pet.owner_id}")
    return db_pet


@router.get("/", response_model=List[PetResponse])
def list_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Pet).offset(skip).limit(limit).all()


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        logger.warning(f"Pet not found: {pet_id}")
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, updates: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        logger.warning(f"Pet not found for update: {pet_id}")
        raise HTTPException(status_code=404, detail="Pet not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(pet, field, value)
    db.commit()
    db.refresh(pet)
    logger.info(f"Updated pet with ID: {pet_id}")
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        logger.warning(f"Pet not found for deletion: {pet_id}")
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    logger.info(f"Deleted pet with ID: {pet_id}")


@router.get("/{pet_id}/vaccinations", response_model=List[VaccinationResponse])
def list_pet_vaccinations(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        logger.warning(f"Pet not found for vaccinations list: {pet_id}")
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet.vaccinations


@router.post("/{pet_id}/vaccinations", response_model=VaccinationResponse, status_code=status.HTTP_201_CREATED)
def add_pet_vaccination(pet_id: int, vaccination: VaccinationCreate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        logger.warning(f"Pet not found for adding vaccination: {pet_id}")
        raise HTTPException(status_code=404, detail="Pet not found")
    db_vaccination = Vaccination(**vaccination.model_dump(), pet_id=pet_id)
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    logger.info(f"Added vaccination {db_vaccination.id} to pet {pet_id}")
    return db_vaccination


@router.put("/{pet_id}/vaccinations/{vaccination_id}", response_model=VaccinationResponse)
def update_pet_vaccination(pet_id: int, vaccination_id: int, updates: VaccinationUpdate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        logger.warning(f"Pet not found for updating vaccination: {pet_id}")
        raise HTTPException(status_code=404, detail="Pet not found")
    db_vaccination = db.query(Vaccination).filter(Vaccination.id == vaccination_id, Vaccination.pet_id == pet_id).first()
    if not db_vaccination:
        logger.warning(f"Vaccination {vaccination_id} not found for pet {pet_id}")
        raise HTTPException(status_code=404, detail="Vaccination not found")
    
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(db_vaccination, field, value)
    
    db.commit()
    db.refresh(db_vaccination)
    logger.info(f"Updated vaccination {vaccination_id} for pet {pet_id}")
    return db_vaccination


@router.delete("/{pet_id}/vaccinations/{vaccination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet_vaccination(pet_id: int, vaccination_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        logger.warning(f"Pet not found for deleting vaccination: {pet_id}")
        raise HTTPException(status_code=404, detail="Pet not found")
    db_vaccination = db.query(Vaccination).filter(Vaccination.id == vaccination_id, Vaccination.pet_id == pet_id).first()
    if not db_vaccination:
        logger.warning(f"Vaccination {vaccination_id} not found for pet {pet_id}")
        raise HTTPException(status_code=404, detail="Vaccination not found")
    
    db.delete(db_vaccination)
    db.commit()
    logger.info(f"Deleted vaccination {vaccination_id} for pet {pet_id}")
