# models.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from .database import Base

class MedicalData(Base):
    __tablename__ = "medical_data_tbl"

    id = Column(Integer, primary_key=True, index=True)
    channel_title = Column(String, index=True)
    channel_username = Column(String, index=True)
    message = Column(Text)
    date = Column(TIMESTAMP)
    mediapath = Column(String)
