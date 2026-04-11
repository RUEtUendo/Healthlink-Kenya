import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import joblib
import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# --- 1. DATABASE & ROUTER IMPORTS ---
from routers import auth, patients, analytics
from database import engine
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

# --- 2. PROFESSIONAL LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("HealthcareAPI")

# --- 3. UNIVERSAL NLP PREPROCESSING MODULE ---
for package in ['tokenizers/punkt', 'corpora/wordnet', 'tokenizers/punkt_tab']:
    try:
        nltk.data.find(package)
    except LookupError:
        nltk.download(package.split('/')[-1], quiet=True)

_lemmatizer = WordNetLemmatizer()
_base_stopwords = {
    'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'him', 'his', 'she', 'her', 
    'it', 'its', 'they', 'them', 'their', 'what', 'which', 'who', 'this', 'that', 
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 
    'does', 'did', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
    'of', 'at', 'by', 'for', 'with', 'about', 'to', 'from', 'in', 'out', 'on'
}
_custom_stopwords = {'study', 'method', 'result', 'patient', 'group', 'clinical'}
FINAL_STOPWORDS = _base_stopwords.union(_custom_stopwords)

def clean_and_tokenize(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    tokens = word_tokenize(text)
    clean_tokens = [
        _lemmatizer.lemmatize(token) for token in tokens
        if token not in FINAL_STOPWORDS and len(token) > 2
    ]
    return " ".join(clean_tokens)

# --- 4. INITIALIZE FASTAPI & MIDDLEWARE ---
app = FastAPI(
    title="HealthLink Kenya API & Analytics Engine",
    version="2.0",
    description="UN-Grade Microservice for Predictive Healthcare Analytics & NLP"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include existing routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(analytics.router)

# --- 5. LOAD MACHINE LEARNING MODEL ---
try:
    model = joblib.load("xgboost_access_model.pkl")
    logger.info("✅ XGBoost Prediction Model loaded successfully")
except Exception as e:
    model = None
    logger.error(f"⚠️ Warning: Model not loaded. {e}")

# --- 6. DATA CONTRACT ---
class PatientData(BaseModel):
    distance_km: float = Field(..., ge=0.0, description="Distance in km to facility")
    age_group: str = Field(..., description="Age category")
    gender: str = Field(..., description="Administrative gender")
    wealth_index: str = Field(..., description="Socioeconomic quintile")
    insurance_status: int = Field(..., ge=0, le=1, description="0 = Uninsured, 1 = Insured")
    residential_area_group: str = Field(..., description="Urban or Rural residence")
    survey_weight: float = Field(default=1.0, description="Sampling weight")
    clinical_notes: Optional[str] = Field(default="", description="Optional context")

# --- 7. ENDPOINTS ---
@app.get("/", tags=["System"])
def read_root():
    return {"status": "HealthLink API is live and running!"}

@app.post("/predict_access", tags=["Analytics"])
def predict_access(patient: PatientData):
    if model is None:
        raise HTTPException(status_code=500, detail="ML Model is unavailable.")

    try:
        processed_notes = clean_and_tokenize(patient.clinical_notes) if patient.clinical_notes else None
        model_input = patient.model_dump(exclude={"clinical_notes"})
        input_df = pd.DataFrame([model_input])
        
        raw_probability = float(model.predict_proba(input_df)[0][1])
        multiplier = 1.0
        
        if patient.insurance_status == 0: multiplier *= 0.55 
            
        wealth_lower = patient.wealth_index.lower()
        if any(w in wealth_lower for w in ["poor", "lowest", "low"]): multiplier *= 0.75
        elif any(w in wealth_lower for w in ["rich", "highest", "high"]): multiplier *= 1.20

        age_str = patient.age_group.lower()
        if any(a in age_str for a in ["50", "60", "70", "80", "90", "older", "+"]): multiplier *= 0.70
        elif any(a in age_str for a in ["0-4", "under 5", "infant"]): multiplier *= 0.80

        if patient.distance_km > 50: multiplier *= 0.40
        elif patient.distance_km > 15: multiplier *= 0.80

        final_probability = max(0.01, min(raw_probability * multiplier, 0.99))
        final_prediction = 1 if final_probability >= 0.50 else 0

        return {
            "prediction": final_prediction,
            "probability": round(final_probability * 100, 2),
            "nlp_analysis": {
                "original_notes_provided": bool(patient.clinical_notes),
                "cleaned_keywords": processed_notes
            },
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
