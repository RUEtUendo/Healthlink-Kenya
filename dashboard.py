"""
HealthLink Kenya — Predictive Framework for Healthcare Access
Rutendo Julia Kandeya · ID 168332 · Strathmore University · 2026
Supervisor: Dr. Esther Khakata

v4.0 — multipage navigation via st.navigation(), warm-slate theme,
       CartoDB Voyager map, white-bordered circle markers.
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from datetime import datetime
import hashlib
import math
import warnings
warnings.filterwarnings("ignore")

# ── PAGE CONFIG (must be first Streamlit call) ─────────────────────
st.set_page_config(
    page_title="HealthLink Kenya",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── MODEL LOADING ──────────────────────────────────────────────────
@st.cache_resource
def load_models():
    try:
        import joblib
        return (
            joblib.load("health_access_pipeline.pkl"),
            joblib.load("retention_pipeline.pkl"),
            True,
        )
    except Exception as e:
        return None, None, str(e)

access_model, retention_model, models_ok = load_models()
OPTIMAL_THRESHOLD = 0.35

def predict_access(dist, age, gender, wealth, insured, residence):
    if access_model is None:
        return 72.0, "fallback"
    try:
        df = pd.DataFrame([{
            "distance_from_facility": dist,
            "insurance_status": "Yes" if insured else "No",
            "education_level": "Secondary",
            "age_group": age,
            "wealth_index1": wealth,
            "resid": residence,
            "gender": gender,
            "working_status": "Unknown",
        }])
        return round(float(access_model.predict_proba(df)[0][1]) * 100, 1), "live"
    except Exception:
        return 72.0, "fallback"

def predict_retention(dist, age, gender, wealth, insured, residence):
    if retention_model is None:
        return 65.0, "fallback"
    try:
        df = pd.DataFrame([{
            "distance_from_facility": dist,
            "insurance_status": "Yes" if insured else "No",
            "education_level": "Secondary",
            "age_group": age,
            "wealth_index1": wealth,
            "resid": residence,
            "gender": gender,
            "working_status": "Unknown",
        }])
        return round(float(retention_model.predict_proba(df)[0][1]) * 100, 1), "live"
    except Exception:
        return 65.0, "fallback"

# ── SESSION STATE INIT ─────────────────────────────────────────────
for key, default in [
    ("authenticated", False),
    ("user", {}),
    ("theme", "light"),
    ("accent", "#0B3D6E"),
    ("font_size", "Medium"),
    ("map_style", "CartoDB Voyager"),
    ("show_paradox", True),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── THEME TOKENS ───────────────────────────────────────────────────
acc     = st.session_state.accent
is_dark = st.session_state.theme == "dark"

bg      = "#0D1117" if is_dark else "#F4F6F9"   # warm-slate light bg
sbg     = "#161B22" if is_dark else "#FFFFFF"
card    = "#1C2333" if is_dark else "#FFFFFF"
border  = "#30363D" if is_dark else "#DDE4EF"
text    = "#E6EDF3" if is_dark else "#1A2B40"
muted   = "#8B949E" if is_dark else "#6B84A0"
card_b  = "#1A2D4A" if is_dark else "#EEF5FF"
card_g  = "#1A3A2A" if is_dark else "#EDFBF5"
card_a  = "#3A2D10" if is_dark else "#FFFBEE"
card_r  = "#3A1A1A" if is_dark else "#FFF5F5"
bdr_b   = "#2D5490" if is_dark else "#C2D8F5"
bdr_g   = "#2D7A5A" if is_dark else "#A8E6D0"
bdr_a   = "#7A5A20" if is_dark else "#FDDDA0"
bdr_r   = "#7A2D2D" if is_dark else "#FBCACA"
TICK    = "#E6EDF3" if is_dark else "#1A1A2E"
fs      = {"Small": "11px", "Medium": "13px", "Large": "15px"}.get(
              st.session_state.font_size, "13px")

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;font-size:{fs};}}
.stApp{{background-color:{bg};color:{text};}}
section[data-testid="stSidebar"]{{background-color:{sbg};border-right:1px solid {border};box-shadow:2px 0 8px rgba(0,0,0,0.06);}}
h1{{color:{acc}!important;font-weight:800!important;}}
h2{{color:{acc}!important;font-weight:700!important;}}
h3,h4{{color:{text}!important;font-weight:600!important;}}
p,span,div{{color:{text};}}
[data-testid="metric-container"]{{background:{card}!important;border:1.5px solid {border}!important;border-radius:14px!important;padding:20px 22px!important;box-shadow:0 2px 8px rgba(0,0,0,0.07)!important;}}
[data-testid="metric-container"] label{{color:{muted}!important;font-size:11px!important;text-transform:uppercase;letter-spacing:.06em;font-weight:700!important;}}
[data-testid="metric-container"] [data-testid="stMetricValue"]{{color:{acc}!important;font-size:28px!important;font-weight:900!important;}}
[data-testid="metric-container"] [data-testid="stMetricDelta"]{{color:#16A34A!important;font-weight:600!important;}}
.stButton>button{{background:{acc}!important;color:#FFFFFF!important;border:none!important;border-radius:8px!important;font-weight:700!important;padding:10px 28px!important;}}
.stButton>button:hover{{filter:brightness(1.12)!important;}}
.stSelectbox label,.stSlider label,.stRadio label,.stTextArea label,.stTextInput label,.stNumberInput label,.stSelectSlider label{{color:{muted}!important;font-size:11px!important;font-weight:700!important;text-transform:uppercase;letter-spacing:.05em;}}
.stTextInput input,.stSelectbox>div>div,.stTextArea textarea{{background:{card}!important;border:1px solid {border}!important;border-radius:8px!important;color:{text}!important;}}
.stRadio>div{{gap:3px;}}
.stRadio label{{padding:10px 14px!important;border-radius:10px!important;font-size:13px!important;font-weight:500;color:{text}!important;}}
.med-card{{background:{card};border:1.5px solid {border};border-radius:14px;padding:18px 22px;box-shadow:0 2px 8px rgba(0,0,0,0.05);margin-bottom:12px;}}
.med-card-blue{{background:{card_b};border:1.5px solid {bdr_b};border-radius:14px;padding:16px 20px;margin-bottom:12px;}}
.med-card-green{{background:{card_g};border:1.5px solid {bdr_g};border-radius:14px;padding:16px 20px;margin-bottom:12px;}}
.med-card-amber{{background:{card_a};border:1.5px solid {bdr_a};border-radius:14px;padding:16px 20px;margin-bottom:12px;}}
.med-card-red{{background:{card_r};border:1.5px solid {bdr_r};border-radius:14px;padding:16px 20px;margin-bottom:12px;}}
.badge-green{{background:#DCFCE7;color:#15803D;border-radius:99px;padding:3px 12px;font-size:11px;font-weight:700;}}
.badge-amber{{background:#FEF9C3;color:#A16207;border-radius:99px;padding:3px 12px;font-size:11px;font-weight:700;}}
.badge-red{{background:#FEE2E2;color:#DC2626;border-radius:99px;padding:3px 12px;font-size:11px;font-weight:700;}}
.badge-blue{{background:#DBEAFE;color:#1D4ED8;border-radius:99px;padding:3px 12px;font-size:11px;font-weight:700;}}
.badge-grey{{background:#F1F5F9;color:#64748B;border-radius:99px;padding:3px 12px;font-size:11px;font-weight:700;}}
.pt-row{{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid {border};font-size:13px;}}
.pt-label{{color:{muted};font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.04em;}}
.pt-value{{color:{text};font-weight:600;}}
.login-card{{background:{card};border:1.5px solid {border};border-radius:18px;padding:40px 44px;box-shadow:0 6px 28px rgba(0,0,0,0.10);max-width:440px;margin:0 auto;}}
.stTabs [data-baseweb="tab-list"]{{background:{"#21262D" if is_dark else "#F0F4FA"};border-radius:10px;padding:4px;}}
.stTabs [data-baseweb="tab"]{{color:{muted};border-radius:7px;font-weight:500;}}
.stTabs [aria-selected="true"]{{color:{acc}!important;background:{card}!important;box-shadow:0 1px 4px rgba(0,0,0,0.10);font-weight:700;}}
hr{{border-color:{border};margin:16px 0;}}
.stProgress>div>div{{background-color:{acc}!important;}}
[data-testid="stDataFrame"]{{border-radius:10px;overflow:hidden;}}
</style>""", unsafe_allow_html=True)

# ── AUTH ───────────────────────────────────────────────────────────
DEMO_USERS = {
    "admin@healthlink.ke":   {"pw": hashlib.sha256(b"Admin2024!").hexdigest(),  "role": "Administrator",  "name": "Dr. Admin"},
    "doctor@healthlink.ke":  {"pw": hashlib.sha256(b"Doctor2024!").hexdigest(), "role": "Clinician",      "name": "Dr. Wanjiku"},
    "nurse@healthlink.ke":   {"pw": hashlib.sha256(b"Nurse2024!").hexdigest(),  "role": "Nurse",          "name": "Sr. Auma"},
    "planner@healthlink.ke": {"pw": hashlib.sha256(b"Plan2024!").hexdigest(),   "role": "Health Planner", "name": "Mr. Omondi"},
}

if not st.session_state.authenticated:
    st.markdown(f"""
    <div style='text-align:center;padding:48px 0 24px;'>
      <div style='font-size:56px;'>⚕️</div>
      <div style='font-size:30px;font-weight:800;color:{acc};margin-top:8px;'>HealthLink Kenya</div>
      <div style='font-size:14px;color:{muted};margin-top:6px;font-weight:500;'>
        A Predictive Framework for Healthcare Access and Referral Planning
      </div>
    </div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        tab_in, tab_up = st.tabs(["Sign In", "Create Account"])
        with tab_in:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;margin-bottom:20px;color:{acc};'>Sign In</h3>", unsafe_allow_html=True)
            email    = st.text_input("Email Address", placeholder="you@healthlink.ke", key="si_email")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="si_pw")
            if st.button("Sign In", use_container_width=True, key="si_btn"):
                hashed = hashlib.sha256(password.encode()).hexdigest()
                if email in DEMO_USERS and DEMO_USERS[email]["pw"] == hashed:
                    st.session_state.authenticated = True
                    st.session_state.user = {"email": email, **DEMO_USERS[email]}
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: doctor@healthlink.ke / Doctor2024!")
            st.markdown(f"""
            <div style='margin-top:16px;padding:12px 14px;background:{"#21262D" if is_dark else "#F7F9FC"};
                        border-radius:8px;font-size:11px;color:{muted};line-height:2.0;'>
              <b style='color:{acc};'>Demo accounts:</b><br>
              doctor@healthlink.ke · <i>Doctor2024!</i><br>
              nurse@healthlink.ke · <i>Nurse2024!</i><br>
              planner@healthlink.ke · <i>Plan2024!</i>
            </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with tab_up:
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;margin-bottom:20px;color:{acc};'>Create Profile</h3>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                fn = st.text_input("First Name", placeholder="Jane", key="su_fn")
            with c2:
                ln = st.text_input("Last Name",  placeholder="Njoroge", key="su_ln")
            em  = st.text_input("Institutional Email", placeholder="you@hospital.ke", key="su_em")
            rol = st.selectbox("Role", ["Clinician","Nurse","Health Planner","Administrator","Research Officer","Community Health Worker"], key="su_rol")
            p1, p2 = st.columns(2)
            with p1: pw1 = st.text_input("Password", type="password", key="su_pw1")
            with p2: pw2 = st.text_input("Confirm",  type="password", key="su_pw2")
            if st.button("Create Profile", use_container_width=True, key="su_btn"):
                if not all([fn, ln, em, pw1]):
                    st.warning("Fill in all required fields.")
                elif pw1 != pw2:
                    st.error("Passwords do not match.")
                elif len(pw1) < 8:
                    st.error("Password must be at least 8 characters.")
                elif "@" not in em:
                    st.error("Enter a valid email address.")
                else:
                    st.success(f"Registration submitted for {fn} {ln} · {rol}.")
                    st.info("This is a research prototype. Use a demo account on the Sign In tab to access the dashboard.")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ── DATA ───────────────────────────────────────────────────────────
FACILITIES = pd.DataFrame([
    {"Name":"Strathmore University Health Centre","Type":"Clinic","Sector":"Private","Phone":"+254 020 606 1000","Specialties":"General OPD, First Aid, Mental Health, Referral","Dist_km":0.0,"Insurance_pct":85,"Wealth":"Richer","Access_pct":88,"Retention_pct":80,"Lat":-1.3031,"Lon":36.8155,"Paradox":False,"Beds":5,"Band":"Under 5km"},
    {"Name":"Kenyatta National Hospital","Type":"National Referral Hospital","Sector":"Public","Phone":"+254 020 272 6300","Specialties":"Oncology, Cardiology, Neurology, Trauma, Burns, Transplant","Dist_km":1.0,"Insurance_pct":91,"Wealth":"Highest","Access_pct":94,"Retention_pct":89,"Lat":-1.3006,"Lon":36.8066,"Paradox":False,"Beds":1800,"Band":"Under 5km"},
    {"Name":"Nairobi Hospital","Type":"Private Hospital","Sector":"Private","Phone":"+254 020 284 5000","Specialties":"Cardiology, Neurosurgery, Oncology, Transplant, Trauma","Dist_km":1.2,"Insurance_pct":97,"Wealth":"Highest","Access_pct":93,"Retention_pct":90,"Lat":-1.2923,"Lon":36.8161,"Paradox":False,"Beds":300,"Band":"Under 5km"},
    {"Name":"Nairobi West Hospital","Type":"Religious / Mission Hospital","Sector":"Faith-Based","Phone":"+254 020 603 0000","Specialties":"Oncology, Orthopaedics, Cardiology, Dialysis, ICU","Dist_km":1.4,"Insurance_pct":74,"Wealth":"Richer","Access_pct":82,"Retention_pct":76,"Lat":-1.3146,"Lon":36.8100,"Paradox":False,"Beds":200,"Band":"Under 5km"},
    {"Name":"Nairobi Women's Hospital — Hurlingham","Type":"Private Hospital","Sector":"Private","Phone":"+254 020 272 0160","Specialties":"Obstetrics, Gynaecology, Emergency, Paediatrics, Oncology","Dist_km":1.5,"Insurance_pct":90,"Wealth":"Highest","Access_pct":92,"Retention_pct":87,"Lat":-1.2937,"Lon":36.8063,"Paradox":False,"Beds":140,"Band":"Under 5km"},
    {"Name":"Coptic Hospital Nairobi","Type":"Religious / Mission Hospital","Sector":"Faith-Based","Phone":"+254 020 269 1141","Specialties":"General Surgery, Maternity, Orthopaedics, Paediatrics","Dist_km":2.2,"Insurance_pct":78,"Wealth":"Richer","Access_pct":84,"Retention_pct":78,"Lat":-1.2963,"Lon":36.7970,"Paradox":False,"Beds":130,"Band":"Under 5km"},
    {"Name":"Mater Misericordiae Hospital","Type":"Religious / Mission Hospital","Sector":"Faith-Based","Phone":"+254 020 690 6000","Specialties":"Cardiology, Oncology, ICU, Maternity, Renal","Dist_km":2.8,"Insurance_pct":88,"Wealth":"Richer","Access_pct":87,"Retention_pct":82,"Lat":-1.3001,"Lon":36.8401,"Paradox":False,"Beds":290,"Band":"Under 5km"},
    {"Name":"MP Shah Hospital","Type":"Private Hospital","Sector":"Private","Phone":"+254 020 374 2763","Specialties":"Cardiology, Oncology, Orthopaedics, ICU, Dialysis","Dist_km":3.4,"Insurance_pct":95,"Wealth":"Highest","Access_pct":91,"Retention_pct":88,"Lat":-1.2726,"Lon":36.8156,"Paradox":False,"Beds":210,"Band":"Under 5km"},
    {"Name":"Aga Khan University Hospital","Type":"Private Hospital","Sector":"Private","Phone":"+254 020 366 2000","Specialties":"Neurosurgery, Oncology, Cardiology, Transplant, MRI/CT","Dist_km":3.8,"Insurance_pct":96,"Wealth":"Highest","Access_pct":91,"Retention_pct":88,"Lat":-1.2702,"Lon":36.8074,"Paradox":False,"Beds":250,"Band":"Under 5km"},
    {"Name":"Pumwani Maternity Hospital","Type":"County Hospital","Sector":"Public","Phone":"+254 020 222 3991","Specialties":"Maternity, Neonatal ICU, Gynaecology","Dist_km":4.0,"Insurance_pct":62,"Wealth":"Middle","Access_pct":81,"Retention_pct":74,"Lat":-1.2841,"Lon":36.8458,"Paradox":False,"Beds":320,"Band":"Under 5km"},
    {"Name":"Mediheal Hospital — Nairobi","Type":"Private Hospital","Sector":"Private","Phone":"+254 020 208 1000","Specialties":"Cardiology, Orthopaedics, General Surgery, ICU","Dist_km":4.0,"Insurance_pct":82,"Wealth":"Richer","Access_pct":85,"Retention_pct":80,"Lat":-1.3189,"Lon":36.8480,"Paradox":False,"Beds":180,"Band":"Under 5km"},
    {"Name":"Mbagathi District Hospital","Type":"County Hospital","Sector":"Public","Phone":"+254 020 201 9000","Specialties":"General Surgery, Infectious Disease, Psychiatry, Paediatrics","Dist_km":5.7,"Insurance_pct":55,"Wealth":"Middle","Access_pct":77,"Retention_pct":71,"Lat":-1.3217,"Lon":36.7680,"Paradox":False,"Beds":260,"Band":"5–15km"},
    {"Name":"Mathare North Health Centre","Type":"Health Centre","Sector":"Public","Phone":"+254 020 232 0000","Specialties":"General OPD, Maternal Health, Immunisation, HIV/ART","Dist_km":6.7,"Insurance_pct":31,"Wealth":"Lowest","Access_pct":48,"Retention_pct":44,"Lat":-1.2611,"Lon":36.8590,"Paradox":True,"Beds":40,"Band":"5–15km"},
    {"Name":"Ruaraka Health Centre","Type":"Health Centre","Sector":"Public","Phone":"+254 020 856 0000","Specialties":"General OPD, Family Planning, HIV/ART, TB/DOTS","Dist_km":9.0,"Insurance_pct":44,"Wealth":"Middle","Access_pct":65,"Retention_pct":59,"Lat":-1.2488,"Lon":36.8756,"Paradox":False,"Beds":20,"Band":"5–15km"},
    {"Name":"Kayole Sub-County Hospital","Type":"Sub-County Hospital","Sector":"Public","Phone":"+254 020 232 1000","Specialties":"Emergency, Maternity, General OPD, Eye Clinic","Dist_km":10.0,"Insurance_pct":28,"Wealth":"Poorer","Access_pct":43,"Retention_pct":38,"Lat":-1.2718,"Lon":36.9001,"Paradox":True,"Beds":120,"Band":"5–15km"},
    {"Name":"Dandora Dispensary","Type":"Dispensary","Sector":"Public","Phone":"+254 020 232 2000","Specialties":"Basic Primary Care, Immunisation, Wound Care","Dist_km":11.4,"Insurance_pct":19,"Wealth":"Poorest","Access_pct":37,"Retention_pct":30,"Lat":-1.2595,"Lon":36.9087,"Paradox":True,"Beds":10,"Band":"5–15km"},
    {"Name":"Mama Lucy Kibaki Hospital","Type":"County Referral Hospital","Sector":"Public","Phone":"+254 020 231 0000","Specialties":"Surgery, Maternity, Paediatrics, Emergency, ICU","Dist_km":11.9,"Insurance_pct":52,"Wealth":"Middle","Access_pct":71,"Retention_pct":64,"Lat":-1.2762,"Lon":36.9195,"Paradox":False,"Beds":240,"Band":"5–15km"},
    {"Name":"Karen Hospital","Type":"Private Hospital","Sector":"Private","Phone":"+254 020 661 3000","Specialties":"Oncology, Cardiology, Neurology, ICU, Maternity","Dist_km":14.3,"Insurance_pct":94,"Wealth":"Highest","Access_pct":90,"Retention_pct":86,"Lat":-1.3418,"Lon":36.6930,"Paradox":False,"Beds":160,"Band":"5–15km"},
    {"Name":"Kiambu Level 4 Hospital","Type":"County Hospital","Sector":"Public","Phone":"+254 066 22 330","Specialties":"General Surgery, Maternity, Paediatrics, TB/DOTS","Dist_km":14.8,"Insurance_pct":48,"Wealth":"Middle","Access_pct":66,"Retention_pct":59,"Lat":-1.1711,"Lon":36.8347,"Paradox":False,"Beds":200,"Band":"5–15km"},
    {"Name":"Kikuyu Mission Hospital","Type":"Religious / Mission Hospital","Sector":"Faith-Based","Phone":"+254 020 203 2395","Specialties":"Ophthalmology, Orthopaedics, General Surgery, Maternity","Dist_km":17.3,"Insurance_pct":60,"Wealth":"Middle","Access_pct":73,"Retention_pct":67,"Lat":-1.2480,"Lon":36.6701,"Paradox":False,"Beds":160,"Band":"15–25km"},
    {"Name":"Nazareth Hospital — Limuru Road","Type":"Religious / Mission Hospital","Sector":"Faith-Based","Phone":"+254 020 200 2040","Specialties":"General Surgery, Maternity, Paediatrics, Radiology","Dist_km":15.5,"Insurance_pct":58,"Wealth":"Middle","Access_pct":68,"Retention_pct":61,"Lat":-1.1800,"Lon":36.7500,"Paradox":False,"Beds":120,"Band":"15–25km"},
    {"Name":"Ruiru Sub-County Hospital","Type":"Sub-County Hospital","Sector":"Public","Phone":"+254 067 52 304","Specialties":"General OPD, Maternity, Emergency, TB/DOTS","Dist_km":23.9,"Insurance_pct":42,"Wealth":"Middle","Access_pct":61,"Retention_pct":54,"Lat":-1.1449,"Lon":36.9612,"Paradox":False,"Beds":100,"Band":"15–25km"},
    {"Name":"AIC Kijabe Hospital","Type":"Religious / Mission Hospital","Sector":"Faith-Based","Phone":"+254 050 202 0270","Specialties":"Neurosurgery, Oncology, Paediatrics, Cleft Surgery","Dist_km":47.7,"Insurance_pct":62,"Wealth":"Middle","Access_pct":60,"Retention_pct":55,"Lat":-0.9360,"Lon":36.5930,"Paradox":False,"Beds":280,"Band":"25–50km"},
    {"Name":"Thika Level 5 Hospital","Type":"County Referral Hospital","Sector":"Public","Phone":"+254 067 221 000","Specialties":"Oncology, Dialysis, Orthopaedics, ICU, Cardiology","Dist_km":41.2,"Insurance_pct":52,"Wealth":"Richer","Access_pct":24,"Retention_pct":20,"Lat":-1.0332,"Lon":37.0693,"Paradox":False,"Beds":350,"Band":"25–50km"},
    {"Name":"Machakos Level 5 Hospital","Type":"County Referral Hospital","Sector":"Public","Phone":"+254 044 20 940","Specialties":"Oncology, General Surgery, Maternity, ICU, Paediatrics","Dist_km":55.2,"Insurance_pct":50,"Wealth":"Middle","Access_pct":55,"Retention_pct":48,"Lat":-1.5177,"Lon":37.2634,"Paradox":False,"Beds":400,"Band":"Over 50km"},
    {"Name":"Kajiado County Referral Hospital","Type":"County Referral Hospital","Sector":"Public","Phone":"+254 045 22 334","Specialties":"General Surgery, Maternity, Emergency, Paediatrics","Dist_km":61.1,"Insurance_pct":38,"Wealth":"Middle","Access_pct":45,"Retention_pct":39,"Lat":-1.8512,"Lon":36.7779,"Paradox":False,"Beds":180,"Band":"Over 50km"},
    {"Name":"Nakuru Level 5 Hospital","Type":"County Referral Hospital","Sector":"Public","Phone":"+254 051 221 2783","Specialties":"Oncology, General Surgery, Neurology, ICU, Maternity","Dist_km":140.5,"Insurance_pct":55,"Wealth":"Middle","Access_pct":62,"Retention_pct":55,"Lat":-0.2831,"Lon":36.0698,"Paradox":False,"Beds":500,"Band":"Over 50km"},
])

MODEL_PERF = pd.DataFrame([
    {"Algorithm": "XGBoost (Tuned) ★ Deployed",  "Stage": "Operational", "F1": 0.8091, "AUC": 0.8144, "Accuracy": 0.7222},
    {"Algorithm": "XGBoost (Tournament)",          "Stage": "Tournament",  "F1": 0.9343, "AUC": 0.5926, "Accuracy": 0.8768},
    {"Algorithm": "Ensemble (Top 3)",              "Stage": "Tournament",  "F1": 0.9343, "AUC": 0.5902, "Accuracy": 0.8767},
    {"Algorithm": "AdaBoost",                      "Stage": "Tournament",  "F1": 0.9343, "AUC": 0.5501, "Accuracy": 0.8766},
    {"Algorithm": "Gradient Boosting",             "Stage": "Tournament",  "F1": 0.9342, "AUC": 0.5762, "Accuracy": 0.8766},
    {"Algorithm": "Random Forest",                 "Stage": "Tournament",  "F1": 0.6573, "AUC": 0.5932, "Accuracy": 0.5282},
    {"Algorithm": "Logistic Regression",           "Stage": "Tournament",  "F1": 0.6611, "AUC": 0.6143, "Accuracy": 0.5342},
    {"Algorithm": "Decision Tree",                 "Stage": "Tournament",  "F1": 0.5010, "AUC": 0.5641, "Accuracy": 0.3963},
])

SHAP_DATA = pd.DataFrame([
    {"Feature": "Distance (km)",    "Importance": 0.41, "Category": "Enabling"},
    {"Feature": "Wealth Index",     "Importance": 0.18, "Category": "Enabling"},
    {"Feature": "Insurance Status", "Importance": 0.14, "Category": "Enabling"},
    {"Feature": "Residence Type",   "Importance": 0.09, "Category": "Predisposing"},
    {"Feature": "Education Level",  "Importance": 0.08, "Category": "Predisposing"},
    {"Feature": "Age Group",        "Importance": 0.05, "Category": "Predisposing"},
    {"Feature": "Gender",           "Importance": 0.03, "Category": "Predisposing"},
    {"Feature": "Provider Type",    "Importance": 0.02, "Category": "Need"},
])

GAM_DIST = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60]
GAM_PROB = [0.899, 0.905, 0.910, 0.914, 0.916, 0.918, 0.910, 0.895, 0.875, 0.840, 0.800]

SECTOR_COLORS = {
    "Public":      "#1E40AF",
    "Private":     "#7C3AED",
    "Faith-Based": "#0F766E",
}

LEGEND_COLORS = {
    "National Referral Hospital": "#1D4ED8",
    "County Referral Hospital":   "#2563EB",
    "County Hospital":            "#0891B2",
    "Sub-County Hospital":        "#0D9488",
    "Health Centre":              "#059669",
    "Clinic":                     "#65A30D",
    "Dispensary":                 "#CA8A04",
    "Private Hospital":           "#7C3AED",
    "Religious / Mission Hospital": "#E11D48",
}

ALL_SPECIALTIES = sorted({
    s.strip() for row in FACILITIES["Specialties"] for s in row.split(",")
})

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))

def make_map(df, show_ring=True):
    """Build a Folium map using CartoDB Voyager with white-bordered circle markers."""
    tile = st.session_state.map_style
    m = folium.Map(location=[-1.2921, 36.8219], zoom_start=11, tiles=tile)
    if show_ring:
        folium.Circle(
            location=[-1.3006, 36.8066], radius=25000,
            color="#1D4ED8", weight=2, fill=True,
            fill_color="#1D4ED8", fill_opacity=0.06,
            tooltip="25 km GAM critical threshold",
        ).add_to(m)
    for _, row in df.iterrows():
        is_paradox = row["Paradox"] and st.session_state.show_paradox
        fill_color = "#DC2626" if is_paradox else SECTOR_COLORS.get(row["Sector"], "#64748B")
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            radius=8,
            color="white",
            weight=2,
            fill=True,
            fill_color=fill_color,
            fill_opacity=0.92,
            tooltip=f"{row['Name']} · {row['Type']}",
            popup=folium.Popup(f"""
                <div style='font-family:sans-serif;font-size:12px;min-width:200px;'>
                  <b style='color:#0B3D6E;font-size:13px;'>{row['Name']}</b><br>
                  <span style='color:#6B84A0;'>{row['Type']} · {row['Sector']}</span><br><br>
                  <b>Specialties:</b> {row['Specialties']}<br><br>
                  <table style='width:100%;font-size:11px;'>
                    <tr><td style='color:#6B84A0;'>Distance:</td><td><b>{row['Dist_km']} km</b></td></tr>
                    <tr><td style='color:#6B84A0;'>Access rate:</td><td><b>{row['Access_pct']}%</b></td></tr>
                    <tr><td style='color:#6B84A0;'>Retention:</td><td><b>{row['Retention_pct']}%</b></td></tr>
                    {'<tr><td colspan=2 style="color:#DC2626;font-weight:bold;">⚠ Urban Proximity Paradox</td></tr>' if row["Paradox"] else ''}
                  </table>
                </div>""", max_width=260),
        ).add_to(m)
    return m

# ── SIDEBAR ────────────────────────────────────────────────────────
user = st.session_state.user
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:20px 0 14px;'>
      <div style='font-size:42px;'>⚕️</div>
      <div style='font-size:17px;font-weight:800;color:{acc};margin-top:6px;'>HealthLink Kenya</div>
      <div style='font-size:11px;color:{muted};margin-top:4px;'>Predictive Framework · Healthcare Access</div>
    </div>
    <div style='background:{"#21262D" if is_dark else "#F0F4FA"};border-radius:10px;
                padding:10px 14px;margin-bottom:10px;'>
      <div style='font-size:12px;font-weight:700;color:{acc};'>👤 {user.get("name","User")}</div>
      <div style='font-size:11px;color:{muted};'>{user.get("role","")}</div>
      <div style='font-size:10px;color:{muted};margin-top:2px;opacity:.7;'>{user.get("email","")}</div>
    </div>""", unsafe_allow_html=True)

    if models_ok is True:
        st.markdown(f"""<div style='background:#EDFBF5;border:1px solid #A8E6D0;border-radius:8px;
            padding:8px 12px;font-size:11px;color:#065F46;margin-bottom:8px;'>
            ✅ Models loaded — live predictions active</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style='background:#FFF5F5;border:1px solid #FBCACA;border-radius:8px;
            padding:8px 12px;font-size:11px;color:#DC2626;margin-bottom:8px;'>
            ⚠️ Model load issue — using fallback values</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""<div style='font-size:10px;color:{muted};line-height:2.0;'>
      <b>Access model:</b> XGBoost (Tuned)<br>
      <b>F1:</b> 0.8091 · AUC: 0.8144<br>
      <b>Retention model:</b> XGBoost Stage 2<br>
      <b>AUC:</b> 0.8510 (SMOTE retrain)<br>
      <b>Data:</b> KNBS HSB Survey 2022<br>
      <b>n =</b> 99,031 observations<br>
      <b>GAM threshold:</b> 25 km<br>
      <b>Decision threshold:</b> {OPTIMAL_THRESHOLD}
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    _, toggle_col = st.columns([3, 1])
    with toggle_col:
        if st.button("☀️" if is_dark else "🌙", use_container_width=True):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = {}
        st.rerun()

# ══════════════════════════════════════════════════════════════════
# PAGE FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def page_overview():
    st.markdown("## Overview & Insights")
    st.caption("KNBS Health-Seeking Behaviour Survey 2022 · n = 99,031 · XGBoost Operational Model")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Population Access Rate",   "78.4%", "+3.2% vs prev. quarter")
    k2.metric("Retention Rate",           "71.2%", "+1.8% vs prev. quarter")
    k3.metric("GAM Critical Threshold",   "25 km", "Access drops sharply beyond")
    k4.metric("Urban Proximity Paradox",  "3,484", "Patients facing hidden barriers")

    st.markdown("---")
    st.markdown("### Andersen's Behavioural Model — Feature Weight by Category")
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown(f"""<div class='med-card-amber'>
          <div style='font-size:12px;font-weight:700;color:#92400E;text-transform:uppercase;'>Enabling Factors · 73%</div>
          <div style='font-size:13px;color:{muted};margin-top:10px;line-height:2.2;'>
            Distance to Facility &nbsp;<b style='color:{text};'>41%</b><br>
            Wealth Index &nbsp;<b style='color:{text};'>18%</b><br>
            Insurance Status &nbsp;<b style='color:{text};'>14%</b>
          </div>
          <div style='font-size:10px;color:#B45309;margin-top:10px;font-weight:600;'>Dominant predictors · TreeSHAP</div>
        </div>""", unsafe_allow_html=True)
    with cb:
        st.markdown(f"""<div class='med-card-blue'>
          <div style='font-size:12px;font-weight:700;color:#1E3A8A;text-transform:uppercase;'>Predisposing Factors · 25%</div>
          <div style='font-size:13px;color:{muted};margin-top:10px;line-height:2.2;'>
            Residence Type &nbsp;<b style='color:{text};'>9%</b><br>
            Education Level &nbsp;<b style='color:{text};'>8%</b><br>
            Age Group &nbsp;<b style='color:{text};'>5%</b> &nbsp;Gender &nbsp;<b style='color:{text};'>3%</b>
          </div>
          <div style='font-size:10px;color:#1D4ED8;margin-top:10px;font-weight:600;'>Demographic &amp; social attributes</div>
        </div>""", unsafe_allow_html=True)
    with cc:
        st.markdown(f"""<div class='med-card-green'>
          <div style='font-size:12px;font-weight:700;color:#065F46;text-transform:uppercase;'>Need Factors · 2%</div>
          <div style='font-size:13px;color:{muted};margin-top:10px;line-height:2.2;'>
            Provider Group &nbsp;<b style='color:{text};'>2%</b><br>
            Perceived health need<br>Triage classification
          </div>
          <div style='font-size:10px;color:#059669;margin-top:10px;font-weight:600;'>Lowest individual weight</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    cl, cr = st.columns(2)
    fac_types  = ["National Referral", "County Hospital", "Sub-County", "Health Centre", "Dispensary/Clinic"]
    access_v   = [94, 79, 61, 52, 37]
    retain_v   = [89, 71, 53, 44, 30]
    with cl:
        st.markdown("#### Access Rate by Facility Type")
        fig = go.Figure(go.Bar(
            x=access_v, y=fac_types, orientation="h",
            marker_color=[acc if v >= 50 else "#EF4444" for v in access_v],
            text=[f"{v}%" for v in access_v], textposition="outside",
            textfont=dict(color=TICK, size=13)))
        fig.update_layout(paper_bgcolor=card, plot_bgcolor=card, height=260,
            margin=dict(l=0, r=60, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor=border, range=[0, 115], tickfont=dict(color=TICK)),
            yaxis=dict(tickfont=dict(color=TICK, size=13)), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with cr:
        st.markdown("#### Access → Retention Gap")
        gaps = [a - r for a, r in zip(access_v, retain_v)]
        fig2 = go.Figure(go.Bar(
            x=gaps, y=fac_types, orientation="h",
            marker_color=["#EF4444" if g > 12 else "#F59E0B" if g > 8 else "#10B981" for g in gaps],
            text=[f"{v}pp" for v in gaps], textposition="outside",
            textfont=dict(color=TICK, size=13)))
        fig2.update_layout(paper_bgcolor=card, plot_bgcolor=card, height=260,
            margin=dict(l=0, r=70, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor=border, range=[0, 25],
                       tickfont=dict(color=TICK),
                       title=dict(text="Access–Retention gap (pp)", font=dict(color=TICK))),
            yaxis=dict(tickfont=dict(color=TICK, size=13)), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""<div class='med-card-red'><b style='color:#DC2626;'>⚠️ Urban Proximity Paradox Detected</b><br>
      <span style='font-size:12px;color:{muted};'>3,484 patients within &lt;50 km failed to access care despite
      favourable profiles. Flagged: <b style='color:{text};'>Mathare North HC · Kayole Sub-County · Dandora Dispensary</b>.</span>
    </div>""", unsafe_allow_html=True)


def page_triage():
    st.markdown("## Predictive Triage & Nearby Facilities")
    st.caption("Enter patient profile → live XGBoost prediction → see nearby facilities on map")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Patient Demographics")
        age_group = st.selectbox("Age Group", ["0-4","5-14","15-24","25-34","35-49","50-64","65+"])
        gender    = st.selectbox("Gender", ["Female", "Male"])
        residence = st.radio("Residence Type", ["Urban","Rural"], horizontal=True)
    with c2:
        st.markdown("#### Enabling Factors")
        wealth    = st.select_slider("Wealth Index", options=["Poorest","Poorer","Middle","Richer","Richest"])
        insurance = st.radio("Insurance Status", ["Insured","Uninsured"], horizontal=True)
        distance  = st.slider("Distance to Nearest Facility (km)", 0.0, 100.0, 5.0, 0.5)

    if distance > 25:
        st.markdown(f"""<div class='med-card-red' style='margin-top:8px;'>
          <b style='color:#DC2626;'>📍 Beyond GAM Threshold (25 km)</b> —
          <span style='font-size:12px;color:{muted};'>Access probability drops sharply.
          Consider mobile clinic or CHW intervention.</span></div>""", unsafe_allow_html=True)
    elif distance > 15:
        st.markdown(f"""<div class='med-card-amber' style='margin-top:8px;'>
          <span style='font-size:12px;color:#92400E;'>⚡ Approaching critical zone (15–25 km).
          Monitor this catchment.</span></div>""", unsafe_allow_html=True)

    notes = st.text_area("Clinical Notes (optional)", height=70,
                         value="Patient reports difficulty travelling to facility.")

    if st.button("Run Access Prediction"):
        insured = 1 if insurance == "Insured" else 0
        prob, src = predict_access(distance, age_group, gender, wealth, insured, residence)
        pred = 1 if (prob / 100) >= OPTIMAL_THRESHOLD else 0
        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("Access Probability", f"{prob}%", f"XGBoost · {src}")
        m2.metric("Prediction", "Will Access ✅" if pred == 1 else "Will NOT Access ❌")
        m3.metric("Distance Zone", ">25 km ⚠️" if distance > 25 else "Safe Zone ✅")
        st.progress(min(prob / 100, 1.0))
        if prob >= 70:
            st.markdown(f'<div class="med-card-green"><b style="color:#065F46;">✅ High likelihood of access.</b></div>', unsafe_allow_html=True)
        elif prob >= 40:
            st.markdown(f'<div class="med-card-amber"><b style="color:#92400E;">⚡ Moderate — consider outreach support.</b></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="med-card-red"><b style="color:#DC2626;">🚨 Low likelihood — prioritise mobile clinic or CHW.</b></div>', unsafe_allow_html=True)
        if notes.strip():
            st.info("Clinical notes received. Keywords are for display only — they do not affect the probability score.")

    st.markdown("---")
    st.markdown("#### Nearby Facilities")
    nearby = FACILITIES[FACILITIES["Dist_km"] <= max(distance + 10, 15)].copy()
    s1, s2, s3 = st.columns(3)
    s1.metric("Facilities in Range", len(nearby))
    s2.metric("Avg Access Rate", f"{nearby['Access_pct'].mean():.1f}%")
    s3.metric("Paradox Facilities", int(nearby["Paradox"].sum()))
    st_folium(make_map(nearby), width="100%", height=400)
    st.markdown("#### Facility Quick Reference")
    qref = nearby[["Name","Type","Dist_km","Access_pct","Specialties"]].copy()
    qref.columns = ["Facility","Type","Dist (km)","Access %","Specialties"]
    st.dataframe(qref, use_container_width=True, hide_index=True)


def page_geospatial():
    st.markdown("## Geospatial Facility Mapper")
    st.caption("Full facility map · Distance bands · Specialty filter · Click to find nearest facility")

    fc1, fc2 = st.columns([2, 2])
    with fc1:
        sel_types = st.multiselect("Filter by Facility Type",
                                   options=sorted(FACILITIES["Type"].unique()),
                                   default=list(FACILITIES["Type"].unique()))
    with fc2:
        sel_spec = st.multiselect("Filter by Specialty", options=ALL_SPECIALTIES,
                                  placeholder="All specialties shown")

    c_dist, c_band, c_ring = st.columns([1, 2, 1])
    with c_dist:
        max_dist = st.slider("Max distance (km)", 1, 170, 80)
    with c_band:
        band_opts = ["All bands","Under 5km","5–15km","15–25km","25–50km","Over 50km"]
        sel_band  = st.radio("Distance band", band_opts, horizontal=True)
    with c_ring:
        show_ring = st.checkbox("25 km GAM ring", value=True)

    filt = FACILITIES[
        (FACILITIES["Dist_km"] <= max_dist) &
        (FACILITIES["Type"].isin(sel_types))
    ].copy()
    if sel_band != "All bands":
        filt = filt[filt["Band"] == sel_band]
    if sel_spec:
        filt = filt[filt["Specialties"].apply(lambda s: any(sp in s for sp in sel_spec))]

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Facilities in Range", len(filt))
    s2.metric("Avg Access Rate",  f"{filt['Access_pct'].mean():.1f}%" if len(filt) else "—")
    s3.metric("Paradox Facilities", int(filt["Paradox"].sum()))
    s4.metric("Types Shown", len(filt["Type"].unique()))

    map_data = st_folium(make_map(filt, show_ring=show_ring),
                         width="100%", height=520,
                         returned_objects=["last_clicked"])

    # Map legend
    st.markdown("#### Map Legend — Sector")
    leg_cols = st.columns(3)
    for i, (sector, color) in enumerate(SECTOR_COLORS.items()):
        leg_cols[i].markdown(
            f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px;'>"
            f"<div style='width:14px;height:14px;border-radius:50%;background:{color};"
            f"border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.25);flex-shrink:0;'></div>"
            f"<span style='font-size:12px;color:{muted};'>{sector}</span></div>",
            unsafe_allow_html=True)
    if st.session_state.show_paradox:
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:8px;margin-top:4px;'>"
            f"<div style='width:14px;height:14px;border-radius:50%;background:#DC2626;"
            f"border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.25);flex-shrink:0;'></div>"
            f"<span style='font-size:12px;color:#DC2626;font-weight:600;'>Urban Proximity Paradox</span></div>",
            unsafe_allow_html=True)

    # Nearest facility on click
    if map_data and map_data.get("last_clicked"):
        clat = map_data["last_clicked"]["lat"]
        clng = map_data["last_clicked"]["lng"]
        FACILITIES["_d"] = FACILITIES.apply(
            lambda r: haversine(clat, clng, r["Lat"], r["Lon"]), axis=1)
        nearest = FACILITIES.nsmallest(3, "_d")
        closest = nearest.iloc[0]
        in_zone = closest["_d"] <= 25
        zcls = "med-card-green" if in_zone else "med-card-red"
        zcol = "#065F46"        if in_zone else "#DC2626"
        zlbl = "Within 25 km safe zone ✅" if in_zone else "Beyond 25 km — access risk zone ⚠️"
        st.markdown(f"""<div class='{zcls}' style='margin-top:16px;'>
          <b style='color:{zcol};'>📍 Clicked ({clat:.4f}, {clng:.4f}) — {zlbl}</b><br>
          <span style='font-size:12px;color:{muted};'>Distance to nearest: <b style='color:{text};'>{closest['_d']:.1f} km</b></span>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:13px;font-weight:700;color:{text};margin:12px 0 8px;'>3 Nearest Facilities:</div>", unsafe_allow_html=True)
        for _, row in nearest.iterrows():
            d     = row["_d"]
            dcol  = "#065F46" if d <= 25 else "#92400E" if d <= 40 else "#DC2626"
            abadg = "badge-green" if row["Access_pct"] >= 70 else "badge-amber" if row["Access_pct"] >= 50 else "badge-red"
            st.markdown(f"""<div class='med-card' style='border-left:3px solid {acc};margin-bottom:8px;'>
              <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                  <div style='font-size:14px;font-weight:700;color:{acc};'>{row['Name']}</div>
                  <div style='font-size:11px;color:{muted};margin:3px 0 6px;'>{row['Type']}</div>
                  <span class='{abadg}'>Access: {row['Access_pct']}%</span>
                  <span class='badge-amber'>Retention: {row['Retention_pct']}%</span>
                  {'<span class="badge-red">⚠️ Paradox</span>' if row["Paradox"] else ''}
                </div>
                <div style='text-align:right;min-width:80px;'>
                  <div style='font-size:20px;font-weight:900;color:{dcol};'>{d:.1f} km</div>
                  <div style='font-size:10px;color:{muted};'>from click</div>
                </div>
              </div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Facility Directory")
    for _, row in filt.sort_values("Dist_km").iterrows():
        ab = "badge-green" if row["Access_pct"] >= 70 else "badge-amber" if row["Access_pct"] >= 50 else "badge-red"
        rb = "badge-green" if row["Retention_pct"] >= 70 else "badge-amber" if row["Retention_pct"] >= 50 else "badge-red"
        pflag  = "<span class='badge-red'>⚠️ Urban Paradox</span>" if row["Paradox"] else ""
        carcls = "med-card-red" if row["Paradox"] else "med-card"
        gurl   = f"https://www.google.com/maps/dir/?api=1&destination={row['Lat']},{row['Lon']}&travelmode=driving"
        st.markdown(f"""<div class='{carcls}' style='border-left:4px solid {acc};margin-bottom:14px;'>
          <div style='display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;'>
            <div style='flex:1;min-width:220px;'>
              <div style='font-size:15px;font-weight:800;color:{acc};margin-bottom:3px;'>{row['Name']}</div>
              <div style='font-size:11px;color:{muted};margin-bottom:8px;'>{row['Type']} · {row['Dist_km']} km · {row['Beds']} beds</div>
              <div style='margin-bottom:8px;display:flex;flex-wrap:wrap;gap:4px;'>
                <span class='badge-blue'>{row['Sector']}</span>
                <span class='{ab}'>Access: {row['Access_pct']}%</span>
                <span class='{rb}'>Retention: {row['Retention_pct']}%</span>
                {pflag}
              </div>
              <div style='font-size:11px;color:{muted};'><b style='color:{text};'>Specialties:</b> {row['Specialties']}</div>
            </div>
            <div style='display:flex;flex-direction:column;gap:8px;min-width:140px;align-items:flex-end;'>
              <a href='tel:{row["Phone"]}' style='display:flex;align-items:center;gap:6px;background:{acc};
                 color:#FFFFFF;padding:8px 16px;border-radius:8px;font-size:12px;font-weight:700;
                 text-decoration:none;width:130px;justify-content:center;'>📞 Call Facility</a>
              <a href='{gurl}' target='_blank' style='display:flex;align-items:center;gap:6px;background:#10B981;
                 color:#FFFFFF;padding:8px 16px;border-radius:8px;font-size:12px;font-weight:700;
                 text-decoration:none;width:130px;justify-content:center;'>🧭 Get Directions</a>
            </div>
          </div></div>""", unsafe_allow_html=True)


def page_retention():
    st.markdown("## Patient Retention Record")
    st.caption("Existing patient follow-up · Visit history · Treatment continuity")

    sc, sb = st.columns([3, 1])
    with sc:
        st.text_input("Search by Patient ID or National ID", placeholder="e.g. PT-2024-00142")
    with sb:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        st.button("Load Record", use_container_width=True)

    st.markdown("---")
    pt = {
        "id":"PT-2024-00142","name":"Amina Wanjiru Kariuki","dob":"14 March 1987","age":37,
        "gender":"Female","national_id":"23456781","nhif_no":"NHIF-KE-882341",
        "insurance":"NHIF (Active)","facility":"Mbagathi District Hospital",
        "clinician":"Dr. P. Ochieng","blood_group":"O+","allergies":"Penicillin, Sulfonamides",
        "phone":"+254 712 345 678","county":"Nairobi","distance_km":8.1,
        "wealth":"Middle","residence":"Urban",
        "next_appointment":"28 March 2026","last_visit":"12 February 2026",
        "visits_ytd":4,"total_visits":17,
        "conditions":["Hypertension","Type 2 Diabetes"],
        "medications":[
            {"Drug":"Amlodipine 5mg","Dose":"1 tab OD","Refill Due":"28 Mar 2026","Status":"Active"},
            {"Drug":"Metformin 500mg","Dose":"1 tab BD","Refill Due":"28 Mar 2026","Status":"Active"},
            {"Drug":"Atorvastatin 20mg","Dose":"1 tab ON","Refill Due":"28 Mar 2026","Status":"Active"},
        ],
        "visits":[
            {"Date":"12 Feb 2026","Facility":"Mbagathi District Hospital","Type":"Chronic Disease Review","Clinician":"Dr. P. Ochieng","BP":"138/88","Sugar":"7.4 mmol/L","Notes":"Well-controlled. Refill issued."},
            {"Date":"10 Jan 2026","Facility":"Mbagathi District Hospital","Type":"Routine OPD","Clinician":"Dr. P. Ochieng","BP":"142/92","Sugar":"8.1 mmol/L","Notes":"Metformin dose increased."},
            {"Date":"05 Nov 2025","Facility":"Mbagathi District Hospital","Type":"Emergency (Hypertensive)","Clinician":"Dr. R. Njoroge","BP":"178/104","Sugar":"9.2 mmol/L","Notes":"IV antihypertensive. Admitted overnight."},
        ],
        "investigations":[
            {"Test":"HbA1c","Date":"12 Feb 2026","Result":"7.8%","Normal Range":"<7.0%","Flag":"⚠️ Elevated"},
            {"Test":"Fasting Glucose","Date":"12 Feb 2026","Result":"7.4 mmol/L","Normal Range":"3.9–5.5 mmol/L","Flag":"⚠️ Elevated"},
            {"Test":"BP","Date":"12 Feb 2026","Result":"138/88 mmHg","Normal Range":"<130/80 mmHg","Flag":"⚠️ Elevated"},
            {"Test":"Renal Function","Date":"10 Jan 2026","Result":"Creatinine 82","Normal Range":"62–106 µmol/L","Flag":"✅ Normal"},
        ],
        "referrals":[
            {"Date":"12 Feb 2026","Referred To":"KNH — Cardiology","Reason":"Uncontrolled hypertension, cardiac risk assessment","Status":"Pending"},
        ],
    }

    live_acc, acc_src = predict_access(pt["distance_km"], "35-49", pt["gender"], pt["wealth"], 1, pt["residence"])
    live_ret, ret_src = predict_retention(pt["distance_km"], "35-49", pt["gender"], pt["wealth"], 1, pt["residence"])

    st.markdown(f"""<div class='med-card' style='border-left:4px solid {acc};'>
      <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
        <div>
          <div style='font-size:22px;font-weight:800;color:{acc};'>{pt["name"]}</div>
          <div style='font-size:12px;color:{muted};margin-top:4px;'>
            ID: <b style='color:{text};'>{pt["id"]}</b> &nbsp;·&nbsp;
            NID: <b style='color:{text};'>{pt["national_id"]}</b> &nbsp;·&nbsp;
            NHIF: <b style='color:{text};'>{pt["nhif_no"]}</b>
          </div>
          <div style='margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;'>
            <span class='badge-blue'>{pt["age"]} yrs · {pt["gender"]}</span>
            <span class='badge-green'>{pt["insurance"]}</span>
            <span class='badge-blue'>Blood: {pt["blood_group"]}</span>
            <span class='badge-red'>⚠ Allergies: {pt["allergies"]}</span>
          </div>
        </div>
        <div style='text-align:right;'>
          <div style='font-size:11px;color:{muted};'>Attending Facility</div>
          <div style='font-size:13px;font-weight:700;color:{acc};'>{pt["facility"]}</div>
          <div style='font-size:11px;color:{muted};margin-top:2px;'>{pt["clinician"]}</div>
        </div>
      </div></div>""", unsafe_allow_html=True)

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Access Probability",    f"{int(round(live_acc))}%",  f"XGBoost · {acc_src}")
    a2.metric("Retention Probability", f"{int(round(live_ret))}%",  f"Stage 2 · {ret_src}")
    a3.metric("Next Appointment",      pt["next_appointment"])
    a4.metric("Visits YTD / Total",    f"{pt['visits_ytd']} / {pt['total_visits']}")

    t1, t2, t3, t4, t5 = st.tabs(["Summary","Visit History","Medications","Investigations","Referrals"])

    with t1:
        pc1, pc2 = st.columns(2)
        with pc1:
            st.markdown("#### Personal Details")
            for label, val in [("Date of Birth",pt["dob"]),("County",pt["county"]),
                                ("Phone",pt["phone"]),("Residence",pt["residence"]),
                                ("Wealth Index",pt["wealth"]),
                                ("Distance to Facility",f"{pt['distance_km']} km"),
                                ("Last Visit",pt["last_visit"])]:
                st.markdown(f"<div class='pt-row'><span class='pt-label'>{label}</span><span class='pt-value'>{val}</span></div>", unsafe_allow_html=True)
        with pc2:
            st.markdown("#### Active Conditions")
            for cond in pt["conditions"]:
                st.markdown(f"<div class='med-card-blue' style='margin-bottom:8px;'><span style='font-size:13px;font-weight:600;color:#1D4ED8;'>🩺 {cond}</span></div>", unsafe_allow_html=True)
            d = pt["distance_km"]
            if d <= 25:   zc, zl, zb = "#065F46", "✅ Safe Zone (≤25 km)",    "#EDFBF5"
            elif d <= 50: zc, zl, zb = "#92400E", "⚠️ Transition Zone",        "#FFFBEE"
            else:         zc, zl, zb = "#DC2626", "🚨 Exclusion Zone",          "#FFF5F5"
            st.markdown(f"""<div style='background:{zb};border-radius:10px;padding:14px 16px;margin-top:12px;'>
              <div style='font-size:11px;color:{muted};text-transform:uppercase;font-weight:600;'>GAM Distance Zone</div>
              <div style='font-size:16px;font-weight:800;color:{zc};margin-top:4px;'>{zl}</div>
              <div style='font-size:12px;color:{muted};margin-top:2px;'>{d} km from registered facility</div>
            </div>""", unsafe_allow_html=True)

    with t2:
        for v in pt["visits"]:
            flag = "🚨" if "Emergency" in v["Type"] else "📋"
            st.markdown(f"""<div class='med-card' style='border-left:3px solid {acc};'>
              <div style='display:flex;justify-content:space-between;'>
                <span style='font-size:13px;font-weight:700;color:{acc};'>{flag} {v["Type"]}</span>
                <span class='badge-grey'>{v["Clinician"]}</span>
              </div>
              <div style='font-size:11px;color:{muted};margin-top:3px;'>{v["Date"]} · {v["Facility"]}</div>
              <div style='font-size:12px;color:{muted};margin-top:6px;'>BP: <b style='color:{text};'>{v["BP"]}</b> &nbsp; BGL: <b style='color:{text};'>{v["Sugar"]}</b></div>
              <div style='font-size:12px;color:{muted};margin-top:4px;'>{v["Notes"]}</div>
            </div>""", unsafe_allow_html=True)

    with t3:
        for med in pt["medications"]:
            st.markdown(f"""<div class='med-card' style='display:flex;justify-content:space-between;'>
              <div>
                <div style='font-size:14px;font-weight:700;color:{acc};'>💊 {med["Drug"]}</div>
                <div style='font-size:12px;color:{muted};margin-top:3px;'>Dose: <b style='color:{text};'>{med["Dose"]}</b></div>
              </div>
              <div style='text-align:right;'>
                <div style='font-size:11px;color:{muted};'>Refill Due</div>
                <div style='font-size:13px;font-weight:700;color:{acc};'>{med["Refill Due"]}</div>
                <span class='badge-green'>{med["Status"]}</span>
              </div>
            </div>""", unsafe_allow_html=True)

    with t4:
        st.dataframe(pd.DataFrame(pt["investigations"]), use_container_width=True, hide_index=True)

    with t5:
        for ref in pt["referrals"]:
            st.markdown(f"""<div class='med-card-blue'>
              <div style='font-size:13px;font-weight:700;color:#1D4ED8;'>🔀 {ref["Referred To"]}</div>
              <div style='font-size:12px;color:{muted};margin-top:4px;'>
                Date: <b style='color:{text};'>{ref["Date"]}</b> &nbsp;·&nbsp;
                Status: <span class='badge-amber'>{ref["Status"]}</span>
              </div>
              <div style='font-size:12px;color:{muted};margin-top:6px;'>{ref["Reason"]}</div>
            </div>""", unsafe_allow_html=True)


def page_gam():
    st.markdown("## Distance Decay — GAM Analysis")
    st.caption("Generalised Additive Model spline · Critical inflection at 25 km · KNBS 2022")

    st.markdown(f"""<div class='med-card-amber' style='margin-bottom:16px;'>
      <b style='color:#92400E;'>Interpretation Note</b><br>
      <span style='font-size:11px;color:{muted};'>Probabilities reflect <b>within-cohort variation</b> among KNBS survey
      respondents. The high baseline (~90%) reflects positive selection bias — individuals who never sought care are absent
      from the survey. The <b>25 km inflection</b> marks where distance-decay accelerates within this cohort.</span>
    </div>""", unsafe_allow_html=True)

    fig = go.Figure()
    safe_d = [d for d in GAM_DIST if d <= 25];  safe_p = [p for d, p in zip(GAM_DIST, GAM_PROB) if d <= 25]
    risk_d = [d for d in GAM_DIST if d >= 25];  risk_p = [p for d, p in zip(GAM_DIST, GAM_PROB) if d >= 25]
    fig.add_trace(go.Scatter(x=safe_d + [25], y=safe_p + [0.918], fill="tozeroy",
        fillcolor="rgba(16,185,129,0.10)", line=dict(color="rgba(0,0,0,0)"), showlegend=False))
    fig.add_trace(go.Scatter(x=risk_d, y=risk_p, fill="tozeroy",
        fillcolor="rgba(239,68,68,0.08)", line=dict(color="rgba(0,0,0,0)"), showlegend=False))
    fig.add_trace(go.Scatter(x=GAM_DIST, y=GAM_PROB, mode="lines+markers",
        line=dict(color=acc, width=3), marker=dict(size=7, color=acc),
        name="P(Access | Distance) — within cohort",
        hovertemplate="Distance: %{x} km<br>Access Prob: %{y:.0%}"))
    fig.add_vline(x=25, line_dash="dash", line_color="#F59E0B", line_width=2,
        annotation_text="25 km — decay accelerates",
        annotation_font_color="#F59E0B", annotation_position="top right")
    fig.update_layout(paper_bgcolor=card, plot_bgcolor=card, font_color=text, height=420,
        xaxis=dict(title="Distance to Nearest Facility (km)", color=muted,
                   gridcolor=border, tickfont=dict(color=TICK)),
        yaxis=dict(title="Probability of Accessing Care (within cohort)",
                   tickformat=".0%", color=muted, gridcolor=border, tickfont=dict(color=TICK)),
        legend=dict(bgcolor=card, bordercolor=border),
        margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"""<div class='med-card-green'><b style='color:#065F46;'>0–25 km · Stable Zone</b><br>
      <span style='font-size:11px;color:{muted};'>Access probability 89.9–91.8% within the surveyed cohort.</span></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class='med-card-amber'><b style='color:#92400E;'>25 km · Decay Threshold</b><br>
      <span style='font-size:11px;color:{muted};'>GAM-derived inflection. Evidence base for mobile clinic radius recalibration.</span></div>""", unsafe_allow_html=True)
    with c3: st.markdown(f"""<div class='med-card-red'><b style='color:#DC2626;'>&gt;25 km · Declining Zone</b><br>
      <span style='font-size:11px;color:{muted};'>Access declines to 84.0% at 50 km. Priority zone for outreach.</span></div>""", unsafe_allow_html=True)


def page_analytics():
    st.markdown("## Analytics & Model Visuals")
    st.caption("SHAP feature importance · Algorithm tournament · Model performance comparison")

    tab_shap, tab_perf = st.tabs(["SHAP Interpretability", "Model Performance"])

    with tab_shap:
        col_chart, col_ins = st.columns([3, 2])
        with col_chart:
            cat_colors = {"Enabling":"#F59E0B","Predisposing":"#6366F1","Need":"#10B981"}
            bar_colors = [cat_colors[c] for c in SHAP_DATA["Category"]]
            fig = go.Figure(go.Bar(
                x=SHAP_DATA["Importance"] * 100, y=SHAP_DATA["Feature"], orientation="h",
                marker_color=bar_colors,
                text=[f"{v*100:.0f}%" for v in SHAP_DATA["Importance"]],
                textposition="outside", textfont=dict(color=TICK, size=12),
                hovertemplate="%{y}<br>Importance: %{x:.1f}%<extra></extra>"))
            fig.update_layout(paper_bgcolor=card, plot_bgcolor=card, height=340,
                xaxis=dict(title="SHAP Importance (%)", tickfont=dict(color=TICK),
                           gridcolor=border, range=[0, 55]),
                yaxis=dict(tickfont=dict(color=TICK, size=12), autorange="reversed"),
                margin=dict(l=10, r=60, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            lc = st.columns(3)
            for i, (cat, col) in enumerate(cat_colors.items()):
                total = SHAP_DATA[SHAP_DATA["Category"] == cat]["Importance"].sum() * 100
                lc[i].markdown(f"""<div style='background:{col}18;border:1px solid {col}40;border-radius:8px;
                    padding:8px 12px;text-align:center;'>
                    <div style='font-size:10px;color:{col};font-weight:700;text-transform:uppercase;'>{cat}</div>
                    <div style='font-size:20px;font-weight:900;color:{col};'>{total:.0f}%</div>
                    <div style='font-size:10px;color:{muted};'>combined weight</div>
                </div>""", unsafe_allow_html=True)
        with col_ins:
            st.markdown(f"""
            <div class='med-card-amber' style='margin-bottom:12px;'>
              <b style='color:#92400E;'>Dominant Signal: Distance</b><br>
              <span style='font-size:11px;color:{muted};'>Distance drives 41% of model decisions —
              more than all socioeconomic features combined.</span>
            </div>
            <div class='med-card-blue' style='margin-bottom:12px;'>
              <b style='color:#1D4ED8;'>Enabling: 73% Combined</b><br>
              <span style='font-size:11px;color:{muted};'>Distance + Wealth + Insurance = 73% of model weight.
              Targeting all three yields the highest policy ROI.</span>
            </div>
            <div class='med-card-green'>
              <b style='color:#065F46;'>Predisposing: 25%</b><br>
              <span style='font-size:11px;color:{muted};'>Residence type (urban vs rural) is the
              strongest predisposing signal.</span>
            </div>""", unsafe_allow_html=True)

    with tab_perf:
        st.markdown(f"""<div class='med-card-amber' style='margin-bottom:12px;'>
          <b style='color:#92400E;'>⚠️ Two evaluation stages — read carefully</b><br>
          <span style='font-size:11px;color:{muted};'>The ★ Deployed row shows the tuned model after
          class-imbalance correction (F1 0.8091 · AUC 0.8144). All other rows are pre-tuning tournament
          scores — high F1 (~0.93) reflects majority-class dominance, not balanced performance.</span>
        </div>""", unsafe_allow_html=True)

        def style_row(row):
            if "Deployed" in str(row["Algorithm"]):
                return [f"background-color:{card_b};color:{acc};font-weight:600"] * len(row)
            return [f"color:{text}"] * len(row)

        st.dataframe(MODEL_PERF.style.apply(style_row, axis=1),
                     use_container_width=True, hide_index=True)
        st.markdown("---")
        fig = go.Figure()
        for col_name, color in [("F1", acc), ("AUC", "#0891B2"), ("Accuracy", "#6366F1")]:
            fig.add_trace(go.Bar(name=col_name, x=MODEL_PERF["Algorithm"],
                                 y=MODEL_PERF[col_name], marker_color=color, opacity=0.85))
        fig.update_layout(barmode="group", paper_bgcolor=card, plot_bgcolor=card, height=350,
            xaxis=dict(tickfont=dict(color=TICK), gridcolor=border, tickangle=-25),
            yaxis=dict(tickfont=dict(color=TICK), gridcolor=border, range=[0, 1.05]),
            legend=dict(bgcolor=card, bordercolor=border),
            margin=dict(l=10, r=10, t=10, b=80))
        st.plotly_chart(fig, use_container_width=True)


def page_faq():
    st.markdown("## FAQ & How It Works")
    st.caption("Plain-English guide to the HealthLink Kenya platform")

    faqs = [
        ("What does this dashboard do?",
         "HealthLink Kenya is a clinical decision-support tool that helps administrators decide <b>where to send patients</b>. It uses a machine learning model trained on 99,031 real Kenyans to predict whether a patient is likely to access healthcare."),
        ("Who is this tool designed for?",
         "Hospital administrators, referral coordinators, community health workers, health planners at county and national level, and researchers studying healthcare access in Kenya."),
        ("What is the 25 km rule?",
         "A Generalised Additive Model applied to the KNBS 2022 survey shows access probability peaks at <b>91.8% at 25 km</b> then declines. <b>Important:</b> the high baseline reflects positive selection bias — the survey captured people who already engaged with facilities. The 25 km mark is where distance-decay accelerates within this cohort."),
        ("What is the Urban Proximity Paradox?",
         "3,484 patients who lived close to a hospital still failed to access care. Hidden barriers — long wait times, indirect costs, poor perceived service quality — matter as much as distance."),
        ("How does the Access Prediction work?",
         "The Triage page loads the trained XGBoost pipeline (<code>health_access_pipeline.pkl</code>) directly inside Streamlit. No external server is needed — predictions work for anyone who opens the link."),
        ("What is the Andersen Behavioural Model?",
         "Three factor groups: <b>Enabling</b> (distance, wealth, insurance — 73% of model weight), <b>Predisposing</b> (age, gender, education — 25%), <b>Need</b> (provider type — 2%). Weights from TreeSHAP analysis of the trained model."),
        ("Why was XGBoost selected?",
         "Highest tuned ROC-AUC (0.8144) and F1-score (0.8091) on the held-out test set. Generalisation gap 0.013. Ensemble (Top 3) added only 0.0001 AUC at much higher complexity."),
        ("What does SHAP mean?",
         "<b>SHAP (SHapley Additive exPlanations)</b> explains why the model made each prediction. TreeSHAP shows distance contributes 41% of model decisions — more than all socioeconomic variables combined."),
        ("How do I run this locally?",
         "<code>python -m streamlit run dashboard.py</code> — see Appendix A of the thesis for the full command reference."),
        ("Can I update the dashboard after deployment?",
         "Yes. Push changes to GitHub and Streamlit Cloud deploys automatically within 2 minutes."),
    ]
    for q, a in faqs:
        with st.expander(f"❓  {q}"):
            st.markdown(f"<div style='font-size:13px;color:{muted};line-height:1.9;padding:4px 0;'>{a}</div>",
                        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""<div class='med-card-blue'>
      <b style='color:#1D4ED8;'>Research Reference</b><br>
      <span style='font-size:12px;color:{muted};line-height:2.2;'>
        <b>Title:</b> HealthLink Kenya: A Predictive Framework for Healthcare Access and Referral Planning<br>
        <b>Author:</b> Rutendo Julia Kandeya (ID: 168332)<br>
        <b>Institution:</b> Strathmore University · MSc Data Science &amp; Analytics · 2026<br>
        <b>Supervisor:</b> Dr. Esther Khakata<br>
        <b>Dataset:</b> KNBS Health-Seeking Behaviour Survey 2022 · n = 99,031
      </span>
    </div>""", unsafe_allow_html=True)


def page_settings():
    st.markdown("## Settings")
    st.caption("Personalise your HealthLink Kenya experience")

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("#### Appearance")
        new_theme = st.radio("Colour Theme", ["light","dark"],
                             index=0 if st.session_state.theme == "light" else 1, horizontal=True)
        accent_opts = {
            "Navy Blue (#0B3D6E)": "#0B3D6E",
            "Teal (#0891B2)":      "#0891B2",
            "Forest Green (#065F46)": "#065F46",
            "Deep Purple (#5B21B6)": "#5B21B6",
            "Crimson (#B91C1C)":   "#B91C1C",
        }
        new_accent_lbl = st.selectbox("Accent Colour", options=list(accent_opts.keys()),
                                      index=list(accent_opts.values()).index(
                                          st.session_state.accent) if st.session_state.accent in accent_opts.values() else 0)
        new_font = st.radio("Font Size", ["Small","Medium","Large"],
                            index=["Small","Medium","Large"].index(st.session_state.font_size), horizontal=True)
        if st.button("Apply Appearance", use_container_width=True):
            st.session_state.theme  = new_theme
            st.session_state.accent = accent_opts[new_accent_lbl]
            st.session_state.font_size = new_font
            st.success("Appearance updated.")
            st.rerun()

    with s2:
        st.markdown("#### Map Settings")
        map_opts = ["CartoDB Voyager", "CartoDB positron", "CartoDB dark_matter", "OpenStreetMap"]
        new_map  = st.selectbox("Map Tile Style", map_opts,
                                index=map_opts.index(st.session_state.map_style)
                                if st.session_state.map_style in map_opts else 0)
        new_para = st.checkbox("Highlight Urban Proximity Paradox facilities in red",
                               value=st.session_state.show_paradox)
        if st.button("Save Map Settings", use_container_width=True):
            st.session_state.map_style   = new_map
            st.session_state.show_paradox = new_para
            st.success("Map settings saved.")
            st.rerun()

    st.markdown("---")
    st.markdown("#### Account Information")
    ac1, ac2, ac3 = st.columns(3)
    ac1.metric("Logged in as", user.get("name","—"))
    ac2.metric("Role",         user.get("role","—"))
    ac3.metric("Session",      datetime.now().strftime("%d %b %Y · %H:%M"))

    st.markdown(f"""<div class='med-card-blue' style='margin-top:12px;'>
      <b style='color:#1D4ED8;'>HealthLink Kenya v4.0</b><br>
      <span style='font-size:12px;color:{muted};'>
        MSc Data Science &amp; Analytics · Strathmore University · 2026<br>
        Access Model: XGBoost (Tuned) F1 0.8091 · AUC 0.8144<br>
        Retention Model: XGBoost Stage 2 (SMOTE) · AUC 0.8292 · Dropout recall 53.4%<br>
        Data: KNBS Health-Seeking Behaviour Survey 2022 · n = 99,031
      </span>
    </div>""", unsafe_allow_html=True)


# ── MULTIPAGE NAVIGATION ───────────────────────────────────────────
pg = st.navigation([
    st.Page(page_overview,   title="Overview & Insights",       icon="📊", default=True),
    st.Page(page_triage,     title="Triage & Facility Map",     icon="🏥"),
    st.Page(page_geospatial, title="Geospatial Mapper",         icon="🗺️"),
    st.Page(page_retention,  title="Patient Retention Record",  icon="👤"),
    st.Page(page_gam,        title="Distance Decay (GAM)",      icon="📍"),
    st.Page(page_analytics,  title="Analytics & Visuals",       icon="📈"),
    st.Page(page_faq,        title="FAQ & How It Works",        icon="❓"),
    st.Page(page_settings,   title="Settings",                  icon="⚙️"),
])
pg.run()
