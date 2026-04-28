from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.owner import Owner
from app.models.pet import Pet
from app.schemas.owner import OwnerCreate, OwnerUpdate, OwnerResponse
from app.schemas.pet import PetResponse

router = APIRouter(prefix="/owners", tags=["Owners"])


@router.post("/", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    if db.query(Owner).filter(Owner.email == owner.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_owner = Owner(**owner.model_dump())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


@router.get("/", response_model=List[OwnerResponse])
def list_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Owner).offset(skip).limit(limit).all()


@router.get("/{owner_id}", response_model=OwnerResponse)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner


@router.put("/{owner_id}", response_model=OwnerResponse)
def update_owner(owner_id: int, updates: OwnerUpdate, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(owner, field, value)
    db.commit()
    db.refresh(owner)
    return owner


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    db.delete(owner)
    db.commit()


@router.get("/{owner_id}/pets", response_model=List[PetResponse])
def get_owner_pets(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return db.query(Pet).filter(Pet.owner_id == owner_id).all()
