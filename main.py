from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, patients, analytics
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HealthLink Kenya API", version="1.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(analytics.router)
#uvicorn main:app --reload
# Docs at http://localhost:8000/docs