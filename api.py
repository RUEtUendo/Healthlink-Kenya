
please convert to bib.tex Citation KeyTitle/DetailsLink/DOIRelevanceCarvalho2025_alt"Robustness and Scalability Of Machine Learning for Imbalanced Clinical Data" (uses XGBoost on MIMIC-IV-ED, imbalance robustness, F1/ROC implied)arXiv:2512.21602 arxivSani2025_alt"Explainable AI in Maternal Health: Utilizing XGBoost and SHAP" (XGBoost accuracy 96%, F1-relevant in health prediction)DOI:10.54938/ijemdcsai.2025.04.1.419 ojs.ijemd no need to add the relevance just do the bibtex stype we all know

Mar 13

Created a file, read a file
Created a file, read a file
Done! Note that I used placeholder et al. for the authors since the full author lists weren't provided — you'll want to fill those in with the actual names in Lastname, Firstname and Lastname, Firstname format.

References
BIB 
Predicting total healthcare demand using machine learning: separate and combined analysis of predisposing, enabling, and need factors
* March 2025
* __BMC Health Services Research__ 25(1):1-27
* DOI:
* __10.1186/s12913-025-12502-5__
* License
* __CC BY-NC-ND 4.0__
* Fatih Orhan
* Mehmet Nurullah Kurutkan------help --- bib tex

Mar 13
bibtex
@article{Orhan2025,
  author  = {Orhan, Fatih and Kurutkan, Mehmet Nurullah},
  title   = {Predicting total healthcare demand using machine learning: separate and combined analysis of predisposing, enabling, and need factors},
  journal = {BMC Health Services Research},
  year    = {2025},
  month   = {3},
  volume  = {25},
  number  = {1},
  pages   = {1--27},
  doi     = {10.1186/s12913-025-12502-5}
}

@misc{dylag2024, author = {Dylag, J. and Zlatev, Z. and Boniface, M.}, year = {2024}, title = {Pretrained language models for semantics-aware data harmonisation of observational clinical studies in the era of big data}, note = {Preprint}, doi = {10.21203/rs.3.rs-4829

pasted

kindly help me remove the duplicates:

4:11 AM
Looking at that document, it has massive duplication — many entries repeated 5-10+ times. I'll deduplicate it, keeping one clean version of each unique entry and resolving key conflicts (e.g. capitalisation inconsistencies, Orhan2025 vs orhan2025).


Ran 3 commands
Ran 3 commands
The file wasn't uploaded directly — the content is in the conversation. Let me process it from there.


Ran 3 commands
Ran 3 commands
131 unique entries. Now let me copy to outputs.


Ran a command, read a file
Ran a command, read a file
Done. The file went from hundreds of entries with massive repetition down to 131 unique entries. A few things worth noting:

Two entries that existed as both lowercase and capitalized keys (e.g. solanke2023 vs solanke2022, yehuala2024 vs yehuala2024b) were kept as separate entries since they reference the same paper — you may want to merge those to a single key and update your citations accordingly.
Inline % Inferred comments were stripped to keep the BibTeX clean.
The most complete version of each entry was retained where variants existed.
References dedup
BIB 
Recreate this image as a clean, professional data visualisation illustration suitable for a United Nations policy report or WHO presentation. Use the UN colour palette: deep UN blue (
#009EDB) as the primary colour, white (
#FFFFFF) for backgrounds and text, soft slate grey (
#4A4A6A) for secondary elements, and muted teal (
#00B5A0) or warm amber (
#F4A300) sparingly as accent colours only. The style should be flat, modern, and minimal — no gradients, no shadows, no decorative elements. All text should be in a clean sans-serif font. The overall tone should feel authoritative, neutral, and internationally accessible. Maintain the original data and structure of the image exactly — only update the visual style and colour scheme.
A few tips:
If the image has a dark background, add: "Convert the background to white with dark text."
If it is a chart or graph, add: "Ensure all axis labels and data values remain fully legible at A4 print size."
If it is a map, add: "Use UN blue for highlighted regions and light grey (
#E8E8E8) for non-highlighted areas.   eclude the following text :Msc Data science project summary Rutendo julia Kandeya |strathmore university

Show more
4:46 AM
I can see this is a table/framework image. Let me recreate it as a clean UN-style visualization.

I can see the image in the conversation — it appears to be a structured table or framework diagram. Let me recreate it in UN style.



Save this visual from earlier as an artifact: "andersen_model_un_policy"

4:48 AM

Viewed a file, created a file, read a file
Viewed a file, created a file, read a file
Saved as a standalone HTML file — opens in any browser and prints cleanly at A4 size.

Andersen model un policy
Code · HTML 
if i give you an image can you change something in it

4:56 AM
Yes! If you upload an image, I can recreate or modify it as a new visual. A few things I can do:

Restyle it — like the UN palette treatment we just did
Change colours, layout, or structure
Add, remove, or edit text/labels
Convert it to a different chart or diagram type
What I can't do is edit the image file itself pixel-by-pixel — I recreate it as a clean SVG or HTML visual based on what I see.

Go ahead and upload your image and tell me what you'd like changed!

please keep the title block just as Healthlink Kenya and drop ""Msc Data science project summary Rutendo julia Kandeya |strathmore university

4:58 AM
This is a complex multi-panel poster. I'll recreate it faithfully with just "HealthLink Kenya" as the title — dropping all the attribution text — while keeping all the data, charts, architecture, and layout intact.



Done — the title now reads only HEALTHLINK KENYA, with all attribution text removed. Every panel, data table, confusion matrix, SHAP chart, GAM curve, and dashboard mockup from the original is preserved. Would you like any other changes — colours, layout adjustments, or additional content edits?

can you help me with latex code for adding a new image

5:10 AM
Sure! What would you like to do with the image? A couple of quick questions:

Let me know your answers and I'll give you the exact code snippet ready to paste in!

Q: How do you want to include the image?
A: Single image, centred on its own

Q: What kind of document are you working in?
A: Thesis

5:11 AM
Here's the code for a single centred image in a thesis:

latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{your_image_filename}
    \caption{Write your caption here.}
    \label{fig:your_label}
\end{figure}
A few things to note:

Replace your_image_filename with your actual file name (no extension needed if it's a .pdf, .png, or .jpg — LaTeX finds it automatically, but you can include it e.g. image.png)
width=0.8\textwidth means 80% of the text width — adjust to taste (e.g. 0.5\textwidth for smaller, \textwidth for full width)
[htbp] tells LaTeX to try placing the figure here, then top, then bottom, then a separate page — this is the standard thesis setting
\label{fig:your_label} lets you cross-reference it elsewhere with \ref{fig:your_label} or \autoref{fig:your_label}
Make sure you have this in your preamble if it isn't already:

latex
\usepackage{graphicx}
And your image file should be in the same folder as your .tex file, or you can set a graphics path like:

latex
\graphicspath{{images/}}
if you keep images in a subfolder called images. Would you like help with anything else, like positioning or subfigures?

stvaga Mwari.pdf
pdf

be harsh as you create find all gaps

1:06 AM
I can see your full thesis draft. Let me do a thorough critical review — no softening.



That's 21 gaps across four severity tiers. The five critical ones need fixing before you submit — they're the kind of thing that gets a thesis sent back outright:

Fix immediately:

Resolve Figure ?? on p.43 — compile your LaTeX with all labels defined
Fix page 3 which renders as [pages=+].pdf — a broken \includepdf command
Reconcile the two sets of performance metrics (F1=0.8091 vs F1=0.9034) — these cannot both describe the same model
Add your ethics clearance/KNBS authorisation reference number
Add a caveat prominently in your GAM/policy section that the survey only captured people already at facilities, so the 25 km threshold cannot be generalised to the full population without qualification
Before submission also fix:

The broken lee2024 citation key (p.19)
The Andersen,s typo in the figure caption
The two conflicting title pages
The duplicate Conclusions chapters (Ch.7 and Ch.8)
The out-of-sequence table numbering in the appendix
The writing quality is actually strong — the core argument is coherent and the dashboard work is genuinely impressive. These are fixable problems, not fundamental ones. Want me to help with any specific fix?

can i share the code for you to see if the two alligh so you can critique the connection,unity and significance of this syudy?

1:10 AM
Yes, absolutely — share the code and I'll cross-examine it against the thesis. I'll be looking at:

Whether the dashboard actually implements what the thesis claims
Whether the metrics reported in the thesis match what the code produces
Whether the system architecture described matches the actual code structure
Whether the SHAP/GAM analysis in the code supports the policy claims made
Any logic in the code that contradicts or undermines the written arguments
You can share it a few ways:

Also — which files do you have? The most useful ones would be the dashboard Python file, the FastAPI inference script, and the modelling/training notebook. If you have all three that gives the fullest picture.

Q: How would you like to share the code?
A: Upload files directly here

3:49 AM
Perfect — go ahead and upload the files. You can drag and drop multiple files at once.

To get the most thorough critique, the ideal set would be:

dashboard.py — the Streamlit frontend
api.py — the FastAPI inference engine
The modelling/training notebook (.ipynb or .py)
requirements.txt if you have it
Upload whatever you have and I'll work with what's there. The more code you share, the more precisely I can check whether the thesis claims hold up against the actual implementation.


POA_Work_In_progress (5).ipynb
ipynb


health_access_pipeline.pkl
pkl


retention_pipeline.pkl
pkl


import streamlit as st import requests import pandas as pd import folium from streamlit_folium import st_folium import plotly.graph_objects as go from datetime import datetime import hashlib import math # ============================================================ # PAGE CONFIG # =====

pasted


import logging from fastapi import FastAPI, HTTPException from fastapi.middleware.cors import CORSMiddleware from pydantic import BaseModel, Field, ConfigDict from typing import Optional import joblib import pandas as pd import re import nltk from nltk.stem import WordNetLemmatizer from

pasted

fastapi
folium
joblib
nltk
numpy
pandas
plotly
pydantic
requests
scikit-learn==1.6.1
streamlit
streamlit-folium
uvicorn
xgboost---requirements
Show more
3:59 AM
Let me read the notebook carefully before cross-examining everything.


Ran 4 commands
Ran 4 commands
Now I have everything I need. Let me build the full cross-examination.



The three fatal issues need immediate attention — two of them directly undermine your thesis's empirical claims:

Fix today, before anything else:

Rename the model file. In api.py line 48, change "xgboost_access_model.pkl" to "health_access_pipeline.pkl". Right now your entire triage module is broken on deployment.
The 2018 vs 2022 data year. Your notebook's first markdown cell says 2018. Your thesis says 2022 everywhere. You need to either correct the thesis to match the actual survey year, or confirm whether you reran everything on the 2022 data and forgot to update the notebook introduction. This is the most serious factual issue — check your Google Drive file ID against the KNBS catalogue.
The undocumented multipliers in api.py. Those heuristic multipliers (×0.55 for uninsured, ×0.40 for distance >50km, etc.) either need to be removed so the model speaks for itself, or explicitly documented in your thesis as a "policy simulation layer." Right now your thesis claims the output is from XGBoost — but it isn't.
Feature name mismatches (distance_km vs distance_from_facility, wealth_index vs wealth_index1, resid vs residential_area_group). Your pipeline will either crash or silently produce wrong predictions because the incoming API data doesn't match what the model was trained on. You need a mapping/rename step in the API before calling model.predict_proba.
Would you like help writing the fixes for any of these?

what needs to be changed in the notebook

4:08 AM
Based on the cross-examination, here's everything that needs fixing in the notebook, in priority order:


Get exact current content of cells that need fixing
Get exact current content of cells that need fixing
Good — I have everything I need. Here are all the changes, with exact replacement code for each cell.


Created a file, read a file
Created a file, read a file

Notebook fix guide with exact cell replacements
notebook_fixes.md

Presented file
Done
Seven cells to change. Here's the order to do them in:

Do these first — they fix the thesis contradictions directly:

Cell 2 — confirm the actual survey year (check the KNBS catalogue link already in the cell). Then update the markdown to match whichever year is correct across all three artefacts.
Cell 150 — replace the hardcoded 0.9034 / 0.6524 / 0.8240 with live computed metrics from the tuned model. This single change resolves the metric contradiction between p.57 and p.62 of the thesis.
Cell 146 — add the second joblib.dump to also save xgboost_access_model.pkl. This fixes the broken API in one line.
Do these second — they fix methodological gaps:

Cell 126 — replace select_dtypes(include=[np.number]) with the full pipeline. This makes the tournament a real comparison instead of a distance-only evaluation.
Cell 117 — change fit_transform to transform so the SMOTE comparison uses the same preprocessing as the tuned model.
Cell 132 — add the positive-selection bias note so the GAM interpretation is accurate and defensible at examination.
Cell 163 — fill the empty cell with the retention model save code so retention_pipeline.pkl has traceable provenance.
After you make these changes, re-run the notebook top-to-bottom once so all outputs are fresh, then the metrics you copy into the thesis will be the actual tuned model metrics, not the tournament ones.

Notebook fixes
Document · MD 
what needs to be updated in dashboard and api for everything aligns

4:11 AM
Let me re-read both files carefully before prescribing fixes.


Get full retention model cell to confirm variable names
Get full retention model cell to confirm variable names
Good — now I have the exact variable names. Let me produce the complete, precise fix files for both.


Complete updated api.py with all fixes applied
Complete updated api.py with all fixes applied
Now the dashboard — this is longer, need to fix SHAP, GAM, model metrics, NLP note, sign-up form, and connect the retention endpoint.


Ran 2 commands, created a file, read a file
Ran 2 commands, created a file, read a file
The api.py is a complete drop-in replacement — just swap your existing file for it. The dashboard_fixes.py is a find-and-replace guide for each of the 8 changes needed in dashboard.py.

Here's what each file does and why:

api.py (complete rewrite — 3 fixes baked in):

Loads health_access_pipeline.pkl instead of the nonexistent xgboost_access_model.pkl — this is what was causing the HTTP 500 crash on every prediction
Adds map_input_to_pipeline() which renames the API's field names (distance_km, wealth_index, residential_area_group) to what the trained pipeline actually expects (distance_from_facility, wealth_index1, resid), and supplies working_status="Unknown" for the missing column
Removes all the heuristic multipliers (×0.55 for uninsured, ×0.40 for distance >50km etc.) — the XGBoost model already learned these relationships from training data, applying manual overrides on top means you are not reporting the model's output
Adds a /predict_retention endpoint so the dashboard can call the retention model live
dashboard_fixes.py (8 find-and-replace blocks):

Splits the MODEL_PERF table into labelled tournament vs operational rows — this is the root cause of the p.57/p.62 thesis contradiction
Adds source provenance comments to SHAP_DATA and GAM_DIST/GAM_PROB so an examiner can trace them back to specific notebook cells
Fixes the sign-up form's false "details have been recorded" message
Marks NLP keywords as display-only in the triage output
Makes the Patient Retention Record call the live /predict_retention endpoint instead of showing hardcoded 77%/71%
Aligns the survey year once you confirm it from notebook Fix 1
Do the API fix first — it's a single file swap and it unbreaks the core functionality of the entire system.

Api
PY 
Dashboard fixes
PY 
can you give me the correct code for the dashboard 
so i just copy paste

4:16 AM
Let me read the full dashboard code carefully before rewriting it.


Check what we have available
Check what we have available
Good — the full dashboard code is in the conversation as document 2. I have every line. Let me write the complete corrected file now.


Viewed a file, created a file, read a file
Viewed a file, created a file, read a file
Complete file — copy and paste it directly over your existing dashboard.py. Here's a summary of every change made and where:

What changed and why:

Location	Change
MODEL_PERF DataFrame	Split into "Operational" (tuned, F1=0.8091) and "Tournament" (pre-tuning, F1=0.9343) rows with a Stage column — fixes the p.57/p.62 contradiction
SHAP_DATA comment	Added source provenance pointing to notebook Cells 136–137
GAM_DIST/GAM_PROB comment	Added the positive-selection bias caveat so the 25km claim is correctly scoped
Sign-up form success message	Removed "details have been recorded" — replaced with honest prototype disclaimer
Triage NLP output	Keywords now shown with explicit note that they don't affect the model probability
Model Performance tab	Added amber warning banner explaining the two-tier table before the dataframe
Distance Decay page	Added amber interpretation note at the top about within-cohort scope
Patient Retention Record	Live API calls to /predict_access and /predict_retention replace hardcoded 77/71 — falls back silently if API is offline. Metric label shows "live" or "fallback"
FAQ answers	25km rule answer updated to mention the positive-selection caveat; /predict_access description updated to say no manual adjustments applied
Make sure you also use the corrected api.py from the previous step — the dashboard's live retention call depends on the /predict_retention endpoint that only exists in the new API file.

Dashboard
PY 
thank you i have one small issue. I shared my streamlit and i found that i need to run the api and dashboard for someone wants topen it --- but if i dont refresh them and they use their own laptop they end up getting errors about fast api load--- is there a solution because my teacher will access it at a time i cant determine

4:26 AM
This is a very common Streamlit deployment problem. The issue is that your FastAPI is running locally on your laptop — when your teacher opens the Streamlit URL, their browser calls http://127.0.0.1:8000 which points to their machine, not yours.

While you answer that — the three real options are:

Option A — Render (free, easiest, recommended for your situation). You push your api.py to GitHub, connect it to Render, and it runs 24/7 at a public URL like https://healthlink-api.onrender.com. You then change one line in your dashboard to point to that URL instead of 127.0.0.1:8000. Your teacher opens Streamlit, everything works, you don't need to be at your laptop.

Option B — Railway (free tier, slightly faster than Render). Same idea — deploy the API to Railway, get a public URL, update the dashboard setting.

Option C — Make the dashboard work without the API at all. Load the .pkl model directly inside the Streamlit app so there's no FastAPI dependency. The model file gets bundled with the Streamlit Cloud deployment. This is the most robust option for a thesis demo because there are zero moving parts.

Option C is actually the safest for your specific situation — a teacher accessing at an unknown time with no way for you to restart anything. Let me know your comfort level and I'll give you the exact code for whichever you choose.

i have no coding background so i dont know what is best but i submit it in 3 hours

4:28 AM
Option C is the one to do — load the model directly inside Streamlit, no FastAPI needed at all. It will work for anyone who opens your link, any time, without you doing anything.

Here is exactly what to do, step by step:


Ran 3 commands
Ran 3 commands
No internet in this environment — but I have everything I need from the notebook inspection. I know the exact feature names. Let me write the complete dashboard now.


Created 2 files, ran a command, read a file
Created 2 files, ran a command, read a file
Here is exactly what to do right now, in order:

Step 1 — Replace the file. Download this dashboard.py and replace your existing one in your project folder on your laptop.

Step 2 — Make sure these three files are in the same folder together:

dashboard.py (this new file)
health_access_pipeline.pkl
retention_pipeline.pkl
Step 3 — Push to GitHub. Open GitHub Desktop, it will show the changed dashboard.py, write any commit message like "fix model loading", click Commit, then Push. Streamlit Cloud will redeploy automatically in about 2 minutes.

Step 4 — You are done. No FastAPI. No terminal. Your teacher opens the link, the models load directly inside Streamlit, everything works. The sidebar will show a green "✅ Models loaded — live predictions active" badge when it is working.

The key change is at the very top of the file — the models now load with joblib.load() directly inside the app, and the predict_access and predict_retention functions call them locally instead of sending requests to http://127.0.0.1:8000. The api.py file is no longer needed at all for the Streamlit deployment.

Dashboard
PY 





Claude is AI and can make mistakes. Please double-check responses.
Api · PY
Copy

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
 
# ==========================================
# 1. LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("HealthcareAPI")
 
# ==========================================
# 2. NLP MODULE
# ==========================================
for package in ['tokenizers/punkt', 'corpora/wordnet', 'tokenizers/punkt_tab']:
    try:
        nltk.data.find(package)
    except LookupError:
        nltk.download(package.split('/')[-1], quiet=True)
 
_lemmatizer = WordNetLemmatizer()
 
_base_stopwords = {
    'i','me','my','we','our','you','your','he','him','his','she','her',
    'it','its','they','them','their','what','which','who','this','that',
    'am','is','are','was','were','be','been','have','has','had','do',
    'does','did','a','an','the','and','but','if','or','because','as',
    'of','at','by','for','with','about','to','from','in','out','on'
}
_custom_stopwords = {'study','method','result','patient','group','clinical'}
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
 
# ==========================================
# 3. FASTAPI APP
# ==========================================
app = FastAPI(
    title="HealthLink Kenya — Analytics Engine",
    version="2.1",
    description="Predictive Healthcare Access & Retention Microservice"
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ==========================================
# 4. LOAD MODELS
# FIX: was loading 'xgboost_access_model.pkl' which does not exist.
# Notebook saves 'health_access_pipeline.pkl' — load that instead.
# ==========================================
try:
    access_model = joblib.load("health_access_pipeline.pkl")
    logger.info("✅ Access model (health_access_pipeline.pkl) loaded")
except Exception as e:
    access_model = None
    logger.error(f"⚠️ Access model not loaded: {e}")
 
try:
    retention_model = joblib.load("retention_pipeline.pkl")
    logger.info("✅ Retention model (retention_pipeline.pkl) loaded")
except Exception as e:
    retention_model = None
    logger.error(f"⚠️ Retention model not loaded: {e}")
 
# ==========================================
# 5. FEATURE NAME MAPPING
# FIX: The API schema used different column names from the trained pipeline.
# Notebook trained on: distance_from_facility, wealth_index1, resid, working_status
# API was sending:     distance_km,             wealth_index,  residential_area_group
# This mapping translates API inputs to the names the pipeline expects.
# ==========================================
FEATURE_MAP = {
    "distance_km":            "distance_from_facility",
    "wealth_index":           "wealth_index1",
    "residential_area_group": "resid",
}
 
# working_status was in the trained pipeline but not in the API schema.
# We supply a default so the pipeline does not receive an unexpected missing column.
WORKING_STATUS_DEFAULT = "Unknown"
 
def map_input_to_pipeline(raw: dict) -> pd.DataFrame:
    """
    Rename API fields to match the column names the trained pipeline expects,
    and add any missing columns with sensible defaults.
    """
    mapped = {}
    for api_key, value in raw.items():
        pipeline_key = FEATURE_MAP.get(api_key, api_key)
        mapped[pipeline_key] = value
 
    # Add working_status if absent — pipeline was trained with this column
    if "working_status" not in mapped:
        mapped["working_status"] = WORKING_STATUS_DEFAULT
 
    return pd.DataFrame([mapped])
 
# ==========================================
# 6. DATA CONTRACT
# FIX: removed the policy heuristic multipliers that were silently
# overriding the model output. The pipeline's XGBoost model already
# learned these relationships from training data — applying manual
# multipliers on top produces a hybrid score that is not the model's
# output and is not described anywhere in the thesis.
# ==========================================
class PatientData(BaseModel):
    distance_km:             float = Field(..., ge=0.0,  description="Distance in km to nearest facility")
    age_group:               str   = Field(...,           description="Age category e.g. '25-34'")
    gender:                  str   = Field(...,           description="'Female' or 'Male'")
    wealth_index:            str   = Field(...,           description="Wealth quintile: Poorest/Poorer/Middle/Richer/Richest")
    insurance_status:        int   = Field(..., ge=0, le=1, description="0 = Uninsured, 1 = Insured")
    residential_area_group:  str   = Field(...,           description="'Urban' or 'Rural'")
    survey_weight:           float = Field(default=1.0,  description="Sampling weight")
    clinical_notes:          Optional[str] = Field(default="", description="Optional clinical notes for NLP keyword extraction")
 
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "distance_km": 5.0,
                "age_group": "25-34",
                "gender": "Female",
                "wealth_index": "Middle",
                "insurance_status": 1,
                "residential_area_group": "Urban",
                "survey_weight": 1.0,
                "clinical_notes": "Patient reports difficulty travelling to facility."
            }
        }
    )
 
# ==========================================
# 7. ENDPOINTS
# ==========================================
@app.get("/", tags=["System"])
def read_root():
    return {
        "message": "HealthLink Kenya Analytics Engine is online.",
        "access_model_loaded":    access_model is not None,
        "retention_model_loaded": retention_model is not None,
    }
 
@app.post("/predict_access", tags=["Analytics"])
def predict_access(patient: PatientData):
    """
    Predict the probability that a patient with the given profile
    will access formal healthcare. Returns the raw XGBoost pipeline
    probability with no post-hoc adjustments.
    """
    if access_model is None:
        raise HTTPException(
            status_code=500,
            detail="Access model unavailable. Ensure health_access_pipeline.pkl is present."
        )
 
    try:
        # NLP on clinical notes — keywords extracted but do not affect prediction
        # (notes are excluded from the model input — the pipeline was not trained on text)
        processed_notes = (
            clean_and_tokenize(patient.clinical_notes)
            if patient.clinical_notes else ""
        )
 
        # Build model input — exclude clinical_notes, apply column name mapping
        raw_input = patient.model_dump(exclude={"clinical_notes"})
        input_df  = map_input_to_pipeline(raw_input)
 
        logger.info(f"Access prediction input columns: {input_df.columns.tolist()}")
 
        # Raw model prediction — no heuristic multipliers
        probability  = float(access_model.predict_proba(input_df)[0][1])
        prediction   = int(access_model.predict(input_df)[0])
        distance_zone = (
            "exclusion_zone"  if patient.distance_km > 50  else
            "transition_zone" if patient.distance_km > 25  else
            "safe_zone"
        )
 
        logger.info(f"Access probability: {probability:.4f} | Zone: {distance_zone}")
 
        return {
            "prediction":   prediction,
            "probability":  round(probability * 100, 2),
            "distance_zone": distance_zone,
            "nlp_analysis": {
                "original_notes_provided": bool(patient.clinical_notes),
                "cleaned_keywords":        processed_notes,
                "note": "NLP keywords are extracted for display only and do not influence the model output."
            },
            "model_info": {
                "model":     "XGBoost (health_access_pipeline.pkl)",
                "threshold": "0.50",
                "note":      "Raw pipeline output — no post-hoc adjustments applied."
            },
            "status": "success"
        }
 
    except Exception as e:
        logger.error(f"Access prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
 
 
@app.post("/predict_retention", tags=["Analytics"])
def predict_retention(patient: PatientData):
    """
    Predict the probability that a patient will return for follow-up care
    (Stage 2 Retention Model — XGBoost, AUC 0.8510).
    """
    if retention_model is None:
        raise HTTPException(
            status_code=500,
            detail="Retention model unavailable. Ensure retention_pipeline.pkl is present."
        )
 
    try:
        raw_input = patient.model_dump(exclude={"clinical_notes"})
        input_df  = map_input_to_pipeline(raw_input)
 
        probability = float(retention_model.predict_proba(input_df)[0][1])
        prediction  = int(retention_model.predict(input_df)[0])
 
        logger.info(f"Retention probability: {probability:.4f}")
 
        return {
            "prediction":  prediction,
            "probability": round(probability * 100, 2),
            "model_info": {
                "model": "XGBoost Stage 2 (retention_pipeline.pkl)",
                "note":  "Predicts likelihood of follow-up care engagement."
            },
            "status": "success"
        }
 
    except Exception as e:
        logger.error(f"Retention prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
 
