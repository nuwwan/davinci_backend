from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..controllers import SubjectController
from ..database import get_db
from ..schema import SubjectSchema as schema

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", response_model=schema.SubjectResponse)
def create_subject(
    subject: schema.SubjectCreate, db: Session = Depends(get_db)
):
    return SubjectController.create_subject(db, subject)


@router.get("/", response_model=list[schema.SubjectResponse])
def list_subjects(db: Session = Depends(get_db)):
    return SubjectController.get_subjects(db)


@router.get("/{subject_id}", response_model=schema.SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = SubjectController.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = SubjectController.delete_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Deleted successfully"}
