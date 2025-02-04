# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from my_project.database import SessionLocal, engine

#from database import SessionLocal, engine
#from .database import SessionLocal, engine
from my_project import models, crud

#from . import models, crud

# Initialize FastAPI
app = FastAPI()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency for DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoint: Get medical data
@app.get("/data/")
def read_medical_data(db: Session = Depends(get_db)):
    return crud.get_medical_data(db)

# GUI: Render data in HTML
@app.get("/")
def homepage(request: Request, db: Session = Depends(get_db)):
    data = crud.get_medical_data(db)
    return templates.TemplateResponse("index.html", {"request": request, "data": data})
