from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/", response_model=schemas.SubjectResponse)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)

@router.get("/", response_model=list[schemas.SubjectResponse])
def list_subjects(db: Session = Depends(get_db)):
    return crud.get_subjects(db)

@router.get("/{subject_id}", response_model=schemas.SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = crud.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = crud.delete_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Deleted successfully"}