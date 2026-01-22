from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers import subject_controller
from app.database import get_db
from app.schema import subject_schema as schema

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", response_model=schema.SubjectResponse, status_code=201)
def create_subject(
    subject: schema.SubjectCreate, db: Session = Depends(get_db)
):
    return subject_controller.create_subject(db, subject)


@router.get("/", response_model=list[schema.SubjectResponse])
def list_subjects(db: Session = Depends(get_db)):
    return subject_controller.get_subjects(db)


@router.get("/{subject_id}", response_model=schema.SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = subject_controller.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = subject_controller.delete_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Deleted successfully"}
