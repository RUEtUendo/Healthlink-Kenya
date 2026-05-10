"""
HealthLink Kenya — Model Service Layer
Loads XGBoost pipelines at startup and provides inference functions.
Replaces the per-request try/except fallback pattern with robust, validated loading.
"""
import os
import logging
import pandas as pd

logger = logging.getLogger("healthlink.models")

# Module-level model references — set by load_models()
_access_model = None
_retention_model = None
_gam_model = None
_models_loaded = False


def load_models():
    """Load serialized pipelines at startup. Called once from main.py on_event('startup')."""
    global _access_model, _retention_model, _gam_model, _models_loaded
    import config

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Stage 1: Access Pipeline
    access_path = config.ACCESS_PIPELINE_PATH
    if not os.path.isabs(access_path):
        access_path = os.path.join(base_dir, access_path)
    if os.path.exists(access_path):
        try:
            import joblib
            _access_model = joblib.load(access_path)
            logger.info(f"[OK] Access pipeline loaded from {access_path}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to load access pipeline: {e}")
    else:
        logger.warning(f"[WARN] Access pipeline not found at {access_path}")

    # Stage 2: Retention Pipeline
    retention_path = config.RETENTION_PIPELINE_PATH
    if not os.path.isabs(retention_path):
        retention_path = os.path.join(base_dir, retention_path)
    if os.path.exists(retention_path):
        try:
            import joblib
            _retention_model = joblib.load(retention_path)
            logger.info(f"[OK] Retention pipeline loaded from {retention_path}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to load retention pipeline: {e}")
    else:
        logger.warning(f"[WARN] Retention pipeline not found at {retention_path}")

    # GAM Distance Model
    gam_path = config.GAM_MODEL_PATH
    if not os.path.isabs(gam_path):
        gam_path = os.path.join(base_dir, gam_path)
    if os.path.exists(gam_path):
        try:
            import joblib
            _gam_model = joblib.load(gam_path)
            logger.info(f"[OK] GAM model loaded from {gam_path}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to load GAM model: {e}")

    _models_loaded = True
    logger.info(f"Model loading complete - Access: {'OK' if _access_model else 'MISSING'}, "
                f"Retention: {'OK' if _retention_model else 'MISSING'}, "
                f"GAM: {'OK' if _gam_model else 'MISSING'}")


def predict_access(distance_km: float, age_group: str, gender: str,
                   wealth_index: str, insurance_status: int,
                   residential_area_group: str, survey_weight: float = 1.0) -> dict:
    """
    Stage 1 prediction: Healthcare access probability.
    Uses XGBoost pipeline if loaded, otherwise falls back to rule-based scoring.
    """
    import config

    # Attempt XGBoost inference
    if _access_model is not None:
        try:
            df = pd.DataFrame([{
                "distance_from_facility": distance_km,
                "insurance_status": "Yes" if insurance_status else "No",
                "education_level": "Secondary",
                "age_group": age_group,
                "wealth_index1": wealth_index,
                "resid": residential_area_group,
                "gender": gender,
                "working_status": "Unknown",
            }])
            prob = round(float(_access_model.predict_proba(df)[0][1]) * 100, 1)
            return {
                "probability": prob,
                "source": "XGBoost",
                "model_auc": config.ACCESS_MODEL_AUC,
                "threshold_km": config.GAM_DISTANCE_THRESHOLD_KM,
                "note": "Access probability conditional on survey participation (§6.5)"
            }
        except Exception as e:
            logger.error(f"XGBoost inference error: {e}")

    # Rule-based fallback (documented in thesis as simplified heuristic)
    base_score = 72.0
    if distance_km > config.GAM_DISTANCE_THRESHOLD_KM:
        base_score -= (distance_km - config.GAM_DISTANCE_THRESHOLD_KM) * 0.5
    if insurance_status == 0:
        base_score -= 8
    if wealth_index in ["Poorest", "Poorer"]:
        base_score -= 6
    if residential_area_group == "Rural":
        base_score -= 4
    base_score = max(15, min(95, base_score))

    return {
        "probability": round(base_score, 1),
        "source": "rule-based fallback",
        "model_auc": None,
        "threshold_km": config.GAM_DISTANCE_THRESHOLD_KM,
        "note": "XGBoost pipeline unavailable — using rule-based approximation"
    }


def predict_retention(distance_km: float, age_group: str, gender: str,
                      wealth_index: str, insurance_status: int,
                      residential_area_group: str) -> dict:
    """
    Stage 2 prediction: Retention/dropout probability.
    Uses the retention XGBoost pipeline with the thesis-recommended threshold (0.95).
    """
    import config

    if _retention_model is not None:
        try:
            df = pd.DataFrame([{
                "distance_from_facility": distance_km,
                "insurance_status": "Yes" if insurance_status else "No",
                "education_level": "Secondary",
                "age_group": age_group,
                "wealth_index1": wealth_index,
                "resid": residential_area_group,
                "gender": gender,
                "working_status": "Unknown",
            }])
            prob = float(_retention_model.predict_proba(df)[0][1])
            is_dropout_risk = prob >= config.RETENTION_CLASSIFICATION_THRESHOLD
            return {
                "retention_probability": round(prob * 100, 1),
                "dropout_risk": is_dropout_risk,
                "source": "XGBoost",
                "model_auc": config.RETENTION_MODEL_AUC,
                "threshold_used": config.RETENTION_CLASSIFICATION_THRESHOLD,
                "note": "Precision trade-off: ~4 false positives per true dropout (§6.5)"
            }
        except Exception as e:
            logger.error(f"Retention model inference error: {e}")

    # Fallback
    risk_score = 50.0
    if distance_km > config.GAM_DISTANCE_THRESHOLD_KM:
        risk_score += (distance_km - config.GAM_DISTANCE_THRESHOLD_KM) * 0.8
    if insurance_status == 0:
        risk_score += 10
    risk_score = max(5, min(95, risk_score))

    return {
        "retention_probability": round(risk_score, 1),
        "dropout_risk": risk_score >= config.HIGH_RISK_DROPOUT_THRESHOLD * 100,
        "source": "rule-based fallback",
        "model_auc": None,
        "threshold_used": config.RETENTION_CLASSIFICATION_THRESHOLD,
        "note": "Retention pipeline unavailable — using rule-based approximation"
    }


def get_model_info() -> dict:
    """Return metadata about loaded models for the /model/info endpoint."""
    import config

    return {
        "access_model": {
            "loaded": _access_model is not None,
            "type": "XGBoost" if _access_model else None,
            "pipeline_path": config.ACCESS_PIPELINE_PATH,
            "auc": config.ACCESS_MODEL_AUC,
            "f1": config.ACCESS_MODEL_F1,
            "brier_score": config.ACCESS_MODEL_BRIER,
            "distance_threshold_km": config.GAM_DISTANCE_THRESHOLD_KM,
        },
        "retention_model": {
            "loaded": _retention_model is not None,
            "type": "XGBoost" if _retention_model else None,
            "pipeline_path": config.RETENTION_PIPELINE_PATH,
            "auc": config.RETENTION_MODEL_AUC,
            "f1": config.RETENTION_MODEL_F1,
            "classification_threshold": config.RETENTION_CLASSIFICATION_THRESHOLD,
        },
        "gam_model": {
            "loaded": _gam_model is not None,
            "pipeline_path": config.GAM_MODEL_PATH,
        },
        "dataset": {
            "original_records": config.ORIGINAL_SURVEY_RECORDS,
            "analytical_records": config.CLEANED_ANALYTICAL_RECORDS,
            "dropped_percent": config.RECORDS_DROPPED_PERCENT,
            "paradox_cases": config.URBAN_PROXIMITY_PARADOX_CASES,
        },
        "shap_attribution": {
            "predisposing_weight_pct": config.PREDISPOSING_SHAP_WEIGHT,
            "enabling_weight_pct": config.ENABLING_SHAP_WEIGHT,
            "distance_weight_pct": config.DISTANCE_SHAP_WEIGHT,
        }
    }
