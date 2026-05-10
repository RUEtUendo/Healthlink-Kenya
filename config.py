"""
HealthLink Kenya — Centralized Configuration
All thresholds derived from thesis analysis (Chapters 4-6).
Environment variables override defaults for deployment flexibility.
"""
import os

# ── Distance Thresholds (§6.3 GAM Analysis) ─────────────────────
# The GAM curve identifies 35 km as the boundary of meaningful access.
# Winsorisation capped distance_from_facility at 5th/95th percentiles (0.40–35.00 km).
GAM_DISTANCE_THRESHOLD_KM = float(os.getenv("GAM_DISTANCE_THRESHOLD_KM", "35.0"))
SAFE_ZONE_KM = float(os.getenv("SAFE_ZONE_KM", "15.0"))
TRANSITION_ZONE_KM = float(os.getenv("TRANSITION_ZONE_KM", "35.0"))
WINSORIZE_LOWER_KM = float(os.getenv("WINSORIZE_LOWER_KM", "0.40"))
WINSORIZE_UPPER_KM = float(os.getenv("WINSORIZE_UPPER_KM", "35.0"))

# ── Risk Scoring Thresholds ──────────────────────────────────────
# §6.7: Retention model T1 threshold (F1-optimal = 0.95)
RETENTION_CLASSIFICATION_THRESHOLD = float(os.getenv("RETENTION_THRESHOLD", "0.95"))
# Dashboard alert threshold for dropout risk
HIGH_RISK_DROPOUT_THRESHOLD = float(os.getenv("HIGH_RISK_DROPOUT_THRESHOLD", "0.70"))

# ── Model Performance Baselines (§6.4) ───────────────────────────
# Stage 1 Access Model
ACCESS_MODEL_AUC = 0.8144
ACCESS_MODEL_F1 = 0.8091
ACCESS_MODEL_BRIER = 0.1760
# Stage 2 Retention Model
RETENTION_MODEL_AUC = 0.8510
RETENTION_MODEL_F1 = 0.9836

# ── Class Imbalance Parameters (§6.5) ────────────────────────────
STAGE1_IMBALANCE_RATIO = 4.5
STAGE2_IMBALANCE_RATIO = 28.74
SCALE_POS_WEIGHT_STAGE1 = float(os.getenv("SCALE_POS_WEIGHT", "4.5"))

# ── SHAP Attribution Baselines (§6.2) ────────────────────────────
PREDISPOSING_SHAP_WEIGHT = 73.2  # %
ENABLING_SHAP_WEIGHT = 26.8      # %
DISTANCE_SHAP_WEIGHT = 12.9      # % — single most influential feature

# ── Dataset Statistics (§6.1) ────────────────────────────────────
ORIGINAL_SURVEY_RECORDS = 99_031
CLEANED_ANALYTICAL_RECORDS = 73_059
RECORDS_DROPPED_PERCENT = 26.2
URBAN_PROXIMITY_PARADOX_CASES = 3_484

# ── Pipeline Paths ───────────────────────────────────────────────
ACCESS_PIPELINE_PATH = os.getenv("ACCESS_PIPELINE_PATH", "health_access_pipeline.pkl")
RETENTION_PIPELINE_PATH = os.getenv("RETENTION_PIPELINE_PATH", "retention_pipeline.pkl")
GAM_MODEL_PATH = os.getenv("GAM_MODEL_PATH", "gam_distance_model.pkl")

# ── Auth ─────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "healthlink-secret-2026")
JWT_ALGORITHM = os.getenv("ALGORITHM", "HS256")
JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES", "480"))

# ── Nakuru County Pilot ──────────────────────────────────────────
PILOT_COUNTY = "Nakuru"
PILOT_SUB_COUNTIES = [
    "Nakuru Town", "Rongai", "Subukia", "Molo",
    "Naivasha", "Gilgil", "Bahati", "Njoro", "Kuresoi"
]

# ── Facility Reference Coordinates (Nakuru County) ───────────────
# §6.6: Key facilities for the paradox patient finder
REFERENCE_FACILITIES = [
    {"name": "Nakuru Level 5 Referral Hospital", "distance_km": 2.4},
    {"name": "Njoro Health Centre", "distance_km": 9.1},
    {"name": "Gilgil District Hospital", "distance_km": 18.7},
]
