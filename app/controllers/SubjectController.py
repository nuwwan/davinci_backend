from sqlalchemy.orm import Session
from ..models.Subject import Subject
from ..schema import SubjectSchema as schemas

def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()

def get_subjects(db: Session):
    return db.query(Subject).all()

def delete_subject(db: Session, subject_id: int):
    subject = get_subject(db, subject_id)
    if subject:
        db.delete(subject)
        db.commit()
    return subject