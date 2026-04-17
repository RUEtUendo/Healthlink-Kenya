from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, patients, analytics
from database import engine, SessionLocal
import models
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HealthLink Kenya API", version="1.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(analytics.router)

@app.on_event("startup")
def seed_on_startup():
    db = SessionLocal()
    try:
        if db.query(models.Patient).count() > 0:
            return
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        users = [
            models.User(name="Amara Ochieng", email="amara@healthlink.ke",
                hashed_password=pwd.hash("password123"), role="social_worker"),
            models.User(name="Joyce Mutua", email="joyce@healthlink.ke",
                hashed_password=pwd.hash("password123"), role="social_worker"),
            models.User(name="David Muriithi", email="david@healthlink.ke",
                hashed_password=pwd.hash("password123"), role="social_worker"),
            models.User(name="Faith Wanjiku", email="faith@healthlink.ke",
                hashed_password=pwd.hash("password123"), role="social_worker"),
            models.User(name="James Kipkemboi", email="james@healthlink.ke",
                hashed_password=pwd.hash("password123"), role="social_worker"),
            models.User(name="Rose Kimani", email="rose@healthlink.ke",
                hashed_password=pwd.hash("password123"), role="social_worker"),
            models.User(name="Supervisor Admin", email="admin@healthlink.ke",
                hashed_password=pwd.hash("admin123"), role="supervisor"),
        ]
        db.add_all(users)
        db.commit()

        patients_list = [
            models.Patient(id="HH-NK-00234",name="Rutendo Nyamari",age=34,gender="F",sub_county="Bahati",condition="Hypertension",risk="High",distance_km=41.2,insurance="None",assigned_worker_id=1),
            models.Patient(id="HH-NK-00891",name="Joseph Mwangi",age=52,gender="M",sub_county="Njoro",condition="Diabetes T2",risk="High",distance_km=28.5,insurance="None",assigned_worker_id=1),
            models.Patient(id="HH-NK-01102",name="Aisha Karimi",age=29,gender="F",sub_county="Rongai",condition="Maternal Care",risk="Medium",distance_km=19.3,insurance="NHIF",assigned_worker_id=5),
            models.Patient(id="HH-NK-00455",name="Samuel Otieno",age=45,gender="M",sub_county="Subukia",condition="TB Follow-up",risk="Medium",distance_km=36.7,insurance="None",assigned_worker_id=4),
            models.Patient(id="HH-NK-00678",name="Fatuma Hassan",age=38,gender="F",sub_county="Nakuru Town",condition="HIV Care",risk="Low",distance_km=3.1,insurance="Partial",assigned_worker_id=1),
            models.Patient(id="HH-NK-00312",name="Grace Wambui",age=61,gender="F",sub_county="Molo",condition="Hypertension",risk="High",distance_km=52.3,insurance="None",assigned_worker_id=3),
            models.Patient(id="HH-NK-00549",name="Daniel Kimani",age=44,gender="M",sub_county="Gilgil",condition="Diabetes T2",risk="Medium",distance_km=22.1,insurance="NHIF",assigned_worker_id=2),
            models.Patient(id="HH-NK-00763",name="Susan Njoki",age=33,gender="F",sub_county="Bahati",condition="Maternal Care",risk="Low",distance_km=7.8,insurance="NHIF",assigned_worker_id=1),
            models.Patient(id="HH-NK-00988",name="Peter Koech",age=58,gender="M",sub_county="Kuresoi",condition="TB Screening",risk="High",distance_km=47.0,insurance="None",assigned_worker_id=3),
            models.Patient(id="HH-NK-01055",name="Mary Auma",age=27,gender="F",sub_county="Rongai",condition="Child Nutrition",risk="Low",distance_km=11.2,insurance="NHIF",assigned_worker_id=5),
            models.Patient(id="HH-NK-01201",name="Charles Njoroge",age=49,gender="M",sub_county="Njoro",condition="Mental Health",risk="Medium",distance_km=31.4,insurance="None",assigned_worker_id=1),
            models.Patient(id="HH-NK-01348",name="Alice Chebet",age=36,gender="F",sub_county="Subukia",condition="Hypertension",risk="High",distance_km=39.8,insurance="None",assigned_worker_id=4),
            models.Patient(id="HH-NK-01420",name="Hassan Mwangi",age=41,gender="M",sub_county="Naivasha",condition="HIV Care",risk="Medium",distance_km=18.5,insurance="Partial",assigned_worker_id=6),
            models.Patient(id="HH-NK-01502",name="Joyce Kamau",age=55,gender="F",sub_county="Naivasha",condition="Maternal Anemia",risk="High",distance_km=61.0,insurance="None",assigned_worker_id=6),
            models.Patient(id="HH-NK-01630",name="Eric Mutua",age=31,gender="M",sub_county="Molo",condition="TB Follow-up",risk="High",distance_km=44.5,insurance="None",assigned_worker_id=3),
            models.Patient(id="HH-NK-01744",name="Janet Wanyama",age=48,gender="F",sub_county="Kuresoi",condition="Diabetes T2",risk="Medium",distance_km=25.8,insurance="NHIF",assigned_worker_id=3),
            models.Patient(id="HH-NK-01815",name="Michael Odhiambo",age=23,gender="M",sub_county="Nakuru Town",condition="HIV Care",risk="Low",distance_km=5.5,insurance="NHIF",assigned_worker_id=1),
            models.Patient(id="HH-NK-01900",name="Esther Waweru",age=67,gender="F",sub_county="Subukia",condition="Hypertension",risk="High",distance_km=38.9,insurance="None",assigned_worker_id=4),
            models.Patient(id="HH-NK-02010",name="Philip Kariuki",age=39,gender="M",sub_county="Njoro",condition="Child Nutrition",risk="Medium",distance_km=28.1,insurance="NHIF",assigned_worker_id=1),
            models.Patient(id="HH-NK-02155",name="Catherine Mutai",age=52,gender="F",sub_county="Rongai",condition="TB Screening",risk="High",distance_km=49.2,insurance="None",assigned_worker_id=5),
            models.Patient(id="HH-NK-02231",name="Wilson Otieno",age=29,gender="M",sub_county="Nakuru Town",condition="Mental Health",risk="Low",distance_km=4.2,insurance="NHIF",assigned_worker_id=1),
            models.Patient(id="HH-NK-02340",name="Priscilla Njoroge",age=44,gender="F",sub_county="Gilgil",condition="Hypertension",risk="Medium",distance_km=15.6,insurance="None",assigned_worker_id=2),
            models.Patient(id="HH-NK-02410",name="Bernard Kamau",age=63,gender="M",sub_county="Bahati",condition="TB Follow-up",risk="High",distance_km=33.2,insurance="None",assigned_worker_id=1),
            models.Patient(id="HH-NK-02512",name="Lilian Omondi",age=26,gender="F",sub_county="Naivasha",condition="Maternal Care",risk="Low",distance_km=9.8,insurance="NHIF",assigned_worker_id=6),
            models.Patient(id="HH-NK-02623",name="Francis Kiprotich",age=57,gender="M",sub_county="Kuresoi",condition="Hypertension",risk="High",distance_km=55.4,insurance="None",assigned_worker_id=3),
            models.Patient(id="HH-NK-02710",name="Mercy Njeri",age=34,gender="F",sub_county="Molo",condition="HIV Care",risk="Medium",distance_km=21.3,insurance="Partial",assigned_worker_id=3),
            models.Patient(id="HH-NK-02801",name="Stanley Wachira",age=48,gender="M",sub_county="Subukia",condition="Diabetes T2",risk="Medium",distance_km=27.6,insurance="NHIF",assigned_worker_id=4),
            models.Patient(id="HH-NK-02900",name="Agnes Cherop",age=72,gender="F",sub_county="Rongai",condition="Hypertension",risk="High",distance_km=42.7,insurance="None",assigned_worker_id=5),
            models.Patient(id="HH-NK-03010",name="Collins Mugo",age=19,gender="M",sub_county="Nakuru Town",condition="HIV Screening",risk="Low",distance_km=2.8,insurance="None",assigned_worker_id=1),
            models.Patient(id="HH-NK-03120",name="Veronica Akinyi",age=41,gender="F",sub_county="Gilgil",condition="Child Nutrition",risk="Medium",distance_km=16.9,insurance="NHIF",assigned_worker_id=2),
        ]
        db.add_all(patients_list)
        db.commit()
        print("✅ Database seeded on startup — 30 patients loaded")
    except Exception as e:
        print(f"Seed error: {e}")
        db.rollback()
    finally:
        db.close()
