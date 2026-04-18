"""
HealthLink Kenya — FastAPI Backend
Auto-seeds 5 social workers + 25 patients on every startup if DB is empty
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from database import engine, SessionLocal, Base
import models
from passlib.context import CryptContext

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HealthLink Kenya API", version="1.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── DB dependency ──────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── STARTUP SEEDER ─────────────────────────────────────────────
@app.on_event("startup")
def seed_database():
    db = SessionLocal()
    try:
        if db.query(models.Patient).count() > 0:
            print("✅ Database already seeded.")
            return

        # 5 Social workers + 1 supervisor
        workers = [
            models.User(id=1, name="Amara Ochieng",   email="amara@healthlink.ke",   hashed_password=pwd_ctx.hash("sw2026"),    role="social_worker",  sub_county="Bahati",      phone="+254 712 100 001"),
            models.User(id=2, name="Joyce Mutua",     email="joyce@healthlink.ke",   hashed_password=pwd_ctx.hash("sw2026"),    role="social_worker",  sub_county="Njoro",       phone="+254 712 100 002"),
            models.User(id=3, name="David Muriithi",  email="david@healthlink.ke",   hashed_password=pwd_ctx.hash("sw2026"),    role="social_worker",  sub_county="Molo",        phone="+254 712 100 003"),
            models.User(id=4, name="Faith Wanjiku",   email="faith@healthlink.ke",   hashed_password=pwd_ctx.hash("sw2026"),    role="social_worker",  sub_county="Subukia",     phone="+254 712 100 004"),
            models.User(id=5, name="James Kipkemboi", email="james@healthlink.ke",   hashed_password=pwd_ctx.hash("sw2026"),    role="social_worker",  sub_county="Kuresoi",     phone="+254 712 100 005"),
            models.User(id=6, name="Supervisor Admin",email="admin@healthlink.ke",   hashed_password=pwd_ctx.hash("admin2026"), role="supervisor",     sub_county="Nakuru Town", phone="+254 712 100 006"),
        ]
        db.add_all(workers)
        db.commit()

        # 25 patients — Amara (worker 1) has 5, others have 4 each = 21, plus 4 unassigned to show coverage
        patients = [
            # ── AMARA OCHIENG (Worker 1) — Bahati ──────────────────
            models.Patient(id="HH-NK-00234", name="Rutendo Nyamari",   age=34, gender="F", sub_county="Bahati",      condition="Hypertension",   risk="High",   distance_km=41.2, insurance="None",    last_visit="2026-02-10", assigned_worker_id=1, latitude=-0.154, longitude=36.140),
            models.Patient(id="HH-NK-00763", name="Susan Njoki",       age=33, gender="F", sub_county="Bahati",      condition="Maternal Care",  risk="Low",    distance_km=7.8,  insurance="NHIF",    last_visit="2026-03-20", assigned_worker_id=1, latitude=-0.185, longitude=36.130),
            models.Patient(id="HH-NK-02410", name="Bernard Kamau",     age=63, gender="M", sub_county="Bahati",      condition="TB Follow-up",   risk="High",   distance_km=33.2, insurance="None",    last_visit="2026-01-05", assigned_worker_id=1, latitude=-0.165, longitude=36.125),
            models.Patient(id="HH-NK-00678", name="Fatuma Hassan",     age=38, gender="F", sub_county="Nakuru Town", condition="HIV Care",       risk="Low",    distance_km=3.1,  insurance="Partial", last_visit="2026-03-25", assigned_worker_id=1, latitude=-0.303, longitude=36.075),
            models.Patient(id="HH-NK-01815", name="Michael Odhiambo", age=23, gender="M", sub_county="Nakuru Town", condition="HIV Care",       risk="Low",    distance_km=5.5,  insurance="NHIF",    last_visit="2026-03-18", assigned_worker_id=1, latitude=-0.295, longitude=36.082),

            # ── JOYCE MUTUA (Worker 2) — Njoro ─────────────────────
            models.Patient(id="HH-NK-00891", name="Joseph Mwangi",    age=52, gender="M", sub_county="Njoro",       condition="Diabetes T2",    risk="High",   distance_km=28.5, insurance="None",    last_visit="2026-01-15", assigned_worker_id=2, latitude=-0.368, longitude=35.970),
            models.Patient(id="HH-NK-02010", name="Philip Kariuki",   age=39, gender="M", sub_county="Njoro",       condition="Child Nutrition",risk="Medium", distance_km=28.1, insurance="NHIF",    last_visit="2026-02-28", assigned_worker_id=2, latitude=-0.350, longitude=35.960),
            models.Patient(id="HH-NK-01201", name="Charles Njoroge",  age=49, gender="M", sub_county="Njoro",       condition="Mental Health",  risk="Medium", distance_km=31.4, insurance="None",    last_visit="2026-02-14", assigned_worker_id=2, latitude=-0.375, longitude=35.980),
            models.Patient(id="HH-NK-02340", name="Priscilla Njoroge",age=44, gender="F", sub_county="Gilgil",      condition="Hypertension",   risk="Medium", distance_km=15.6, insurance="None",    last_visit="2026-03-01", assigned_worker_id=2, latitude=-0.480, longitude=36.300),

            # ── DAVID MURIITHI (Worker 3) — Molo ───────────────────
            models.Patient(id="HH-NK-00312", name="Grace Wambui",     age=61, gender="F", sub_county="Molo",        condition="Hypertension",   risk="High",   distance_km=52.3, insurance="None",    last_visit="2026-01-20", assigned_worker_id=3, latitude=-0.270, longitude=35.760),
            models.Patient(id="HH-NK-01630", name="Eric Mutua",       age=31, gender="M", sub_county="Molo",        condition="TB Follow-up",   risk="High",   distance_km=44.5, insurance="None",    last_visit="2025-12-10", assigned_worker_id=3, latitude=-0.265, longitude=35.750),
            models.Patient(id="HH-NK-02710", name="Mercy Njeri",      age=34, gender="F", sub_county="Molo",        condition="HIV Care",       risk="Medium", distance_km=21.3, insurance="Partial", last_visit="2026-03-05", assigned_worker_id=3, latitude=-0.280, longitude=35.770),
            models.Patient(id="HH-NK-00988", name="Peter Koech",      age=58, gender="M", sub_county="Kuresoi",     condition="TB Screening",   risk="High",   distance_km=47.0, insurance="None",    last_visit="2025-11-30", assigned_worker_id=3, latitude=-0.420, longitude=35.690),

            # ── FAITH WANJIKU (Worker 4) — Subukia ─────────────────
            models.Patient(id="HH-NK-00455", name="Samuel Otieno",    age=45, gender="M", sub_county="Subukia",     condition="TB Follow-up",   risk="Medium", distance_km=36.7, insurance="None",    last_visit="2026-02-22", assigned_worker_id=4, latitude=0.020,  longitude=36.220),
            models.Patient(id="HH-NK-01348", name="Alice Chebet",     age=36, gender="F", sub_county="Subukia",     condition="Hypertension",   risk="High",   distance_km=39.8, insurance="None",    last_visit="2026-01-18", assigned_worker_id=4, latitude=0.015,  longitude=36.215),
            models.Patient(id="HH-NK-01900", name="Esther Waweru",    age=67, gender="F", sub_county="Subukia",     condition="Hypertension",   risk="High",   distance_km=38.9, insurance="None",    last_visit="2025-12-20", assigned_worker_id=4, latitude=0.025,  longitude=36.230),
            models.Patient(id="HH-NK-02801", name="Stanley Wachira",  age=48, gender="M", sub_county="Subukia",     condition="Diabetes T2",    risk="Medium", distance_km=27.6, insurance="NHIF",    last_visit="2026-03-10", assigned_worker_id=4, latitude=0.010,  longitude=36.210),

            # ── JAMES KIPKEMBOI (Worker 5) — Kuresoi / Rongai ──────
            models.Patient(id="HH-NK-01102", name="Aisha Karimi",     age=29, gender="F", sub_county="Rongai",      condition="Maternal Care",  risk="Medium", distance_km=19.3, insurance="NHIF",    last_visit="2026-03-22", assigned_worker_id=5, latitude=-0.190, longitude=35.980),
            models.Patient(id="HH-NK-01055", name="Mary Auma",        age=27, gender="F", sub_county="Rongai",      condition="Child Nutrition",risk="Low",    distance_km=11.2, insurance="NHIF",    last_visit="2026-03-28", assigned_worker_id=5, latitude=-0.150, longitude=36.020),
            models.Patient(id="HH-NK-02155", name="Catherine Mutai",  age=52, gender="F", sub_county="Rongai",      condition="TB Screening",   risk="High",   distance_km=49.2, insurance="None",    last_visit="2025-12-05", assigned_worker_id=5, latitude=-0.175, longitude=35.990),
            models.Patient(id="HH-NK-02623", name="Francis Kiprotich",age=57, gender="M", sub_county="Kuresoi",     condition="Hypertension",   risk="High",   distance_km=55.4, insurance="None",    last_visit="2025-11-15", assigned_worker_id=5, latitude=-0.410, longitude=35.680),

            # ── ADDITIONAL PATIENTS (shared / Naivasha) ─────────────
            models.Patient(id="HH-NK-01420", name="Hassan Mwangi",    age=41, gender="M", sub_county="Naivasha",    condition="HIV Care",       risk="Medium", distance_km=18.5, insurance="Partial", last_visit="2026-03-12", assigned_worker_id=1, latitude=-0.715, longitude=36.434),
            models.Patient(id="HH-NK-01502", name="Joyce Kamau",      age=55, gender="F", sub_county="Naivasha",    condition="Maternal Anemia",risk="High",   distance_km=61.0, insurance="None",    last_visit="2025-11-28", assigned_worker_id=2, latitude=-0.720, longitude=36.440),
            models.Patient(id="HH-NK-02512", name="Lilian Omondi",    age=26, gender="F", sub_county="Naivasha",    condition="Maternal Care",  risk="Low",    distance_km=9.8,  insurance="NHIF",    last_visit="2026-03-30", assigned_worker_id=5, latitude=-0.710, longitude=36.428),
            models.Patient(id="HH-NK-02231", name="Wilson Otieno",    age=29, gender="M", sub_county="Nakuru Town", condition="Mental Health",  risk="Low",    distance_km=4.2,  insurance="NHIF",    last_visit="2026-03-15", assigned_worker_id=1, latitude=-0.295, longitude=36.078),
            models.Patient(id="HH-NK-00549", name="Daniel Kimani",    age=44, gender="M", sub_county="Gilgil",      condition="Diabetes T2",    risk="Medium", distance_km=22.1, insurance="NHIF",    last_visit="2026-02-18", assigned_worker_id=2, latitude=-0.480, longitude=36.300),
        ]
        db.add_all(patients)
        db.commit()
        print(f"✅ Seeded {len(workers)} workers and {len(patients)} patients")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed error: {e}")
    finally:
        db.close()

# ── SCHEMAS ────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    distance_km: float
    age_group: str
    gender: str
    wealth_index: str
    insurance_status: int
    residential_area_group: str
    survey_weight: float = 1.0

# ── ROUTES ────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "HealthLink Kenya API running", "docs": "/docs"}

@app.get("/patients/")
def get_patients(
    page: int = 1,
    page_size: int = 10,
    risk: Optional[str] = None,
    sub_county: Optional[str] = None,
    search: Optional[str] = None,
    worker_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(models.Patient)
    if risk:      q = q.filter(models.Patient.risk == risk)
    if sub_county:q = q.filter(models.Patient.sub_county == sub_county)
    if worker_id: q = q.filter(models.Patient.assigned_worker_id == worker_id)
    if search:
        s = f"%{search}%"
        q = q.filter(
            models.Patient.name.ilike(s) |
            models.Patient.id.ilike(s) |
            models.Patient.sub_county.ilike(s) |
            models.Patient.condition.ilike(s)
        )
    total = q.count()
    patients = q.offset((page-1)*page_size).limit(page_size).all()
    result = []
    for p in patients:
        worker = db.query(models.User).filter(models.User.id == p.assigned_worker_id).first()
        result.append({
            "id": p.id, "name": p.name, "age": p.age, "gender": p.gender,
            "sub_county": p.sub_county, "condition": p.condition, "risk": p.risk,
            "distance_km": p.distance_km, "insurance": p.insurance,
            "last_visit": str(p.last_visit) if p.last_visit else None,
            "latitude": p.latitude, "longitude": p.longitude,
            "assigned_worker_id": p.assigned_worker_id,
            "assigned_worker": worker.name if worker else "Unassigned",
            "worker_phone": worker.phone if worker else "",
            "worker_sub_county": worker.sub_county if worker else "",
        })
    return {"total": total, "page": page, "page_size": page_size, "data": result}

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p: raise HTTPException(status_code=404, detail="Patient not found")
    worker = db.query(models.User).filter(models.User.id == p.assigned_worker_id).first()
    return {
        "id": p.id, "name": p.name, "age": p.age, "gender": p.gender,
        "sub_county": p.sub_county, "condition": p.condition, "risk": p.risk,
        "distance_km": p.distance_km, "insurance": p.insurance,
        "last_visit": str(p.last_visit) if p.last_visit else None,
        "latitude": p.latitude, "longitude": p.longitude,
        "assigned_worker": worker.name if worker else "Unassigned",
        "worker_email": worker.email if worker else "",
        "worker_phone": worker.phone if worker else "",
        "worker_sub_county": worker.sub_county if worker else "",
    }

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    result = []
    for u in users:
        count = db.query(models.Patient).filter(models.Patient.assigned_worker_id == u.id).count()
        result.append({
            "id": u.id, "name": u.name, "email": u.email,
            "role": u.role, "sub_county": u.sub_county,
            "phone": u.phone, "patient_count": count
        })
    return result

@app.get("/analytics/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    total  = db.query(models.Patient).count()
    high   = db.query(models.Patient).filter(models.Patient.risk=="High").count()
    medium = db.query(models.Patient).filter(models.Patient.risk=="Medium").count()
    low    = db.query(models.Patient).filter(models.Patient.risk=="Low").count()
    nhif   = db.query(models.Patient).filter(models.Patient.insurance=="NHIF").count()
    far    = db.query(models.Patient).filter(models.Patient.distance_km > 35).count()
    cov    = round((1 - far/total)*100, 1) if total else 0
    return {
        "total": total, "high_risk": high, "medium_risk": medium,
        "low_risk": low, "nhif_count": nhif, "beyond_threshold": far,
        "coverage_rate": cov
    }

@app.post("/predict_access")
def predict_access(req: PredictRequest):
    """Simple rule-based prediction fallback if model not available"""
    try:
        import joblib, pandas as pd, os
        base = os.path.dirname(os.path.abspath(__file__))
        for path in ["health_access_pipeline.pkl", os.path.join(base,"health_access_pipeline.pkl")]:
            if os.path.exists(path):
                model = joblib.load(path)
                df = pd.DataFrame([{
                    "distance_from_facility": req.distance_km,
                    "insurance_status": "Yes" if req.insurance_status else "No",
                    "education_level": "Secondary",
                    "age_group": req.age_group,
                    "wealth_index1": req.wealth_index,
                    "resid": req.residential_area_group,
                    "gender": req.gender,
                    "working_status": "Unknown"
                }])
                prob = round(float(model.predict_proba(df)[0][1]) * 100, 1)
                return {"probability": prob, "source": "XGBoost"}
    except Exception as e:
        pass
    # Rule-based fallback
    base_score = 72.0
    if req.distance_km > 35: base_score -= (req.distance_km - 35) * 0.5
    if req.insurance_status == 0: base_score -= 8
    if req.wealth_index in ["Poorest","Poorer"]: base_score -= 6
    if req.residential_area_group == "Rural": base_score -= 4
    base_score = max(15, min(95, base_score))
    return {"probability": round(base_score, 1), "source": "rule-based fallback"}
