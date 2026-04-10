from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import Patient
from database import SessionLocal

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_patients(
    risk: str = Query(None),
    sub_county: str = Query(None),
    search: str = Query(None),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Patient)
    if risk:       query = query.filter(Patient.risk == risk)
    if sub_county: query = query.filter(Patient.sub_county == sub_county)
    if search:     query = query.filter(Patient.name.ilike(f"%{search}%"))
    total = query.count()
    patients = query.offset((page-1)*page_size).limit(page_size).all()
    return {"total": total, "page": page, "data": patients}

@router.get("/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient