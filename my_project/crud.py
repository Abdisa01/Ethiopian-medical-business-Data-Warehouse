# crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from my_project import models

def get_medical_data(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MedicalData).offset(skip).limit(limit).all()
