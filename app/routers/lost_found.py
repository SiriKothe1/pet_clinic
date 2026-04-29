import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.lost_found_pet import LostFoundPet
from app.schemas.lost_found_pet import LostFoundPetCreate, LostFoundPetUpdate, LostFoundPetResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/lost-found", tags=["Lost & Found"])


@router.post("/", response_model=LostFoundPetResponse, status_code=status.HTTP_201_CREATED)
def create_report(report: LostFoundPetCreate, db: Session = Depends(get_db)):
    db_report = LostFoundPet(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    logger.info(f"Created {report.report_type} report with ID: {db_report.id}")
    return db_report


@router.get("/", response_model=List[LostFoundPetResponse])
def list_reports(
    report_type: Optional[str] = Query(None, pattern="^(LOST|FOUND)$"),
    is_resolved: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(LostFoundPet)
    if report_type:
        query = query.filter(LostFoundPet.report_type == report_type)
    if is_resolved is not None:
        query = query.filter(LostFoundPet.is_resolved == is_resolved)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{report_id}", response_model=LostFoundPetResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(LostFoundPet).filter(LostFoundPet.id == report_id).first()
    if not report:
        logger.warning(f"Lost/Found report not found: {report_id}")
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.put("/{report_id}", response_model=LostFoundPetResponse)
def update_report(report_id: int, updates: LostFoundPetUpdate, db: Session = Depends(get_db)):
    report = db.query(LostFoundPet).filter(LostFoundPet.id == report_id).first()
    if not report:
        logger.warning(f"Lost/Found report not found for update: {report_id}")
        raise HTTPException(status_code=404, detail="Report not found")
    
    for field, value in updates.model_dump(exclude_none=True).items():
        setattr(report, field, value)
    
    db.commit()
    db.refresh(report)
    logger.info(f"Updated report with ID: {report_id}")
    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(LostFoundPet).filter(LostFoundPet.id == report_id).first()
    if not report:
        logger.warning(f"Lost/Found report not found for deletion: {report_id}")
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    logger.info(f"Deleted report with ID: {report_id}")
