from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers import subject_controller
from app.database import get_db
from app.schema import subject_schema as schema
from app.core.logger import logger

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", response_model=schema.SubjectResponse, status_code=201)
def create_subject(
    subject: schema.SubjectCreate, db: Session = Depends(get_db)
):
    logger.info(f"Creating subject: {subject.name}")
    try:
        result = subject_controller.create_subject(db, subject)
        logger.info(f"Subject created successfully with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating subject: {str(e)}")
        raise


@router.get("/", response_model=list[schema.SubjectResponse])
def list_subjects(db: Session = Depends(get_db)):
    logger.debug("Fetching all subjects")
    try:
        subjects = subject_controller.get_subjects(db)
        logger.info(f"Retrieved {len(subjects)} subjects")
        return subjects
    except Exception as e:
        logger.error(f"Error listing subjects: {str(e)}")
        raise


@router.get("/{subject_id}", response_model=schema.SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    logger.debug(f"Fetching subject with ID: {subject_id}")
    subject = subject_controller.get_subject(db, subject_id)
    if not subject:
        logger.warning(f"Subject with ID {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    logger.info(f"Retrieved subject with ID: {subject_id}")
    return subject


@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting subject with ID: {subject_id}")
    subject = subject_controller.delete_subject(db, subject_id)
    if not subject:
        logger.warning(f"Subject with ID {subject_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Subject not found")
    logger.info(f"Subject with ID {subject_id} deleted successfully")
    return {"message": "Deleted successfully"}
