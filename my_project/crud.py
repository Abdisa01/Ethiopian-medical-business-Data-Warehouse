# crud.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy.orm import Session
from my_project.models import MedicalData

def get_medical_data(db: Session):
    data = db.query(MedicalData).limit(15).all()
    
    return [
        {
            "id": item.id,
            "channel_title": item.channel_title,
            "channel_username": item.channel_username,
            "message": item.message,
            "date": item.date,
            "mediapath": item.mediapath
        }
        for item in data
    ]
