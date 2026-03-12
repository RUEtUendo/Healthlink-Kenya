import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import hashlib

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="HealthLink Kenya",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THEME: Clean white medical aesthetic
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Base - clean white */
    .stApp { background-color: #F7F9FC; color: #1A2B40; }
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E8EDF3;
        box-shadow: 2px 0 8px rgba(0,0,0,0.04);
    }

    /* Headings */
    h1 { color: #0B3D6E !important; font-weight: 800 !important; }
    h2 { color: #0B3D6E !important; font-weight: 700 !important; }
    h3, h4 { color: #1A2B40 !important; font-weight: 600 !important; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E2EAF4;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 4px rgba(11,61,110,0.06);
    }
    [data-testid="metric-container"] label {
        color: #6B84A0 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0B3D6E !important;
        font-size: 26px !important;
        font-weight: 800 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #00A878 !important;
    }

    /* Primary button */
    .stButton > button {
        background: #0B3D6E !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 28px !important;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: #0D4F8C !important;
        box-shadow: 0 4px 12px rgba(11,61,110,0.25) !important;
    }

    /* Input labels */
    .stSelectbox label, .stSlider label, .stRadio label,
    .stTextArea label, .stSelectSlider label, .stTextInput label,
    .stNumberInput label {
        color: #4A6278 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Input fields */
    .stTextInput input, .stSelectbox > div > div,
    .stTextArea textarea {
        background: #FFFFFF !important;
        border: 1px solid #D4DEE9 !important;
        border-radius: 8px !important;
        color: #1A2B40 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0B3D6E !important;
        box-shadow: 0 0 0 3px rgba(11,61,110,0.08) !important;
    }

    /* Dataframe */
    .dataframe { background: #FFFFFF !important; color: #1A2B40 !important; }
    [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

    /* Info / warning / success boxes */
    .stAlert { border-radius: 10px; }

    /* Progress bar */
    .stProgress > div > div { background-color: #0B3D6E !important; }

    /* Divider */
    hr { border-color: #E2EAF4; margin: 16px 0; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background: #F0F4FA; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: #6B84A0; border-radius: 7px; font-weight: 500; }
    .stTabs [aria-selected="true"] {
        color: #0B3D6E !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        font-weight: 700;
    }

    /* Sidebar radio */
    .stRadio > div { gap: 2px; }
    .stRadio label { padding: 8px 12px; border-radius: 8px; transition: background 0.15s; }
    .stRadio label:hover { background: #F0F4FA; }

    /* Custom card classes */
    .med-card {
        background: #FFFFFF;
        border: 1px solid #E2EAF4;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 4px rgba(11,61,110,0.05);
        margin-bottom: 12px;
    }
    .med-card-blue {
        background: #EEF5FF;
        border: 1px solid #C2D8F5;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .med-card-green {
        background: #EDFBF5;
        border: 1px solid #A8E6D0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .med-card-amber {
        background: #FFFBEE;
        border: 1px solid #FDDDA0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .med-card-red {
        background: #FFF5F5;
        border: 1px solid #FBCACA;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }

    /* Status badges */
    .badge-green  { background:#DCFCE7; color:#15803D; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }
    .badge-amber  { background:#FEF9C3; color:#A16207; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }
    .badge-red    { background:#FEE2E2; color:#DC2626; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }
    .badge-blue   { background:#DBEAFE; color:#1D4ED8; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }
    .badge-grey   { background:#F1F5F9; color:#64748B; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }

    /* Patient record row */
    .pt-row { display:flex; justify-content:space-between; align-items:center;
              padding:10px 0; border-bottom:1px solid #F0F4FA; font-size:13px; }
    .pt-label { color:#6B84A0; font-weight:500; font-size:12px; text-transform:uppercase; letter-spacing:0.04em; }
    .pt-value { color:#1A2B40; font-weight:600; }

    /* Login card */
    .login-card {
        background: #FFFFFF;
        border: 1px solid #E2EAF4;
        border-radius: 16px;
        padding: 40px 44px;
        box-shadow: 0 4px 24px rgba(11,61,110,0.08);
        max-width: 440px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIMPLE AUTH  (demo — no real DB needed)
# ============================================================
DEMO_USERS = {
    "admin@healthlink.ke":   {"pw": hashlib.sha256("Admin2024!".encode()).hexdigest(),  "role": "Administrator", "name": "Dr. Admin"},
    "doctor@healthlink.ke":  {"pw": hashlib.sha256("Doctor2024!".encode()).hexdigest(), "role": "Clinician",     "name": "Dr. Wanjiku"},
    "nurse@healthlink.ke":   {"pw": hashlib.sha256("Nurse2024!".encode()).hexdigest(),  "role": "Nurse",         "name": "Sr. Auma"},
    "planner@healthlink.ke": {"pw": hashlib.sha256("Plan2024!".encode()).hexdigest(),   "role": "Health Planner","name": "Mr. Omondi"},
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "user" not in st.session_state:
    st.session_state.user = {}

def do_logout():
    st.session_state.authenticated = False
    st.session_state.user = {}

# ============================================================
# LOGIN / SIGNUP SCREEN
# ============================================================
if not st.session_state.authenticated:
    # Centred logo header
    st.markdown("""
    <div style='text-align:center; padding:48px 0 24px 0;'>
        <div style='font-size:52px;'>⚕️</div>
        <div style='font-size:28px; font-weight:800; color:#0B3D6E; margin-top:8px;'>HealthLink Kenya</div>
        <div style='font-size:14px; color:#6B84A0; margin-top:6px; font-weight:500;'>
            Clinical Decision-Support Platform · Hospital Referral System
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.4, 1])
    with col_c:
        mode_tab = st.radio("", ["🔑  Sign In", "📝  Create Account"],
                            horizontal=True, label_visibility="collapsed")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if "Sign In" in mode_tab:
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center; margin-bottom:20px; color:#0B3D6E;'>Sign In to Your Account</h3>", unsafe_allow_html=True)
            email    = st.text_input("Email Address", placeholder="you@healthlink.ke")
            password = st.text_input("Password", type="password", placeholder="Enter password")

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True):
                hashed = hashlib.sha256(password.encode()).hexdigest()
                if email in DEMO_USERS and DEMO_USERS[email]["pw"] == hashed:
                    st.session_state.authenticated = True
                    st.session_state.user = {"email": email, **DEMO_USERS[email]}
                    st.rerun()
                else:
                    st.error("Invalid email or password. Try demo: doctor@healthlink.ke / Doctor2024!")

            st.markdown("""
            <div style='margin-top:16px; padding:12px 14px; background:#F7F9FC; border-radius:8px;
                        font-size:11px; color:#6B84A0; line-height:1.9;'>
                <b style='color:#0B3D6E;'>Demo accounts:</b><br>
                doctor@healthlink.ke · <i>Doctor2024!</i><br>
                nurse@healthlink.ke · <i>Nurse2024!</i><br>
                planner@healthlink.ke · <i>Plan2024!</i>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        else:  # Sign Up
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center; margin-bottom:20px; color:#0B3D6E;'>Create an Account</h3>", unsafe_allow_html=True)
            new_name  = st.text_input("Full Name", placeholder="Dr. Jane Njoroge")
            new_email = st.text_input("Institutional Email", placeholder="you@hospital.ke")
            new_role  = st.selectbox("Role", ["Clinician", "Nurse", "Health Planner", "Administrator", "Research Officer"])
            new_facility = st.text_input("Facility / Organisation", placeholder="Kenyatta National Hospital")
            new_pw    = st.text_input("Password", type="password", placeholder="Create a strong password")
            new_pw2   = st.text_input("Confirm Password", type="password", placeholder="Repeat password")

            if st.button("Create Account", use_container_width=True):
                if not all([new_name, new_email, new_pw]):
                    st.warning("Please fill in all required fields.")
                elif new_pw != new_pw2:
                    st.error("Passwords do not match.")
                elif len(new_pw) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    st.success(f"✅ Account created for {new_name}. Please sign in above.")
            st.markdown("</div>", unsafe_allow_html=True)

    st.stop()  # nothing below renders until authenticated


# ============================================================
# DATA
# ============================================================
FACILITIES_DATA = pd.DataFrame([
    {"Name": "Kenyatta National Hospital",  "Type": "National Referral Hospital",
     "Specialties": "Oncology, Cardiology, Neurology, Trauma, Burns, Transplant",
     "Dist_km": 0,    "Insurance_pct": 91, "Wealth": "Highest", "Access_pct": 94,
     "Retention_pct": 89, "Lat": -1.3006, "Lon": 36.8066, "Paradox": False, "Beds": 1800},

    {"Name": "Pumwani Maternity Hospital",  "Type": "County Hospital",
     "Specialties": "Maternity, Neonatal ICU, Gynaecology",
     "Dist_km": 4.2,  "Insurance_pct": 62, "Wealth": "Middle",  "Access_pct": 81,
     "Retention_pct": 74, "Lat": -1.2841, "Lon": 36.8458, "Paradox": False, "Beds": 320},

    {"Name": "Mathare North HC",            "Type": "Health Centre",
     "Specialties": "General OPD, Maternal Health, Immunisation",
     "Dist_km": 6.8,  "Insurance_pct": 31, "Wealth": "Lowest",  "Access_pct": 48,
     "Retention_pct": 44, "Lat": -1.2611, "Lon": 36.8590, "Paradox": True,  "Beds": 40},

    {"Name": "Mbagathi District Hospital",  "Type": "County Hospital",
     "Specialties": "General Surgery, Infectious Disease, Psychiatry, Paediatrics",
     "Dist_km": 8.1,  "Insurance_pct": 55, "Wealth": "Middle",  "Access_pct": 77,
     "Retention_pct": 71, "Lat": -1.3217, "Lon": 36.7680, "Paradox": False, "Beds": 260},

    {"Name": "Kayole Sub-County Hospital",  "Type": "Sub-County Hospital",
     "Specialties": "Emergency, Maternity, General OPD, Eye Clinic",
     "Dist_km": 12.4, "Insurance_pct": 28, "Wealth": "Second",  "Access_pct": 43,
     "Retention_pct": 38, "Lat": -1.2718, "Lon": 36.9001, "Paradox": True,  "Beds": 120},

    {"Name": "Ruaraka Health Centre",       "Type": "Clinic",
     "Specialties": "General OPD, Family Planning, HIV/ART",
     "Dist_km": 15.0, "Insurance_pct": 44, "Wealth": "Middle",  "Access_pct": 65,
     "Retention_pct": 59, "Lat": -1.2488, "Lon": 36.8756, "Paradox": False, "Beds": 20},

    {"Name": "Dandora Dispensary",          "Type": "Dispensary",
     "Specialties": "Basic Primary Care, Immunisation, Wound Care",
     "Dist_km": 18.3, "Insurance_pct": 19, "Wealth": "Lowest",  "Access_pct": 37,
     "Retention_pct": 30, "Lat": -1.2595, "Lon": 36.9087, "Paradox": True,  "Beds": 10},

    {"Name": "Kangemi Health Centre",       "Type": "Health Centre",
     "Specialties": "General OPD, Maternal Health, TB/DOTS, Dental",
     "Dist_km": 21.1, "Insurance_pct": 33, "Wealth": "Second",  "Access_pct": 55,
     "Retention_pct": 48, "Lat": -1.2724, "Lon": 36.7369, "Paradox": False, "Beds": 35},

    {"Name": "Nairobi West Hospital",       "Type": "Religious / Mission Hospital",
     "Specialties": "Oncology, Orthopaedics, Cardiology, Dialysis, ICU",
     "Dist_km": 9.5,  "Insurance_pct": 74, "Wealth": "Fourth",  "Access_pct": 82,
     "Retention_pct": 76, "Lat": -1.3146, "Lon": 36.8100, "Paradox": False, "Beds": 200},

    {"Name": "Aga Khan University Hospital","Type": "Private Hospital",
     "Specialties": "Neurosurgery, Oncology, Cardiology, Transplant, MRI/CT",
     "Dist_km": 3.1,  "Insurance_pct": 96, "Wealth": "Highest", "Access_pct": 91,
     "Retention_pct": 88, "Lat": -1.2702, "Lon": 36.8074, "Paradox": False, "Beds": 250},

    {"Name": "Limuru Sub-County Hospital",  "Type": "Sub-County Hospital",
     "Specialties": "General Surgery, Maternity, Emergency",
     "Dist_km": 31.7, "Insurance_pct": 47, "Wealth": "Middle",  "Access_pct": 31,
     "Retention_pct": 26, "Lat": -1.1140, "Lon": 36.6480, "Paradox": False, "Beds": 80},

    {"Name": "Thika Level 5 Hospital",      "Type": "County Referral Hospital",
     "Specialties": "Oncology, Dialysis, Orthopaedics, ICU, Cardiology",
     "Dist_km": 44.2, "Insurance_pct": 52, "Wealth": "Fourth",  "Access_pct": 24,
     "Retention_pct": 20, "Lat": -1.0332, "Lon": 37.0693, "Paradox": False, "Beds": 350},

    {"Name": "Meds Chemist Westlands",      "Type": "Pharmacy / Chemist",
     "Specialties": "Pharmaceutical dispensing, OTC medications, Lab services",
     "Dist_km": 5.2,  "Insurance_pct": 55, "Wealth": "Fourth",  "Access_pct": 88,
     "Retention_pct": 72, "Lat": -1.2633, "Lon": 36.8036, "Paradox": False, "Beds": 0},

    {"Name": "St Francis Community Clinic",  "Type": "Religious / Mission Clinic",
     "Specialties": "General OPD, HIV/ART, Nutrition, TB/DOTS",
     "Dist_km": 14.0, "Insurance_pct": 22, "Wealth": "Lowest",  "Access_pct": 58,
     "Retention_pct": 50, "Lat": -1.2800, "Lon": 36.8700, "Paradox": False, "Beds": 15},
])

MODEL_PERF = pd.DataFrame([
    {"Algorithm": "XGBoost (Optimised)", "F1": 0.9034, "AUC": 0.6524, "Accuracy": 0.8240, "Operational": True },
    {"Algorithm": "Gradient Boosting",   "F1": 0.9034, "AUC": 0.6463, "Accuracy": 0.8239, "Operational": False},
    {"Algorithm": "AdaBoost",            "F1": 0.9034, "AUC": 0.6397, "Accuracy": 0.8238, "Operational": False},
    {"Algorithm": "Ensemble (Top 3)",    "F1": 0.9034, "AUC": 0.6510, "Accuracy": 0.8238, "Operational": False},
    {"Algorithm": "Decision Tree",       "F1": 0.7584, "AUC": 0.6445, "Accuracy": 0.6496, "Operational": False},
    {"Algorithm": "Random Forest",       "F1": 0.7509, "AUC": 0.6528, "Accuracy": 0.6422, "Operational": False},
    {"Algorithm": "Logistic Regression", "F1": 0.5152, "AUC": 0.5248, "Accuracy": 0.4281, "Operational": False},
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

GAM_DIST  = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 80, 100]
GAM_PROB  = [0.96, 0.94, 0.91, 0.88, 0.84, 0.76, 0.58, 0.40, 0.27, 0.14, 0.08, 0.04, 0.02]

# Facility type → map icon colour and marker colour
FACILITY_STYLE = {
    "National Referral Hospital":  {"color": "#1D4ED8", "icon": "🏛️"},
    "County Referral Hospital":    {"color": "#2563EB", "icon": "🏥"},
    "County Hospital":             {"color": "#0891B2", "icon": "🏥"},
    "Sub-County Hospital":         {"color": "#0D9488", "icon": "🏨"},
    "Health Centre":               {"color": "#059669", "icon": "🩺"},
    "Clinic":                      {"color": "#65A30D", "icon": "🩺"},
    "Dispensary":                  {"color": "#CA8A04", "icon": "💊"},
    "Pharmacy / Chemist":          {"color": "#9333EA", "icon": "💊"},
    "Religious / Mission Hospital":{"color": "#E11D48", "icon": "⛪"},
    "Religious / Mission Clinic":  {"color": "#F43F5E", "icon": "⛪"},
    "Private Hospital":            {"color": "#7C3AED", "icon": "🏥"},
}

FOLIUM_COLORS = {
    "National Referral Hospital":  "darkblue",
    "County Referral Hospital":    "blue",
    "County Hospital":             "cadetblue",
    "Sub-County Hospital":         "darkgreen",
    "Health Centre":               "green",
    "Clinic":                      "lightgreen",
    "Dispensary":                  "orange",
    "Pharmacy / Chemist":          "purple",
    "Religious / Mission Hospital":"red",
    "Religious / Mission Clinic":  "pink",
    "Private Hospital":            "darkpurple",
}

ALL_SPECIALTIES = sorted(set(
    s.strip()
    for row in FACILITIES_DATA["Specialties"]
    for s in row.split(",")
))

# ============================================================
# SIDEBAR — authenticated
# ============================================================
user = st.session_state.user
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding:20px 0 12px 0;'>
        <div style='font-size:40px;'>⚕️</div>
        <div style='font-size:17px; font-weight:800; color:#0B3D6E; margin-top:6px;'>HealthLink Kenya</div>
        <div style='font-size:11px; color:#6B84A0; margin-top:4px;'>Clinical Decision-Support Platform</div>
    </div>
    <div style='background:#F0F4FA; border-radius:10px; padding:10px 14px; margin-bottom:8px;'>
        <div style='font-size:12px; font-weight:700; color:#0B3D6E;'>👤 {user.get("name","User")}</div>
        <div style='font-size:11px; color:#6B84A0;'>{user.get("role","")}</div>
        <div style='font-size:10px; color:#94A3B8; margin-top:2px;'>{user.get("email","")}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    module = st.radio("Navigate", [
        "📊  Overview & Insights",
        "🏥  Predictive Triage",
        "👤  Patient Retention Record",
        "🗺️  Geospatial Mapper",
        "📍  Distance Decay (GAM)",
        "🧠  SHAP Interpretability",
        "⚙️  Model Performance",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:10px; color:#94A3B8; line-height:2.0;'>
        <b style='color:#6B84A0'>Model:</b> XGBoost · F1 0.9034<br>
        <b style='color:#6B84A0'>AUC:</b> 0.6524 · Acc: 0.8240<br>
        <b style='color:#6B84A0'>Data:</b> KNBS HSB Survey 2022<br>
        <b style='color:#6B84A0'>n =</b> 99,031 observations<br>
        <b style='color:#6B84A0'>Threshold:</b> 25km (GAM)<br>
        <b style='color:#6B84A0'>API:</b> FastAPI · localhost:8000
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚪  Sign Out", use_container_width=True):
        do_logout()
        st.rerun()


# ============================================================
# MODULE 0: OVERVIEW
# ============================================================
if "Overview" in module:
    st.markdown("## 📊 Overview & Insights")
    st.caption("KNBS Health-Seeking Behaviour Survey 2022 · n = 99,031 · XGBoost Operational Model")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Population Access Rate",  "78.4%",  "+3.2% vs prev. quarter")
    k2.metric("Retention Rate",          "71.2%",  "+1.8% vs prev. quarter")
    k3.metric("GAM Critical Threshold",  "25 km",  "Access drops sharply beyond")
    k4.metric("Urban Proximity Paradox", "3,484",  "Patients facing hidden barriers")

    st.markdown("---")
    st.markdown("### Andersen's Behavioural Model — Feature Weight by Category")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
        <div class='med-card-amber'>
            <div style='font-size:12px;font-weight:700;color:#92400E;letter-spacing:.04em;text-transform:uppercase;'>Enabling Factors · 73%</div>
            <div style='font-size:13px;color:#6B84A0;margin-top:10px;line-height:2.2;'>
                Distance to Facility &nbsp;<b style='color:#1A2B40;'>41%</b><br>
                Wealth Index &nbsp;<b style='color:#1A2B40;'>18%</b><br>
                Insurance Status &nbsp;<b style='color:#1A2B40;'>14%</b>
            </div>
            <div style='font-size:10px;color:#B45309;margin-top:10px;font-weight:600;'>Dominant predictors of access</div>
        </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class='med-card-blue'>
            <div style='font-size:12px;font-weight:700;color:#1E3A8A;letter-spacing:.04em;text-transform:uppercase;'>Predisposing Factors · 25%</div>
            <div style='font-size:13px;color:#6B84A0;margin-top:10px;line-height:2.2;'>
                Residence Type &nbsp;<b style='color:#1A2B40;'>9%</b><br>
                Education Level &nbsp;<b style='color:#1A2B40;'>8%</b><br>
                Age Group &nbsp;<b style='color:#1A2B40;'>5%</b> &nbsp; Gender &nbsp;<b style='color:#1A2B40;'>3%</b>
            </div>
            <div style='font-size:10px;color:#1D4ED8;margin-top:10px;font-weight:600;'>Demographic & social attributes</div>
        </div>""", unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class='med-card-green'>
            <div style='font-size:12px;font-weight:700;color:#065F46;letter-spacing:.04em;text-transform:uppercase;'>Need Factors · 2%</div>
            <div style='font-size:13px;color:#6B84A0;margin-top:10px;line-height:2.2;'>
                Provider Group &nbsp;<b style='color:#1A2B40;'>2%</b><br>
                Perceived health need<br>
                Triage classification
            </div>
            <div style='font-size:10px;color:#059669;margin-top:10px;font-weight:600;'>Lowest individual weight</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)
    fac_types      = ["National Referral", "County Hospital", "Sub-County", "Health Centre", "Dispensary/Clinic"]
    access_vals    = [94, 79, 61, 52, 37]
    retention_vals = [89, 71, 53, 44, 30]

    with col_l:
        st.markdown("#### Access Rate by Facility Type")
        fig_a = go.Figure(go.Bar(
            x=access_vals, y=fac_types, orientation="h",
            marker_color=["#0B3D6E" if v >= 50 else "#EF4444" for v in access_vals],
            text=[f"{v}%" for v in access_vals], textposition="outside",
        ))
        fig_a.update_layout(
            paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC",
            font_color="#1A2B40", height=260, margin=dict(l=0, r=40, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="#E2EAF4", range=[0, 110], color="#6B84A0"),
            yaxis=dict(color="#1A2B40"), showlegend=False,
        )
        st.plotly_chart(fig_a, use_container_width=True)

    with col_r:
        st.markdown("#### Access → Retention Gap")
        gap_vals   = [a - r for a, r in zip(access_vals, retention_vals)]
        gap_colors = ["#EF4444" if g > 12 else "#F59E0B" if g > 8 else "#10B981" for g in gap_vals]
        fig_g = go.Figure(go.Bar(
            x=gap_vals, y=fac_types, orientation="h",
            marker_color=gap_colors,
            text=[f"{v}pp" for v in gap_vals], textposition="outside",
        ))
        fig_g.update_layout(
            paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC",
            font_color="#1A2B40", height=260, margin=dict(l=0, r=40, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="#E2EAF4", range=[0, 25],
                       color="#6B84A0", title="Access–Retention gap (pp)"),
            yaxis=dict(color="#1A2B40"), showlegend=False,
        )
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("""
    <div class='med-card-red'>
        <b style='color:#DC2626;'>⚠️ Urban Proximity Paradox Detected</b><br>
        <span style='font-size:12px;color:#6B84A0;'>
        3,484 patients within &lt;50km failed to access care despite favourable distance and wealth profiles.
        These are empirically validated hidden exclusions — caused by indirect costs, wait times, and perceived
        service quality. Flagged facilities: <b style='color:#1A2B40;'>Mathare North HC · Kayole Sub-County · Dandora Dispensary</b>.
        </span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MODULE 1: PREDICTIVE TRIAGE
# ============================================================
elif "Triage" in module:
    st.markdown("## 🏥 Predictive Triage Engine")
    st.caption("Predict individual likelihood of accessing care · Powered by XGBoost via FastAPI")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Demographic Data")
        age_group = st.selectbox("Age Group", ["0-4","5-14","15-24","25-34","35-49","50-64","65+"])
        gender    = st.selectbox("Gender", ["Female", "Male"])
        residence = st.radio("Residence Type", ["Urban", "Rural"], horizontal=True)

    with col2:
        st.markdown("#### Enabling Factors")
        wealth_index = st.select_slider(
            "Wealth Index (Socioeconomic Quintile)",
            options=["Poorest", "Poorer", "Middle", "Richer", "Richest"]
        )
        insurance   = st.radio("Insurance Status", ["Insured", "Uninsured"], horizontal=True)
        distance_km = st.slider("Distance to Nearest Facility (km)", 0.0, 100.0, 5.0, 0.5)

    if distance_km > 25:
        st.markdown("""
        <div class='med-card-red' style='margin-top:8px;'>
            <b style='color:#DC2626;'>📍 Beyond GAM Threshold (25km)</b> —
            <span style='font-size:12px;color:#6B84A0;'>Access probability drops sharply.
            Consider mobile clinic deployment or ambulance dispatch.</span>
        </div>""", unsafe_allow_html=True)
    elif distance_km > 15:
        st.markdown("""
        <div class='med-card-amber' style='margin-top:8px;'>
            <span style='font-size:12px;color:#92400E;'>⚡ Approaching critical zone (15–25km).
            Monitor access rates for this catchment.</span>
        </div>""", unsafe_allow_html=True)

    clinical_notes = st.text_area(
        "Clinical Notes (Optional NLP Input)",
        value="Patient reports fever and difficulty travelling to facility.",
        height=80
    )

    if st.button("Run Access Prediction"):
        payload = {
            "distance_km": distance_km, "age_group": age_group, "gender": gender,
            "wealth_index": wealth_index,
            "insurance_status": 1 if insurance == "Insured" else 0,
            "residential_area_group": residence,
            "survey_weight": 1.0, "clinical_notes": clinical_notes
        }
        try:
            with st.spinner("Connecting to FastAPI inference engine..."):
                response = requests.post("http://127.0.0.1:8000/predict_access", json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                prob   = result["probability"]
                st.markdown("---")
                st.markdown("#### Model Output")
                m1, m2, m3 = st.columns(3)
                m1.metric("Access Probability", f"{prob}%")
                m2.metric("Prediction", "Will Access" if result["prediction"] == 1 else "Will NOT Access")
                m3.metric("Distance Flag", ">25km ⚠️" if distance_km > 25 else "Within Threshold ✅")
                st.progress(prob / 100)
                if prob >= 70:
                    st.markdown('<div class="med-card-green"><b style="color:#065F46;">✅ High likelihood of access.</b> <span style="font-size:12px;color:#6B84A0;">Patient profile is within normal utilisation range.</span></div>', unsafe_allow_html=True)
                elif prob >= 40:
                    st.markdown('<div class="med-card-amber"><b style="color:#92400E;">⚡ Moderate likelihood.</b> <span style="font-size:12px;color:#6B84A0;">Enabling factors limiting access. Consider outreach support.</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="med-card-red"><b style="color:#DC2626;">🚨 Low likelihood.</b> <span style="font-size:12px;color:#6B84A0;">Patient at high risk of exclusion. Prioritise for mobile clinic or CHW intervention.</span></div>', unsafe_allow_html=True)
                if clinical_notes and result.get("nlp_analysis", {}).get("cleaned_keywords"):
                    st.info(f"**NLP Keywords:** {result['nlp_analysis']['cleaned_keywords']}")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("🚨 Cannot connect to FastAPI. Run: `uvicorn main:app --reload` in a separate terminal.")
        except requests.exceptions.Timeout:
            st.error("Request timed out.")


# ============================================================
# MODULE 2: PATIENT RETENTION RECORD  (new — dedicated page)
# ============================================================
elif "Retention" in module:
    st.markdown("## 👤 Patient Retention Record")
    st.caption("Existing patient follow-up · Visit history · Treatment continuity · Care plan status")

    # Patient lookup
    col_s, col_btn = st.columns([3, 1])
    with col_s:
        pt_id = st.text_input("Search by Patient ID or National ID", placeholder="e.g.  PT-2024-00142  or  12345678")
    with col_btn:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        search = st.button("Load Patient Record", use_container_width=True)

    st.markdown("---")

    # ── DEMO PATIENT RECORD (shown when search is triggered or always for demo)
    DEMO_PATIENT = {
        "id":           "PT-2024-00142",
        "name":         "Amina Wanjiru Kariuki",
        "dob":          "14 March 1987",
        "age":          37,
        "gender":       "Female",
        "national_id":  "23456781",
        "nhif_no":      "NHIF-KE-882341",
        "insurance":    "NHIF (Active)",
        "facility":     "Mbagathi District Hospital",
        "clinician":    "Dr. P. Ochieng",
        "blood_group":  "O+",
        "allergies":    "Penicillin, Sulfonamides",
        "phone":        "+254 712 345 678",
        "county":       "Nairobi",
        "distance_km":  8.1,
        "wealth":       "Middle",
        "residence":    "Urban",
        "access_prob":  77,
        "retention_prob": 71,
        "retention_status": "Active",
        "next_appointment": "28 March 2026",
        "last_visit":   "12 February 2026",
        "visits_ytd":   4,
        "total_visits": 17,
        "conditions":   ["Hypertension", "Type 2 Diabetes"],
        "medications":  [
            {"Drug": "Amlodipine 5mg",    "Dose": "1 tab OD",  "Refill Due": "28 Mar 2026", "Status": "Active"},
            {"Drug": "Metformin 500mg",   "Dose": "1 tab BD",  "Refill Due": "28 Mar 2026", "Status": "Active"},
            {"Drug": "Atorvastatin 20mg", "Dose": "1 tab ON",  "Refill Due": "28 Mar 2026", "Status": "Active"},
        ],
        "visits": [
            {"Date": "12 Feb 2026", "Facility": "Mbagathi District Hospital", "Type": "Chronic Disease Review",  "Clinician": "Dr. P. Ochieng",   "BP": "138/88", "Sugar": "7.4 mmol/L", "Notes": "Well-controlled. Refill issued."},
            {"Date": "10 Jan 2026", "Facility": "Mbagathi District Hospital", "Type": "Routine OPD",            "Clinician": "Dr. P. Ochieng",   "BP": "142/92", "Sugar": "8.1 mmol/L", "Notes": "Dose of Metformin increased."},
            {"Date": "05 Nov 2025", "Facility": "Mbagathi District Hospital", "Type": "Emergency (Hypertensive)","Clinician": "Dr. R. Njoroge",   "BP": "178/104","Sugar": "9.2 mmol/L", "Notes": "IV antihypertensive. Admitted overnight."},
            {"Date": "22 Sep 2025", "Facility": "Ruaraka Health Centre",      "Type": "Chronic Disease Review",  "Clinician": "Sr. M. Auma",      "BP": "136/86", "Sugar": "7.0 mmol/L", "Notes": "Stable. Routine refill."},
        ],
        "investigations": [
            {"Test": "HbA1c",          "Date": "12 Feb 2026", "Result": "7.8%",          "Normal Range": "<7.0%",         "Flag": "⚠️ Elevated"},
            {"Test": "Fasting Glucose","Date": "12 Feb 2026", "Result": "7.4 mmol/L",    "Normal Range": "3.9–5.5 mmol/L","Flag": "⚠️ Elevated"},
            {"Test": "Lipid Panel",    "Date": "10 Jan 2026", "Result": "LDL 3.2 mmol/L","Normal Range": "<2.6 mmol/L",   "Flag": "⚠️ Borderline"},
            {"Test": "BP",             "Date": "12 Feb 2026", "Result": "138/88 mmHg",   "Normal Range": "<130/80 mmHg",  "Flag": "⚠️ Elevated"},
            {"Test": "Renal Function", "Date": "10 Jan 2026", "Result": "Creatinine 82", "Normal Range": "62–106 µmol/L", "Flag": "✅ Normal"},
        ],
        "referrals": [
            {"Date": "12 Feb 2026", "Referred To": "Kenyatta National Hospital — Cardiology", "Reason": "Uncontrolled hypertension, cardiac risk assessment", "Status": "Pending"},
        ],
    }

    pt = DEMO_PATIENT

    # ── PATIENT HEADER CARD
    st.markdown(f"""
    <div class='med-card' style='border-left:4px solid #0B3D6E;'>
        <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
            <div>
                <div style='font-size:22px; font-weight:800; color:#0B3D6E;'>{pt["name"]}</div>
                <div style='font-size:12px; color:#6B84A0; margin-top:4px;'>
                    Patient ID: <b style='color:#1A2B40;'>{pt["id"]}</b> &nbsp;·&nbsp;
                    National ID: <b style='color:#1A2B40;'>{pt["national_id"]}</b> &nbsp;·&nbsp;
                    NHIF: <b style='color:#1A2B40;'>{pt["nhif_no"]}</b>
                </div>
                <div style='margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;'>
                    <span class='badge-blue'>{pt["age"]} yrs · {pt["gender"]}</span>
                    <span class='badge-green'>{pt["insurance"]}</span>
                    <span class='badge-blue'>Blood: {pt["blood_group"]}</span>
                    <span class='badge-red'>⚠ Allergies: {pt["allergies"]}</span>
                </div>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:11px; color:#6B84A0;'>Attending Facility</div>
                <div style='font-size:13px; font-weight:700; color:#0B3D6E;'>{pt["facility"]}</div>
                <div style='font-size:11px; color:#6B84A0; margin-top:2px;'>Dr. {pt["clinician"].replace("Dr. ","")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ACCESS & RETENTION PREDICTION ROW
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Access Probability",    f"{pt['access_prob']}%",   "Model: XGBoost")
    a2.metric("Retention Probability", f"{pt['retention_prob']}%", "Retention Model")
    a3.metric("Next Appointment",      pt["next_appointment"])
    a4.metric("Visits (YTD / Total)",  f"{pt['visits_ytd']} / {pt['total_visits']}")

    tab_summary, tab_visits, tab_meds, tab_labs, tab_referrals = st.tabs([
        "📋 Summary", "🗓 Visit History", "💊 Medications", "🔬 Investigations", "🔀 Referrals"
    ])

    # ── TAB 1: SUMMARY
    with tab_summary:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Personal Details")
            rows = [
                ("Date of Birth",  pt["dob"]),
                ("County",         pt["county"]),
                ("Phone",          pt["phone"]),
                ("Residence Type", pt["residence"]),
                ("Wealth Index",   pt["wealth"]),
                ("Distance to Facility", f"{pt['distance_km']} km"),
                ("Last Visit",     pt["last_visit"]),
            ]
            for label, val in rows:
                st.markdown(f"""
                <div class='pt-row'>
                    <span class='pt-label'>{label}</span>
                    <span class='pt-value'>{val}</span>
                </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("#### Active Conditions")
            for cond in pt["conditions"]:
                st.markdown(f"""
                <div style='background:#EEF5FF; border:1px solid #BFDBFE; border-radius:8px;
                            padding:10px 14px; margin-bottom:8px;'>
                    <span style='font-size:13px; font-weight:600; color:#1D4ED8;'>🩺 {cond}</span>
                </div>""", unsafe_allow_html=True)

            # GAM distance zone indicator
            dist = pt["distance_km"]
            if dist <= 25:
                zone_color, zone_label, zone_bg = "#065F46","✅ Safe Zone (≤25km)","#EDFBF5"
            elif dist <= 50:
                zone_color, zone_label, zone_bg = "#92400E","⚠️ Transition Zone","#FFFBEE"
            else:
                zone_color, zone_label, zone_bg = "#DC2626","🚨 Exclusion Zone","#FFF5F5"

            st.markdown(f"""
            <div style='background:{zone_bg}; border-radius:10px; padding:14px 16px; margin-top:12px;'>
                <div style='font-size:11px; color:#6B84A0; text-transform:uppercase; letter-spacing:.04em;
                            font-weight:600;'>GAM Distance Classification</div>
                <div style='font-size:16px; font-weight:800; color:{zone_color}; margin-top:4px;'>
                    {zone_label}
                </div>
                <div style='font-size:12px; color:#6B84A0; margin-top:2px;'>
                    {dist} km from registered facility
                </div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 2: VISIT HISTORY
    with tab_visits:
        st.markdown("#### Visit History")
        for v in pt["visits"]:
            flag = "🚨" if "Emergency" in v["Type"] else "📋"
            st.markdown(f"""
            <div class='med-card' style='border-left:3px solid #0B3D6E; margin-bottom:10px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <span style='font-size:13px; font-weight:700; color:#0B3D6E;'>{flag} {v["Type"]}</span>
                        <span style='font-size:11px; color:#6B84A0; margin-left:10px;'>{v["Date"]} · {v["Facility"]}</span>
                    </div>
                    <span class='badge-grey'>{v["Clinician"]}</span>
                </div>
                <div style='margin-top:8px; font-size:12px; color:#6B84A0; display:flex; gap:24px;'>
                    <span>BP: <b style='color:#1A2B40;'>{v["BP"]}</b></span>
                    <span>BGL: <b style='color:#1A2B40;'>{v["Sugar"]}</b></span>
                </div>
                <div style='margin-top:6px; font-size:12px; color:#4A6278;'>{v["Notes"]}</div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 3: MEDICATIONS
    with tab_meds:
        st.markdown("#### Current Medications")
        for med in pt["medications"]:
            st.markdown(f"""
            <div class='med-card' style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <div style='font-size:14px; font-weight:700; color:#0B3D6E;'>💊 {med["Drug"]}</div>
                    <div style='font-size:12px; color:#6B84A0; margin-top:3px;'>Dose: <b style='color:#1A2B40;'>{med["Dose"]}</b></div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:11px; color:#6B84A0;'>Refill Due</div>
                    <div style='font-size:13px; font-weight:700; color:#0B3D6E;'>{med["Refill Due"]}</div>
                    <span class='badge-green' style='margin-top:4px; display:inline-block;'>{med["Status"]}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 4: INVESTIGATIONS
    with tab_labs:
        st.markdown("#### Recent Investigations")
        inv_df = pd.DataFrame(pt["investigations"])
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

    # ── TAB 5: REFERRALS
    with tab_referrals:
        st.markdown("#### Referral History")
        for ref in pt["referrals"]:
            st.markdown(f"""
            <div class='med-card-blue'>
                <div style='font-size:13px; font-weight:700; color:#1D4ED8;'>🔀 {ref["Referred To"]}</div>
                <div style='font-size:12px; color:#6B84A0; margin-top:4px;'>
                    Date: <b style='color:#1A2B40;'>{ref["Date"]}</b> &nbsp;·&nbsp; Status:
                    <span class='badge-amber'>{ref["Status"]}</span>
                </div>
                <div style='font-size:12px; color:#4A6278; margin-top:6px;'>Reason: {ref["Reason"]}</div>
            </div>""", unsafe_allow_html=True)


# ============================================================
# MODULE 3: GEOSPATIAL MAPPER
# ============================================================
elif "Mapper" in module:
    st.markdown("## 🗺️ Geospatial Facility Mapper")
    st.caption("Interactive facility map · Facility type legend · Specialised treatment filter · Nairobi County")

    # ── Filters row
    fc1, fc2, fc3 = st.columns([2, 2, 1])
    with fc1:
        selected_types = st.multiselect(
            "Filter by Facility Type",
            options=sorted(FACILITIES_DATA["Type"].unique()),
            default=list(FACILITIES_DATA["Type"].unique()),
        )
    with fc2:
        selected_spec = st.multiselect(
            "Filter by Specialised Treatment",
            options=ALL_SPECIALTIES,
            placeholder="All specialties shown"
        )
    with fc3:
        max_dist = st.slider("Max distance (km)", 1, 60, 50)
        show_ring = st.checkbox("25km GAM ring", value=True)

    # Apply filters
    filtered = FACILITIES_DATA[
        (FACILITIES_DATA["Dist_km"] <= max_dist) &
        (FACILITIES_DATA["Type"].isin(selected_types))
    ].copy()

    if selected_spec:
        def has_spec(row_specs):
            return any(s in row_specs for s in selected_spec)
        filtered = filtered[filtered["Specialties"].apply(has_spec)]

    # Stats row
    si1, si2, si3, si4 = st.columns(4)
    si1.metric("Facilities in range",    len(filtered))
    si2.metric("Avg Access Rate",        f"{filtered['Access_pct'].mean():.1f}%" if len(filtered) else "—")
    si3.metric("Paradox Facilities",     int(filtered["Paradox"].sum()))
    si4.metric("Facility Types Shown",   len(filtered["Type"].unique()))

    # ── Build Folium map (white tiles for medical aesthetic)
    m = folium.Map(location=[-1.2921, 36.8219], zoom_start=11, tiles="CartoDB positron")

    if show_ring:
        folium.Circle(
            location=[-1.3006, 36.8066], radius=25000,
            color="#1D4ED8", weight=2, fill=True,
            fill_color="#1D4ED8", fill_opacity=0.04,
            tooltip="25km GAM Critical Threshold"
        ).add_to(m)

    for _, row in filtered.iterrows():
        f_color = FOLIUM_COLORS.get(row["Type"], "gray")
        if row["Paradox"]:
            f_color = "red"

        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            tooltip=f"{row['Name']} · {row['Type']}",
            popup=folium.Popup(
                f"""<div style='font-family:sans-serif; font-size:12px; min-width:200px;'>
                <b style='color:#0B3D6E; font-size:13px;'>{row['Name']}</b><br>
                <span style='color:#6B84A0;'>{row['Type']}</span><br><br>
                <b>Specialties:</b> {row['Specialties']}<br><br>
                <table style='width:100%; font-size:11px;'>
                  <tr><td style='color:#6B84A0;'>Distance:</td><td><b>{row['Dist_km']} km</b></td></tr>
                  <tr><td style='color:#6B84A0;'>Access Rate:</td><td><b>{row['Access_pct']}%</b></td></tr>
                  <tr><td style='color:#6B84A0;'>Retention Rate:</td><td><b>{row['Retention_pct']}%</b></td></tr>
                  <tr><td style='color:#6B84A0;'>Insurance:</td><td><b>{row['Insurance_pct']}%</b></td></tr>
                  {'<tr><td colspan=2 style="color:red; font-weight:bold;">⚠ Urban Proximity Paradox</td></tr>' if row['Paradox'] else ''}
                </table>
                </div>""",
                max_width=260
            ),
            icon=folium.Icon(color=f_color, icon="plus-sign", prefix="glyphicon")
        ).add_to(m)

    st_folium(m, width="100%", height=500)

    # ── LEGEND
    st.markdown("#### Map Legend — Facility Types")
    legend_cols = st.columns(4)
    for i, (ftype, style) in enumerate(FACILITY_STYLE.items()):
        col_idx = i % 4
        legend_cols[col_idx].markdown(
            f"<div style='display:flex; align-items:center; gap:8px; margin-bottom:6px;'>"
            f"<div style='width:12px; height:12px; border-radius:50%; background:{style['color']}; flex-shrink:0;'></div>"
            f"<span style='font-size:11px; color:#4A6278;'>{ftype}</span></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("#### Facility Details")
    display_df = filtered[["Name","Type","Specialties","Dist_km","Access_pct","Retention_pct","Insurance_pct","Paradox"]].copy()
    display_df.columns = ["Facility","Type","Specialties","Dist (km)","Access %","Retention %","Insurance %","⚠ Paradox"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)


# ============================================================
# MODULE 4: DISTANCE DECAY (GAM)
# ============================================================
elif "Decay" in module:
    st.markdown("## 📍 Distance Decay — GAM Analysis")
    st.caption("Generalised Additive Model spline · Critical inflection at 25km · KNBS 2022")

    fig = go.Figure()
    safe_dist = [d for d in GAM_DIST if d <= 25]
    safe_prob = [p for d, p in zip(GAM_DIST, GAM_PROB) if d <= 25]
    danger_dist = [d for d in GAM_DIST if d >= 25]
    danger_prob = [p for d, p in zip(GAM_DIST, GAM_PROB) if d >= 25]

    fig.add_trace(go.Scatter(x=safe_dist + [25], y=safe_prob + [0.76],
        fill="tozeroy", fillcolor="rgba(16,185,129,0.08)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False))
    fig.add_trace(go.Scatter(x=danger_dist, y=danger_prob,
        fill="tozeroy", fillcolor="rgba(239,68,68,0.06)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False))
    fig.add_trace(go.Scatter(x=GAM_DIST, y=GAM_PROB,
        mode="lines+markers", line=dict(color="#0B3D6E", width=3),
        marker=dict(size=6, color="#0B3D6E"),
        name="P(Access | Distance)", hovertemplate="Distance: %{x}km<br>Access Prob: %{y:.0%}"))
    fig.add_vline(x=25, line_dash="dash", line_color="#F59E0B", line_width=2,
                  annotation_text="25km Inflection (GAM)", annotation_font_color="#F59E0B",
                  annotation_position="top right")
    fig.add_trace(go.Scatter(x=[25], y=[0.76], mode="markers",
        marker=dict(size=12, color="#F59E0B", symbol="circle"),
        name="Critical Inflection", hovertemplate="25km → 76% access probability"))
    fig.update_layout(
        paper_bgcolor="#F7F9FC", plot_bgcolor="#FFFFFF",
        font_color="#1A2B40", height=400,
        xaxis=dict(title="Distance to Nearest Facility (km)", color="#6B84A0",
                   gridcolor="#E2EAF4", linecolor="#E2EAF4"),
        yaxis=dict(title="Probability of Accessing Care", tickformat=".0%",
                   color="#6B84A0", gridcolor="#E2EAF4"),
        legend=dict(bgcolor="#F7F9FC", bordercolor="#E2EAF4"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class='med-card-green'>
            <b style='color:#065F46;'>0–25km · Safe Zone</b><br>
            <span style='font-size:11px;color:#6B84A0;'>Access probability 76–96%.
            Facility placement and ambulance dispatch are effective within this radius.</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='med-card-amber'>
            <b style='color:#92400E;'>25km · Critical Inflection</b><br>
            <span style='font-size:11px;color:#6B84A0;'>GAM-derived empirical threshold.
            Traditional 5km buffer is too conservative. Evidence base for mobile clinic radius.</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='med-card-red'>
            <b style='color:#DC2626;'>&gt;25km · Danger Zone</b><br>
            <span style='font-size:11px;color:#6B84A0;'>Access drops precipitously.
            Priority zone for mobile health unit deployment and transport subsidies.</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class='med-card-blue'>
        <b style='color:#1D4ED8;'>Policy Implication (Ministry of Health)</b><br>
        <span style='font-size:12px;color:#6B84A0;'>
        The 25km catchment standard should supplement the linear 5km buffer currently used
        in epidemiological planning. Mobile clinic deployment and ambulance dispatch radius
        should be recalibrated to this empirically derived GAM threshold.
        </span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# MODULE 5: SHAP INTERPRETABILITY
# ============================================================
elif "SHAP" in module:
    st.markdown("## 🧠 SHAP Feature Importance")
    st.caption("TreeSHAP applied to XGBoost · Marginal feature contributions · Andersen Model category breakdown")

    col_chart, col_insight = st.columns([3, 2])
    with col_chart:
        cat_colors = {"Enabling": "#F59E0B", "Predisposing": "#6366F1", "Need": "#10B981"}
        bar_colors = [cat_colors[c] for c in SHAP_DATA["Category"]]
        fig_shap = go.Figure(go.Bar(
            x=SHAP_DATA["Importance"] * 100, y=SHAP_DATA["Feature"],
            orientation="h", marker_color=bar_colors,
            text=[f"{v*100:.0f}%" for v in SHAP_DATA["Importance"]],
            textposition="outside",
            hovertemplate="%{y}<br>Importance: %{x:.1f}%<extra></extra>"
        ))
        fig_shap.update_layout(
            paper_bgcolor="#F7F9FC", plot_bgcolor="#FFFFFF",
            font_color="#1A2B40", height=340,
            xaxis=dict(title="SHAP Importance (%)", color="#6B84A0",
                       gridcolor="#E2EAF4", range=[0, 55]),
            yaxis=dict(color="#1A2B40", autorange="reversed"),
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_shap, use_container_width=True)

        lcols = st.columns(3)
        for i, (cat, col) in enumerate(cat_colors.items()):
            total = SHAP_DATA[SHAP_DATA["Category"] == cat]["Importance"].sum() * 100
            lcols[i].markdown(f"""
            <div style='background:{col}18; border:1px solid {col}40; border-radius:8px;
                        padding:8px 12px; text-align:center;'>
                <div style='font-size:10px; color:{col}; font-weight:700; text-transform:uppercase;'>{cat}</div>
                <div style='font-size:18px; font-weight:800; color:{col};'>{total:.0f}%</div>
                <div style='font-size:10px; color:#6B84A0;'>combined weight</div>
            </div>""", unsafe_allow_html=True)

    with col_insight:
        st.markdown("""
        <div class='med-card-amber' style='margin-bottom:12px;'>
            <b style='color:#92400E;'>🎯 Dominant Signal: Distance</b><br>
            <span style='font-size:11px;color:#6B84A0;'>Distance_km drives 41% of all model decisions —
            more than all socioeconomic and demographic features combined. Validates the 25km GAM threshold.</span>
        </div>
        <div class='med-card-blue' style='margin-bottom:12px;'>
            <b style='color:#1D4ED8;'>💰 Enabling: 73% Combined</b><br>
            <span style='font-size:11px;color:#6B84A0;'>Distance + Wealth + Insurance = 73% of model weight.
            Targeting all three simultaneously is the highest-ROI policy intervention.</span>
        </div>
        <div class='med-card-green'>
            <b style='color:#065F46;'>👤 Predisposing: 25%</b><br>
            <span style='font-size:11px;color:#6B84A0;'>Residence type (urban vs rural) is the strongest
            predisposing signal, interacting with distance. Education and age have smaller contributions.</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# MODULE 6: MODEL PERFORMANCE
# ============================================================
elif "Performance" in module:
    st.markdown("## ⚙️ Algorithm Tournament — Model Performance")
    st.caption("Stratified 3-Fold Cross-Validation · KNBS n=99,031 · scale_pos_weight for class imbalance")

    def style_row(row):
        if row["Algorithm"] == "XGBoost (Optimised)":
            return ["background-color:#EEF5FF; color:#0B3D6E; font-weight:600"] * len(row)
        return ["color:#1A2B40"] * len(row)

    display = MODEL_PERF.drop(columns=["Operational"])
    st.dataframe(display.style.apply(style_row, axis=1),
                 use_container_width=True, hide_index=True)
    st.markdown("---")

    fig_m = go.Figure()
    for col_name, color in [("F1", "#0B3D6E"), ("AUC", "#0891B2"), ("Accuracy", "#6366F1")]:
        fig_m.add_trace(go.Bar(
            name=col_name, x=MODEL_PERF["Algorithm"], y=MODEL_PERF[col_name],
            marker_color=color, opacity=0.85,
        ))
    fig_m.update_layout(
        barmode="group", paper_bgcolor="#F7F9FC", plot_bgcolor="#FFFFFF",
        font_color="#1A2B40", height=350,
        xaxis=dict(color="#6B84A0", gridcolor="#E2EAF4", tickangle=-25),
        yaxis=dict(color="#6B84A0", gridcolor="#E2EAF4", range=[0, 1.05]),
        legend=dict(bgcolor="#F7F9FC", bordercolor="#E2EAF4"),
        margin=dict(l=10, r=10, t=10, b=80),
    )
    st.plotly_chart(fig_m, use_container_width=True)
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='med-card-red'>
            <b style='color:#DC2626;'>⚖️ Class Imbalance & Sensitivity Bias</b><br>
            <span style='font-size:11px;color:#6B84A0;'>The KNBS dataset is heavily skewed — most respondents
            accessed care (Y=1). Without correction the model over-predicts access.
            <b style='color:#1A2B40;'>scale_pos_weight</b> penalises misclassification of the minority class.
            Result: 3,484 False Positives · 5 False Negatives.
            These FPs represent the Urban Proximity Paradox.</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='med-card-green'>
            <b style='color:#065F46;'>✅ Why XGBoost Was Selected</b><br>
            <span style='font-size:11px;color:#6B84A0;'>Highest single-model ROC-AUC (0.6524).
            The Top-3 soft-voting ensemble marginally stabilised variance (AUC 0.6510) without
            material performance gain. Negligible improvement vs added complexity →
            XGBoost selected as the operational model.</span>
        </div>""", unsafe_allow_html=True)
