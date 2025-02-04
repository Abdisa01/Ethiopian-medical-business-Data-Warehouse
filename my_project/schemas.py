# schemas.py
from pydantic import BaseModel
from datetime import datetime

class MedicalDataSchema(BaseModel):
    id: int
    channel_title: str
    channel_username: str
    message: str
    date: datetime
    mediapath: str

    class Config:
        from_attributes = True  
