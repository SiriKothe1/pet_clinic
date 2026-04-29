from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.vaccination import Vaccination
from app.models.pet import Pet
from app.schemas.vaccination import VaccinationCreate, VaccinationUpdate, VaccinationResponse

router = APIRouter(prefix="/vaccinations", tags=["Vaccinations"])


@router.post("/", response_model=VaccinationResponse, status_code=status.HTTP_201_CREATED)
def create_vaccination(vaccination: VaccinationCreate, pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db_vaccination = Vaccination(**vaccination.model_dump(), pet_id=pet_id)
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    return db_vaccination


@router.get("/", response_model=List[VaccinationResponse])
def list_vaccinations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Vaccination).offset(skip).limit(limit).all()


@router.get("/{vaccination_id}", response_model=VaccinationResponse)
def get_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    vaccination = db.query(Vaccination).filter(Vaccination.id == vaccination_id).first()
    if not vaccination:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    return vaccination


@router.get("/pet/{pet_id}", response_model=List[VaccinationResponse])
def list_pet_vaccinations(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet.vaccinations


@router.put("/{vaccination_id}", response_model=VaccinationResponse)
def update_vaccination(vaccination_id: int, updates: VaccinationUpdate, db: Session = Depends(get_db)):
    db_vaccination = db.query(Vaccination).filter(Vaccination.id == vaccination_id).first()
    if not db_vaccination:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(db_vaccination, field, value)
    
    db.commit()
    db.refresh(db_vaccination)
    return db_vaccination


@router.delete("/{vaccination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    db_vaccination = db.query(Vaccination).filter(Vaccination.id == vaccination_id).first()
    if not db_vaccination:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    
    db.delete(db_vaccination)
    db.commit()
