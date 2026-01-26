from sqlalchemy.orm import Session
from app.models.subject import Subject
from app.schema import subject_schema as schemas
from app.core.logger import logger


def create_subject(db: Session, subject: schemas.SubjectCreate):
    logger.debug(f"Creating subject in database: {subject.name}")
    db_subject = Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    logger.debug(f"Subject created with ID: {db_subject.id}")
    return db_subject


def get_subject(db: Session, subject_id: int):
    logger.debug(f"Querying subject with ID: {subject_id}")
    return db.query(Subject).filter(Subject.id == subject_id).first()


def get_subjects(db: Session):
    logger.debug("Querying all subjects from database")
    return db.query(Subject).all()


def delete_subject(db: Session, subject_id: int):
    logger.debug(f"Deleting subject with ID: {subject_id}")
    subject = get_subject(db, subject_id)
    if subject:
        db.delete(subject)
        db.commit()
        logger.debug(f"Subject with ID {subject_id} deleted from database")
    return subject
