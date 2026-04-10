from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Patient
from database import SessionLocal

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(Patient).count()
    if total == 0:
        return {"total": 0, "high_risk": 0, "medium_risk": 0, "coverage_rate": 0}
    high = db.query(Patient).filter(Patient.risk == "High").count()
    med  = db.query(Patient).filter(Patient.risk == "Medium").count()
    return {"total": total, "high_risk": high, "medium_risk": med,
            "coverage_rate": round((total - high) / total * 100, 1)}/
