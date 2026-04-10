"""
HealthLink Kenya — Social Worker Operations Dashboard
Rutendo Julia Kandeya · Strathmore University · 2026
New design: dark navy theme matching HTML operational console
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
import joblib
import requests
import json
import math
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="HealthLink Kenya",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── THEME ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Sora:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0A1929 !important;
    color: #e2e8f0;
}
.stApp { background-color: #0A1929 !important; }
section[data-testid="stSidebar"] {
    background-color: #0C2340 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.7) !important; }
h1,h2,h3 { font-family: 'Sora', sans-serif !important; color: white !important; }
.stButton > button {
    background: linear-gradient(135deg, #1D9E75, #0F6E56) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
div[data-testid="metric-container"] {
    background: #0C2340 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
div[data-testid="metric-container"] label { color: rgba(255,255,255,0.4) !important; font-size:11px !important; text-transform:uppercase; letter-spacing:0.06em; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: white !important; font-family: 'Sora', sans-serif !important; font-size:26px !important; font-weight:700 !important; }
div[data-testid="metric-container"] [data-testid="stMetricDelta"] { color: #5DCAA5 !important; }
.stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: white !important;
    border-radius: 8px !important;
}
.stSlider > div { color: white !important; }
.stRadio > div { color: white !important; }
.stRadio label { color: rgba(255,255,255,0.7) !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.04) !important; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.5) !important; border-radius:7px; }
.stTabs [aria-selected="true"] { color: #5DCAA5 !important; background: rgba(29,158,117,0.15) !important; font-weight:700; }
.stDataFrame { background: #0C2340 !important; }
div[data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }
p, span, div, label { color: rgba(255,255,255,0.8); }
hr { border-color: rgba(255,255,255,0.08) !important; }
.stMarkdown a { color: #5DCAA5 !important; }
.stAlert { background: rgba(29,158,117,0.1) !important; border: 1px solid rgba(29,158,117,0.3) !important; color: white !important; }

/* Custom cards */
.hl-card {
    background: #0C2340;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}
.hl-card-teal {
    background: rgba(29,158,117,0.08);
    border: 1px solid rgba(29,158,117,0.25);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
.hl-card-danger {
    background: rgba(226,75,74,0.08);
    border-left: 4px solid #F87171;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.hl-card-warning {
    background: rgba(245,158,11,0.08);
    border-left: 4px solid #FCD34D;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.risk-high { color: #F87171; font-weight:700; }
.risk-med  { color: #FCD34D; font-weight:700; }
.risk-low  { color: #6EE7B7; font-weight:700; }
.stat-val { font-family:'Sora',sans-serif; font-size:28px; font-weight:700; color:white; }
.stat-label { font-size:11px; color:rgba(255,255,255,0.4); text-transform:uppercase; letter-spacing:0.06em; }
</style>
""", unsafe_allow_html=True)

# ── MODELS ────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    try:
        access  = joblib.load("health_access_pipeline.pkl")
        retain  = joblib.load("retention_pipeline.pkl")
        return access, retain, True
    except Exception as e:
        return None, None, str(e)

access_model, retention_model, models_ok = load_models()

def predict_access(dist, age, gender, wealth, insured, residence):
    if access_model is None: return 72.0
    try:
        df = pd.DataFrame([{
            "distance_from_facility": dist,
            "insurance_status": "Yes" if insured else "No",
            "education_level": "Secondary",
            "age_group": age, "wealth_index1": wealth,
            "resid": residence, "gender": gender,
            "working_status": "Unknown"
        }])
        return round(float(access_model.predict_proba(df)[0][1]) * 100, 1)
    except: return 72.0

def predict_retention(dist, age, gender, wealth, insured, residence):
    if retention_model is None: return 65.0
    try:
        df = pd.DataFrame([{
            "distance_from_facility": dist,
            "insurance_status": "Yes" if insured else "No",
            "education_level": "Secondary",
            "age_group": age, "wealth_index1": wealth,
            "resid": residence, "gender": gender,
            "working_status": "Unknown"
        }])
        return round(float(retention_model.predict_proba(df)[0][1]) * 100, 1)
    except: return 65.0

# ── API HELPERS ───────────────────────────────────────────────
API_BASE = "https://healthlink-kenya-production.up.railway.app"

def get_patients(page=1, risk=None, sub=None, search=None):
    try:
        params = {"page": page, "page_size": 10}
        if risk:   params["risk"] = risk
        if sub:    params["sub_county"] = sub
        if search: params["search"] = search
        r = requests.get(f"{API_BASE}/patients/", params=params, timeout=3)
        if r.status_code == 200: return r.json()
    except: pass
    return None

def get_stats():
    try:
        r = requests.get(f"{API_BASE}/analytics/dashboard/stats", timeout=3)
        if r.status_code == 200: return r.json()
    except: pass
    return {"total": 30, "high_risk": 9, "medium_risk": 11, "coverage_rate": 70.0}

# ── STATIC DATA ───────────────────────────────────────────────
NAKURU_FACILITIES = [
    {"name": "Nakuru PGH",              "lat": -0.2929, "lng": 36.0763, "type": "hospital"},
    {"name": "Naivasha District Hospital","lat": -0.7145,"lng": 36.4335, "type": "hospital"},
    {"name": "Bahati District Hospital", "lat": -0.1703, "lng": 36.1237, "type": "hospital"},
    {"name": "Molo District Hospital",   "lat": -0.2500, "lng": 35.7337, "type": "hospital"},
    {"name": "Gilgil Sub-District Hospital","lat":-0.4987,"lng":36.3225,"type":"hospital"},
    {"name": "Subukia SDH",              "lat": -0.0003, "lng": 36.2283, "type": "hospital"},
    {"name": "Lanet Health Centre",      "lat": -0.2699, "lng": 36.1071, "type": "clinic"},
    {"name": "Njoro Health Centre",      "lat": -0.3355, "lng": 35.9394, "type": "clinic"},
    {"name": "Rongai Health Centre",     "lat": -0.2029, "lng": 35.9612, "type": "clinic"},
    {"name": "Naivasha HC",              "lat": -0.7186, "lng": 36.4371, "type": "clinic"},
    {"name": "Bahati Dispensary",        "lat": -0.1540, "lng": 36.1536, "type": "dispensary"},
    {"name": "Mbaruk Dispensary",        "lat": -0.4996, "lng": 36.3237, "type": "dispensary"},
    {"name": "Subukia Dispensary",       "lat":  0.0003, "lng": 36.2283, "type": "dispensary"},
]

HOUSEHOLDS = [
    {"id":"HH-NK-00234","name":"Rutendo Nyamari","age":34,"cond":"Hypertension","risk":"High","dist":41.2,"ins":"None","sub":"Bahati","lat":-0.154,"lng":36.140},
    {"id":"HH-NK-00891","name":"Joseph Mwangi",  "age":52,"cond":"Diabetes T2", "risk":"High","dist":28.5,"ins":"None","sub":"Njoro","lat":-0.368,"lng":35.970},
    {"id":"HH-NK-01102","name":"Aisha Karimi",   "age":29,"cond":"Maternal Care","risk":"Medium","dist":19.3,"ins":"NHIF","sub":"Rongai","lat":-0.190,"lng":35.980},
    {"id":"HH-NK-00455","name":"Samuel Otieno",  "age":45,"cond":"TB Follow-up","risk":"Medium","dist":36.7,"ins":"None","sub":"Subukia","lat":0.020,"lng":36.220},
    {"id":"HH-NK-00678","name":"Fatuma Hassan",  "age":38,"cond":"HIV Care",    "risk":"Low",  "dist":3.1, "ins":"Partial","sub":"Nakuru Town","lat":-0.303,"lng":36.075},
    {"id":"HH-NK-00312","name":"Grace Wambui",   "age":61,"cond":"Hypertension","risk":"High","dist":52.3,"ins":"None","sub":"Molo","lat":-0.270,"lng":35.760},
    {"id":"HH-NK-00549","name":"Daniel Kimani",  "age":44,"cond":"Diabetes T2", "risk":"Medium","dist":22.1,"ins":"NHIF","sub":"Gilgil","lat":-0.480,"lng":36.300},
    {"id":"HH-NK-00763","name":"Susan Njoki",    "age":33,"cond":"Maternal Care","risk":"Low","dist":7.8,"ins":"NHIF","sub":"Bahati","lat":-0.185,"lng":36.130},
    {"id":"HH-NK-00988","name":"Peter Koech",    "age":58,"cond":"TB Screening","risk":"High","dist":47.0,"ins":"None","sub":"Kuresoi","lat":-0.420,"lng":35.690},
    {"id":"HH-NK-01055","name":"Mary Auma",      "age":27,"cond":"Child Nutrition","risk":"Low","dist":11.2,"ins":"NHIF","sub":"Rongai","lat":-0.150,"lng":36.020},
]

ALERTS = [
    {"id":"HH-NK-00234","name":"Rutendo Nyamari","sub":"Bahati","cond":"Hypertension","type":"critical",
     "msg":"Reported chest pain. Missed follow-up 5 Apr 2026.","ec_name":"James Nyamari","ec_rel":"Spouse","ec_phone":"+254 712 445 678","time":"Today 08:14 AM"},
    {"id":"HH-NK-00312","name":"Grace Wambui","sub":"Molo","cond":"Hypertension","type":"critical",
     "msg":"New registration. Risk score 0.91. Distance 52.3km. No insurance.","ec_name":"Grace Wanjiku","ec_rel":"Mother","ec_phone":"+254 728 990 112","time":"Today 09:32 AM"},
    {"id":"HH-NK-00891","name":"Joseph Mwangi","sub":"Njoro","cond":"Diabetes T2","type":"critical",
     "msg":"Missed 2 consecutive follow-ups. Last contact 15 Feb 2026.","ec_name":"Peter Kamau","ec_rel":"Brother","ec_phone":"+254 700 334 891","time":"Yesterday 04:45 PM"},
    {"id":"HH-NK-00455","name":"Samuel Otieno","sub":"Subukia","cond":"TB Follow-up","type":"warning",
     "msg":"Distance 36.7km exceeds 35km threshold. Utilisation at 38%.","ec_name":"","ec_rel":"","ec_phone":"","time":"2 days ago"},
]

SHAP_DATA = [
    {"feature":"Education Level","importance":73.2,"category":"Predisposing"},
    {"feature":"Distance (km)",  "importance":12.9,"category":"Enabling"},
    {"feature":"Wealth Index",   "importance":8.4, "category":"Enabling"},
    {"feature":"Insurance",      "importance":5.5, "category":"Enabling"},
]

# ── SESSION STATE ─────────────────────────────────────────────
for k,v in [("auth",False),("user",{}),("page","Hub"),("db_page",1),("db_risk",""),("db_sub",""),("db_search","")]:
    if k not in st.session_state: st.session_state[k] = v

# ── LOGIN ─────────────────────────────────────────────────────
USERS = {
    "amara@healthlink.ke":  {"pw":"sw2026","name":"Amara Ochieng","role":"Social Worker","county":"Nakuru"},
    "admin@healthlink.ke":  {"pw":"admin2026","name":"Supervisor Admin","role":"Supervisor","county":"Nakuru"},
    "doctor@healthlink.ke": {"pw":"Doctor2024!","name":"Dr. Wanjiku","role":"Clinician","county":"Nairobi"},
}

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center;padding:48px 0 32px;'>
          <div style='font-size:52px;'>🏥</div>
          <div style='font-family:Sora,sans-serif;font-size:28px;font-weight:700;color:white;margin-top:10px;'>
            Health<span style='color:#1D9E75;'>Link</span> Kenya
          </div>
          <div style='font-size:13px;color:rgba(255,255,255,0.45);margin-top:6px;'>
            Social Worker Operations Console · Nakuru County
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='hl-card'>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;margin-bottom:20px;'><span style='font-size:36px;'>🧑‍💼</span><br><span style='font-family:Sora,sans-serif;font-size:16px;font-weight:700;color:white;'>Social Worker Sign In</span></div>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@healthlink.ke")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            if st.button("Sign In →", use_container_width=True):
                if email in USERS and USERS[email]["pw"] == password:
                    st.session_state.auth = True
                    st.session_state.user = USERS[email]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            st.markdown(f"""
            <div style='margin-top:14px;padding:10px 12px;background:rgba(255,255,255,0.04);border-radius:8px;font-size:11px;color:rgba(255,255,255,0.4);line-height:2.0;'>
              <b style='color:#5DCAA5;'>Demo logins:</b><br>
              amara@healthlink.ke · <i>sw2026</i><br>
              admin@healthlink.ke · <i>admin2026</i>
            </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

user = st.session_state.user

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:20px 0 16px;text-align:center;'>
      <div style='font-size:36px;'>🏥</div>
      <div style='font-family:Sora,sans-serif;font-size:16px;font-weight:700;color:white;margin-top:6px;'>
        Health<span style='color:#5DCAA5;'>Link</span>
      </div>
      <div style='font-size:10px;color:rgba(255,255,255,0.3);margin-top:2px;'>Nakuru County · SW Console</div>
    </div>
    <div style='background:rgba(29,158,117,0.1);border:1px solid rgba(29,158,117,0.2);border-radius:10px;padding:10px 14px;margin-bottom:16px;'>
      <div style='font-size:13px;font-weight:600;color:white;'>👤 {user["name"]}</div>
      <div style='font-size:11px;color:#5DCAA5;'>{user["role"]} · {user["county"]}</div>
    </div>
    """, unsafe_allow_html=True)

    if models_ok is True:
        st.markdown("<div style='background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);border-radius:8px;padding:8px 12px;font-size:11px;color:#6EE7B7;margin-bottom:12px;'>✅ ML Models loaded</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.25);border-radius:8px;padding:8px 12px;font-size:11px;color:#FCD34D;margin-bottom:12px;'>⚠️ Using fallback values</div>", unsafe_allow_html=True)

    st.markdown("---")
    PAGES = [("⊞","Hub"),("🗺️","Geospatial"),("🚐","Mobile Clinic"),("👥","Triage"),("🗄️","Patient DB"),("📊","Reports"),("🔔","Alerts"),("⚙️","Settings")]
    for icon, label in PAGES:
        active = st.session_state.page == label
        bg = "rgba(29,158,117,0.15)" if active else "transparent"
        border = "rgba(29,158,117,0.6)" if active else "transparent"
        color = "#5DCAA5" if active else "rgba(255,255,255,0.5)"
        st.markdown(f"""
        <div onclick="" style='display:flex;align-items:center;gap:10px;padding:10px 16px;
             border-radius:8px;background:{bg};border-left:3px solid {border};
             margin-bottom:2px;cursor:pointer;'>
          <span style='font-size:15px;'>{icon}</span>
          <span style='font-size:13px;font-weight:{"600" if active else "500"};color:{color};'>{label}</span>
        </div>""", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown("---")
    if st.button("← Sign Out", use_container_width=True):
        st.session_state.auth = False
        st.session_state.user = {}
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════
# OUTREACH HUB
# ══════════════════════════════════════════════════════════════
if page == "Hub":
    st.markdown("<h2 style='margin-bottom:4px;'>Outreach Hub</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.4);font-size:13px;margin-bottom:24px;'>Nakuru County — select a module to begin</p>", unsafe_allow_html=True)

    stats = get_stats()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Patients",    stats.get("total",30))
    c2.metric("High Risk",         stats.get("high_risk",9),  delta_color="inverse")
    c3.metric("Medium Risk",       stats.get("medium_risk",11))
    c4.metric("Coverage Rate",     f"{stats.get('coverage_rate',70)}%", "+2pts vs last month")

    st.markdown("---")
    st.markdown("<h3>Quick Access</h3>", unsafe_allow_html=True)

    cols = st.columns(4)
    hub_items = [
        ("🗺️","Geospatial Mapper","Risk zones, facilities & decay","Geospatial"),
        ("👥","Patient Triage",   "View patient profiles & risk","Triage"),
        ("🚐","Mobile Clinic",    "Household IDs on field map","Mobile Clinic"),
        ("🗄️","Patient Database", "All registered patients","Patient DB"),
        ("📊","Reports & SHAP",   "Analytics & model outputs","Reports"),
        ("🔔","Alerts",           "Emergency contacts · Flags","Alerts"),
        ("📍","Distance Decay",   "35km GAM threshold analysis","Reports"),
        ("⚙️","Settings",         "Coverage & thresholds","Settings"),
    ]
    for i, (icon, label, desc, target) in enumerate(hub_items):
        with cols[i % 4]:
            st.markdown(f"""
            <div class='hl-card' style='text-align:center;padding:24px 14px 18px;cursor:pointer;
                 transition:all 0.2s;'>
              <div style='font-size:30px;margin-bottom:10px;'>{icon}</div>
              <div style='font-family:Sora,sans-serif;font-size:13px;font-weight:600;color:white;'>{label}</div>
              <div style='font-size:11px;color:rgba(255,255,255,0.35);margin-top:4px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open {label}", key=f"hub_{label}", use_container_width=True):
                st.session_state.page = target
                st.rerun()

    st.markdown("---")
    st.markdown("<h3>Active Alerts</h3>", unsafe_allow_html=True)
    for a in ALERTS[:2]:
        color = "#F87171" if a["type"]=="critical" else "#FCD34D"
        st.markdown(f"""
        <div class='hl-card-danger'>
          <div style='font-size:14px;font-weight:700;color:white;'>{a["name"]} — {a["id"]}</div>
          <div style='font-size:12px;color:rgba(255,255,255,0.5);margin-top:3px;'>{a["sub"]} · {a["cond"]}</div>
          <div style='font-size:12px;color:rgba(255,255,255,0.7);margin-top:6px;'>{a["msg"]}</div>
          <div style='font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px;'>{a["time"]}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# GEOSPATIAL MAPPER
# ══════════════════════════════════════════════════════════════
elif page == "Geospatial":
    st.markdown("<h2>Geospatial Mapper</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.4);font-size:13px;'>Facility coverage, household IDs & distance decay — Nakuru County</p>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    show_hh   = c1.checkbox("Show Households",  value=True)
    show_risk = c2.checkbox("Show Risk Zones",   value=True)
    decay_km  = c3.slider("Decay threshold (km)", 10, 60, 35)

    m = folium.Map(location=[-0.310, 36.080], zoom_start=9,
                   tiles="CartoDB dark_matter")

    # Facilities
    for f in NAKURU_FACILITIES:
        color = "#1D9E75" if f["type"]=="hospital" else "#185FA5" if f["type"]=="clinic" else "#8B5CF6"
        size  = 9 if f["type"]=="hospital" else 7 if f["type"]=="clinic" else 5
        folium.CircleMarker(
            location=[f["lat"], f["lng"]], radius=size,
            color="white", weight=1.5, fill=True,
            fill_color=color, fill_opacity=0.9,
            tooltip=f['name'],
            popup=folium.Popup(f"<b>{f['name']}</b><br>{f['type'].title()}", max_width=200)
        ).add_to(m)

    # Households
    if show_hh:
        for hh in HOUSEHOLDS:
            risk_color = "#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            folium.CircleMarker(
                location=[hh["lat"], hh["lng"]], radius=8,
                color="white", weight=2, fill=True,
                fill_color=risk_color, fill_opacity=0.9,
                tooltip=f"{hh['id']} · {hh['name']} · {hh['risk']} Risk",
                popup=folium.Popup(f"<b>{hh['id']}</b><br>{hh['name']}<br>{hh['cond']}<br>Distance: {hh['dist']} km<br>Insurance: {hh['ins']}", max_width=220)
            ).add_to(m)

    # Risk zones
    if show_risk:
        risk_zones = [
            {"lat":-0.17,"lng":36.12,"r":8000,"color":"#E24B4A","label":"Bahati High-Risk Zone"},
            {"lat":-0.42,"lng":35.70,"r":12000,"color":"#E24B4A","label":"Kuresoi High-Risk Zone"},
            {"lat":0.04,"lng":36.22,"r":7000,"color":"#F59E0B","label":"Subukia Medium Zone"},
            {"lat":-0.50,"lng":36.33,"r":5000,"color":"#10B981","label":"Gilgil Low-Risk Zone"},
        ]
        for z in risk_zones:
            folium.Circle(
                location=[z["lat"],z["lng"]], radius=z["r"],
                color=z["color"], fill=True, fill_color=z["color"],
                fill_opacity=0.12, weight=1.5,
                tooltip=z["label"]
            ).add_to(m)

    # Decay ring around Nakuru Town
    folium.Circle(
        location=[-0.293, 36.076], radius=decay_km*1000,
        color="#F59E0B", fill=False, weight=2,
        dash_array="8 6",
        tooltip=f"{decay_km}km decay threshold"
    ).add_to(m)

    map_data = st_folium(m, width="100%", height=480, returned_objects=["last_clicked"])

    # Stats row
    s1,s2,s3,s4 = st.columns(4)
    s1.metric("Facilities mapped", len(NAKURU_FACILITIES))
    s2.metric("Households shown",  len(HOUSEHOLDS) if show_hh else 0)
    s3.metric("Decay threshold",   f"{decay_km} km")
    s4.metric("High-risk zones",   "3")

    # Click analysis
    if map_data and map_data.get("last_clicked"):
        clat = map_data["last_clicked"]["lat"]
        clng = map_data["last_clicked"]["lng"]
        def haversine(lat1,lng1,lat2,lng2):
            R=6371; dlat=math.radians(lat2-lat1); dlng=math.radians(lng2-lng1)
            a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
            return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        nearest = sorted(NAKURU_FACILITIES, key=lambda f: haversine(clat,clng,f["lat"],f["lng"]))[:3]
        st.markdown(f"<div class='hl-card-teal'><b style='color:#5DCAA5;'>📍 Click at ({clat:.4f}, {clng:.4f})</b></div>", unsafe_allow_html=True)
        for f in nearest:
            d = haversine(clat,clng,f["lat"],f["lng"])
            col = "#6EE7B7" if d<=decay_km else "#F87171"
            st.markdown(f"<div class='hl-card'><b style='color:white;'>{f['name']}</b> <span style='color:{col};float:right;font-weight:700;'>{d:.1f} km</span><br><span style='color:rgba(255,255,255,0.4);font-size:12px;'>{f['type'].title()}</span></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MOBILE CLINIC ROUTING
# ══════════════════════════════════════════════════════════════
elif page == "Mobile Clinic":
    st.markdown("<h2>Mobile Clinic Routing</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.4);font-size:13px;'>Select a household to locate on map — nearest facilities shown automatically</p>", unsafe_allow_html=True)

    risk_filter = st.radio("Filter by risk", ["All","High","Medium","Low"], horizontal=True)
    filtered_hh = [h for h in HOUSEHOLDS if risk_filter=="All" or h["risk"]==risk_filter]

    col_list, col_map = st.columns([1, 2])

    with col_list:
        st.markdown(f"<div style='font-size:11px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;'>{len(filtered_hh)} Households</div>", unsafe_allow_html=True)
        selected_hh = None
        for hh in filtered_hh:
            rc = "#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            st.markdown(f"""
            <div class='hl-card' style='padding:12px 14px;margin-bottom:6px;cursor:pointer;'>
              <div style='display:flex;align-items:center;gap:10px;'>
                <div style='width:8px;height:8px;border-radius:50%;background:{rc};flex-shrink:0;'></div>
                <div>
                  <div style='font-size:12px;font-weight:700;color:{rc};font-family:monospace;'>{hh["id"]}</div>
                  <div style='font-size:11px;color:rgba(255,255,255,0.5);'>{hh["name"]} · {hh["sub"]}</div>
                  <div style='font-size:10px;color:rgba(255,255,255,0.3);'>{hh["dist"]} km · {hh["cond"]}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Select {hh['id']}", key=f"mc_{hh['id']}", use_container_width=True):
                st.session_state["selected_hh"] = hh

    with col_map:
        selected = st.session_state.get("selected_hh", filtered_hh[0] if filtered_hh else None)
        m2 = folium.Map(location=[selected["lat"], selected["lng"]] if selected else [-0.310, 36.080],
                        zoom_start=11, tiles="CartoDB dark_matter")

        def haversine2(lat1,lng1,lat2,lng2):
            R=6371; dlat=math.radians(lat2-lat1); dlng=math.radians(lng2-lng1)
            a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
            return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

        for f in NAKURU_FACILITIES:
            c = "#1D9E75" if f["type"]=="hospital" else "#185FA5" if f["type"]=="clinic" else "#8B5CF6"
            folium.CircleMarker([f["lat"],f["lng"]], radius=6, color="white", weight=1.5,
                fill=True, fill_color=c, fill_opacity=0.85, tooltip=f["name"]).add_to(m2)

        for hh in filtered_hh:
            rc = "#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            is_sel = selected and hh["id"]==selected["id"]
            folium.CircleMarker([hh["lat"],hh["lng"]], radius=10 if is_sel else 7,
                color="white", weight=3 if is_sel else 1.5,
                fill=True, fill_color=rc, fill_opacity=0.95 if is_sel else 0.8,
                tooltip=f"{hh['id']} · {hh['risk']} Risk").add_to(m2)

        if selected:
            nearest_fac = sorted(NAKURU_FACILITIES, key=lambda f: haversine2(selected["lat"],selected["lng"],f["lat"],f["lng"]))[0]
            folium.PolyLine(
                [[selected["lat"],selected["lng"]],[nearest_fac["lat"],nearest_fac["lng"]]],
                color="#F59E0B", weight=2.5, dash_array="8 5", opacity=0.85
            ).add_to(m2)

        st_folium(m2, width="100%", height=480)

    if selected:
        nearest_facs = sorted(NAKURU_FACILITIES, key=lambda f: haversine2(selected["lat"],selected["lng"],f["lat"],f["lng"]))[:3]
        rc = "#F87171" if selected["risk"]=="High" else "#FCD34D" if selected["risk"]=="Medium" else "#6EE7B7"
        ins_c = "#6EE7B7" if selected["ins"]=="NHIF" else "#FCD34D" if selected["ins"]=="Partial" else "#F87171"
        st.markdown(f"""
        <div class='hl-card' style='margin-top:14px;'>
          <div style='display:flex;justify-content:space-between;align-items:center;'>
            <div>
              <div style='font-family:Sora,sans-serif;font-size:16px;font-weight:700;color:white;'>{selected["id"]}</div>
              <div style='font-size:13px;color:rgba(255,255,255,0.5);margin-top:2px;'>{selected["name"]} · {selected["age"]} yrs · {selected["sub"]}</div>
            </div>
            <div style='text-align:right;'>
              <div style='font-size:14px;font-weight:700;color:{rc};'>{selected["risk"]} Risk</div>
              <div style='font-size:13px;color:{ins_c};font-weight:600;'>{selected["ins"]}</div>
            </div>
          </div>
          <div style='margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.07);'>
            <div style='font-size:10px;font-weight:700;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.07em;margin-bottom:8px;'>3 Nearest Facilities</div>
            <div style='display:flex;gap:8px;'>
              {"".join([f'<div style="flex:1;background:#0F2847;border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:10px;"><div style="font-size:12px;font-weight:600;color:white;">{f["name"]}</div><div style="font-size:11px;color:rgba(255,255,255,0.35);">{haversine2(selected["lat"],selected["lng"],f["lat"],f["lng"]):.1f} km · {f["type"]}</div></div>' for f in nearest_facs])}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PREDICTIVE TRIAGE
# ══════════════════════════════════════════════════════════════
elif page == "Triage":
    st.markdown("<h2>Predictive Triage</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.4);font-size:13px;'>Enter patient profile → live XGBoost prediction → nearest facilities</p>", unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 1])

    with col_form:
        st.markdown("<div class='hl-card'>", unsafe_allow_html=True)
        st.markdown("<b style='color:white;'>Patient Profile</b>", unsafe_allow_html=True)
        age_group = st.selectbox("Age Group", ["0-4","5-14","15-24","25-34","35-49","50-64","65+"])
        gender    = st.selectbox("Gender", ["Female","Male"])
        residence = st.radio("Residence", ["Urban","Rural","Peri-Urban"], horizontal=True)
        wealth    = st.select_slider("Wealth Index", options=["Poorest","Poorer","Middle","Richer","Richest"])
        insurance = st.radio("Insurance", ["Insured","Uninsured"], horizontal=True)
        distance  = st.slider("Distance to Nearest Facility (km)", 0.0, 100.0, 5.0, 0.5)
        notes     = st.text_area("Clinical Notes (optional)", height=60)
        predict_btn = st.button("🔍 Run Prediction", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_result:
        if predict_btn or "last_pred" in st.session_state:
            if predict_btn:
                insured = insurance == "Insured"
                acc  = predict_access(distance, age_group, gender, wealth, insured, residence)
                ret  = predict_retention(distance, age_group, gender, wealth, insured, residence)
                st.session_state.last_pred = {"acc": acc, "ret": ret, "dist": distance}

            pred = st.session_state.last_pred
            acc, ret, dist = pred["acc"], pred["ret"], pred["dist"]

            acc_color = "#6EE7B7" if acc>=70 else "#FCD34D" if acc>=40 else "#F87171"
            ret_color = "#6EE7B7" if ret>=70 else "#FCD34D" if ret>=40 else "#F87171"

            st.markdown(f"""
            <div class='hl-card'>
              <div style='font-family:Sora,sans-serif;font-size:13px;font-weight:700;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:16px;'>Prediction Results</div>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px;'>
                <div style='text-align:center;background:#0F2847;border-radius:10px;padding:20px 10px;'>
                  <div style='font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;margin-bottom:6px;'>Access Probability</div>
                  <div style='font-family:Sora,sans-serif;font-size:36px;font-weight:700;color:{acc_color};'>{acc}%</div>
                </div>
                <div style='text-align:center;background:#0F2847;border-radius:10px;padding:20px 10px;'>
                  <div style='font-size:11px;color:rgba(255,255,255,0.35);text-transform:uppercase;margin-bottom:6px;'>Retention Probability</div>
                  <div style='font-family:Sora,sans-serif;font-size:36px;font-weight:700;color:{ret_color};'>{ret}%</div>
                </div>
              </div>
            """, unsafe_allow_html=True)

            zone = "🟢 Safe Zone (≤35km)" if dist<=35 else "🔴 Beyond Threshold"
            zone_color = "#6EE7B7" if dist<=35 else "#F87171"
            st.markdown(f"<div style='font-size:13px;color:{zone_color};font-weight:600;margin-bottom:12px;'>{zone} · {dist} km</div>", unsafe_allow_html=True)

            if acc >= 70:
                st.markdown("<div class='hl-card-teal'>✅ High likelihood of access — standard outreach schedule.</div>", unsafe_allow_html=True)
            elif acc >= 40:
                st.markdown("<div class='hl-card-warning'>⚡ Moderate — consider transport support or CHW visit.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='hl-card-danger'>🚨 Low likelihood — prioritise mobile clinic or CHW dispatch.</div>", unsafe_allow_html=True)

            # Progress bar
            fig = go.Figure(go.Bar(
                x=[acc, ret], y=["Access", "Retention"],
                orientation="h",
                marker_color=[acc_color, ret_color],
                text=[f"{acc}%", f"{ret}%"], textposition="outside",
                textfont=dict(color="white", size=13)
            ))
            fig.update_layout(
                paper_bgcolor="#0C2340", plot_bgcolor="#0C2340",
                height=150, margin=dict(l=10,r=60,t=10,b=10),
                xaxis=dict(range=[0,115], showgrid=False, tickfont=dict(color="rgba(255,255,255,0.4)")),
                yaxis=dict(tickfont=dict(color="white", size=13)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='hl-card' style='text-align:center;padding:60px 20px;'>
              <div style='font-size:48px;margin-bottom:16px;'>🔍</div>
              <div style='font-size:14px;color:rgba(255,255,255,0.4);'>Fill in the patient profile and click Run Prediction</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PATIENT DATABASE
# ══════════════════════════════════════════════════════════════
elif page == "Patient DB":
    st.markdown("<h2>Patient Database</h2>", unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns([2,1,1,1])
    with sc1: search = st.text_input("🔍 Search name, ID, sub-county...", value=st.session_state.db_search)
    with sc2: risk_f = st.selectbox("Risk Level", ["","High","Medium","Low"], key="risk_sel")
    with sc3: sub_f  = st.selectbox("Sub-county", ["","Nakuru Town","Bahati","Njoro","Rongai","Subukia","Kuresoi","Molo","Gilgil","Naivasha"], key="sub_sel")
    with sc4:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.db_page = 1

    st.session_state.db_search = search
    st.session_state.db_risk   = risk_f
    st.session_state.db_sub    = sub_f

    data = get_patients(
        page=st.session_state.db_page,
        risk=risk_f or None,
        sub=sub_f or None,
        search=search or None
    )

    if data:
        total = data.get("total", 0)
        patients = data.get("data", [])

        # Summary stats
        m1,m2,m3,m4,m5 = st.columns(5)
        m1.metric("Total Records", total)
        highs = sum(1 for p in patients if p.get("risk")=="High")
        meds  = sum(1 for p in patients if p.get("risk")=="Medium")
        lows  = sum(1 for p in patients if p.get("risk")=="Low")
        nhifs = sum(1 for p in patients if p.get("insurance")=="NHIF")
        m2.metric("High Risk",   highs)
        m3.metric("Medium Risk", meds)
        m4.metric("Low Risk",    lows)
        m5.metric("NHIF",        nhifs)

        # Table
        if patients:
            rows = []
            for p in patients:
                rc = "🔴" if p.get("risk")=="High" else "🟡" if p.get("risk")=="Medium" else "🟢"
                ic = "✅" if p.get("insurance")=="NHIF" else "⚠️" if p.get("insurance")=="Partial" else "❌"
                rows.append({
                    "ID": p.get("id",""),
                    "Name": p.get("name",""),
                    "Age": p.get("age",""),
                    "Gender": p.get("gender",""),
                    "Sub-county": p.get("sub_county",""),
                    "Condition": p.get("condition",""),
                    "Risk": f"{rc} {p.get('risk','')}",
                    "Dist (km)": p.get("distance_km",""),
                    "Insurance": f"{ic} {p.get('insurance','')}",
                    "Last Visit": p.get("last_visit") or "N/A",
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True, height=400)

            # Pagination
            total_pages = max(1, math.ceil(total / 10))
            pc1,pc2,pc3 = st.columns([2,2,2])
            with pc1:
                if st.button("← Prev", disabled=st.session_state.db_page<=1):
                    st.session_state.db_page -= 1; st.rerun()
            with pc2:
                st.markdown(f"<div style='text-align:center;color:rgba(255,255,255,0.4);font-size:12px;padding-top:8px;'>Page {st.session_state.db_page} of {total_pages}</div>", unsafe_allow_html=True)
            with pc3:
                if st.button("Next →", disabled=st.session_state.db_page>=total_pages):
                    st.session_state.db_page += 1; st.rerun()

            # Export
            if st.button("⬇️ Export CSV"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "nakuru_patients.csv", "text/csv")
        else:
            st.markdown("<div class='hl-card' style='text-align:center;padding:40px;color:rgba(255,255,255,0.3);'>No patients match current filters</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='hl-card-warning'>
          ⚠️ Could not reach the FastAPI backend. Make sure your server is running:<br><br>
          <code style='background:rgba(0,0,0,0.3);padding:4px 10px;border-radius:4px;'>uvicorn main:app --reload</code>
        </div>""", unsafe_allow_html=True)
        # Show static fallback
        st.markdown("<p style='color:rgba(255,255,255,0.4);font-size:12px;margin-top:12px;'>Showing static data while API is offline:</p>", unsafe_allow_html=True)
        fallback = pd.DataFrame(HOUSEHOLDS)[["id","name","age","cond","risk","dist","ins","sub"]]
        fallback.columns = ["ID","Name","Age","Condition","Risk","Distance","Insurance","Sub-county"]
        st.dataframe(fallback, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# REPORTS & SHAP
# ══════════════════════════════════════════════════════════════
elif page == "Reports":
    st.markdown("<h2>Reports & Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.4);font-size:13px;'>SHAP feature importance · Model performance · Distance decay</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["SHAP Analysis", "Distance Decay", "Model Performance"])

    with tab1:
        st.markdown("<h3>Feature Importance — TreeSHAP</h3>", unsafe_allow_html=True)
        shap_df = pd.DataFrame(SHAP_DATA)
        cat_colors = {"Predisposing":"#6366F1","Enabling":"#F59E0B","Need":"#10B981"}
        bar_colors = [cat_colors[c] for c in shap_df["category"]]

        fig_shap = go.Figure(go.Bar(
            x=shap_df["importance"], y=shap_df["feature"],
            orientation="h", marker_color=bar_colors,
            text=[f"{v}%" for v in shap_df["importance"]],
            textposition="outside",
            textfont=dict(color="white", size=13)
        ))
        fig_shap.update_layout(
            paper_bgcolor="#0C2340", plot_bgcolor="#0C2340",
            height=300, margin=dict(l=10,r=70,t=10,b=10),
            xaxis=dict(range=[0,95], tickfont=dict(color="rgba(255,255,255,0.4)"), gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(tickfont=dict(color="white", size=13), autorange="reversed"),
            showlegend=False
        )
        st.plotly_chart(fig_shap, use_container_width=True)

        c1,c2,c3 = st.columns(3)
        c1.markdown("<div class='hl-card-warning'><b style='color:#F59E0B;'>Enabling: 26.8%</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Distance + Wealth + Insurance</span></div>", unsafe_allow_html=True)
        c2.markdown("<div class='hl-card' style='border-left:3px solid #6366F1;'><b style='color:#A78BFA;'>Predisposing: 73.2%</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Education dominates</span></div>", unsafe_allow_html=True)
        c3.markdown("<div class='hl-card-teal'><b style='color:#5DCAA5;'>Distance: 12.9%</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Strongest individual feature</span></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3>Distance Decay — GAM Analysis</h3>", unsafe_allow_html=True)
        GAM_DIST = [0,5,10,15,20,25,30,35,40,50,60]
        GAM_PROB = [0.899,0.905,0.910,0.914,0.916,0.918,0.910,0.895,0.875,0.840,0.800]

        fig_gam = go.Figure()
        safe_d = [d for d in GAM_DIST if d<=35]; safe_p = [p for d,p in zip(GAM_DIST,GAM_PROB) if d<=35]
        risk_d = [d for d in GAM_DIST if d>=35]; risk_p = [p for d,p in zip(GAM_DIST,GAM_PROB) if d>=35]

        fig_gam.add_trace(go.Scatter(x=safe_d+[35],y=safe_p+[0.895],fill="tozeroy",
            fillcolor="rgba(16,185,129,0.08)",line=dict(color="rgba(0,0,0,0)"),showlegend=False))
        fig_gam.add_trace(go.Scatter(x=risk_d,y=risk_p,fill="tozeroy",
            fillcolor="rgba(239,68,68,0.07)",line=dict(color="rgba(0,0,0,0)"),showlegend=False))
        fig_gam.add_trace(go.Scatter(x=GAM_DIST,y=GAM_PROB,mode="lines+markers",
            line=dict(color="#1D9E75",width=3),marker=dict(size=7,color="#5DCAA5"),
            name="P(Access | Distance)",
            hovertemplate="Distance: %{x} km<br>Access: %{y:.1%}"))
        fig_gam.add_vline(x=35,line_dash="dash",line_color="#F59E0B",line_width=2,
            annotation_text="35 km threshold",annotation_font_color="#F59E0B",
            annotation_position="top right")

        fig_gam.update_layout(
            paper_bgcolor="#0C2340", plot_bgcolor="#0C2340",
            height=380, font_color="white",
            xaxis=dict(title="Distance to Nearest Facility (km)", color="rgba(255,255,255,0.5)",
                       gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="rgba(255,255,255,0.5)")),
            yaxis=dict(title="Access Probability", tickformat=".0%", color="rgba(255,255,255,0.5)",
                       gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="rgba(255,255,255,0.5)")),
            legend=dict(bgcolor="#0C2340", bordercolor="rgba(255,255,255,0.1)"),
            margin=dict(l=20,r=20,t=20,b=20)
        )
        st.plotly_chart(fig_gam, use_container_width=True)

        g1,g2,g3 = st.columns(3)
        g1.markdown("<div class='hl-card-teal'><b style='color:#5DCAA5;'>0–35 km · Stable</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>89.9–91.8% access probability</span></div>", unsafe_allow_html=True)
        g2.markdown("<div class='hl-card-warning'><b style='color:#FCD34D;'>35 km · Inflection</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>GAM threshold — mobile clinic boundary</span></div>", unsafe_allow_html=True)
        g3.markdown("<div class='hl-card-danger'><b style='color:#F87171;'>&gt;35 km · Declining</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Access drops to 84% at 50 km</span></div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<h3>Algorithm Tournament Results</h3>", unsafe_allow_html=True)
        perf_data = pd.DataFrame([
            {"Algorithm":"XGBoost (Deployed ✅)","F1":0.8091,"AUC":0.8144,"Accuracy":0.7222},
            {"Algorithm":"Gradient Boosting",    "F1":0.9342,"AUC":0.5762,"Accuracy":0.8766},
            {"Algorithm":"AdaBoost",             "F1":0.9343,"AUC":0.5501,"Accuracy":0.8766},
            {"Algorithm":"Random Forest",        "F1":0.6573,"AUC":0.5932,"Accuracy":0.5282},
            {"Algorithm":"Logistic Regression",  "F1":0.6611,"AUC":0.6143,"Accuracy":0.5342},
            {"Algorithm":"Decision Tree",        "F1":0.5010,"AUC":0.5641,"Accuracy":0.3963},
        ])

        fig_perf = go.Figure()
        for col, color in [("F1","#1D9E75"),("AUC","#185FA5"),("Accuracy","#6366F1")]:
            fig_perf.add_trace(go.Bar(name=col, x=perf_data["Algorithm"], y=perf_data[col],
                marker_color=color, opacity=0.85))
        fig_perf.update_layout(
            barmode="group", paper_bgcolor="#0C2340", plot_bgcolor="#0C2340",
            height=350, font_color="white",
            xaxis=dict(tickfont=dict(color="white"), tickangle=-25, gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(tickfont=dict(color="rgba(255,255,255,0.5)"), gridcolor="rgba(255,255,255,0.06)", range=[0,1.05]),
            legend=dict(bgcolor="#0C2340", bordercolor="rgba(255,255,255,0.1)"),
            margin=dict(l=10,r=10,t=10,b=100)
        )
        st.plotly_chart(fig_perf, use_container_width=True)
        st.dataframe(perf_data, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# ALERTS
# ══════════════════════════════════════════════════════════════
elif page == "Alerts":
    st.markdown("<h2>Alerts & Emergency Contacts</h2>", unsafe_allow_html=True)

    c1,c2 = st.columns([3,1])
    with c2:
        st.markdown(f"<div style='background:rgba(226,75,74,0.15);color:#F87171;font-size:12px;font-weight:700;padding:8px 14px;border-radius:8px;text-align:center;margin-top:8px;'>{sum(1 for a in ALERTS if a['type']=='critical')} Critical</div>", unsafe_allow_html=True)

    for alert in ALERTS:
        if alert["type"] == "critical":
            icon = "🚨"
            card_class = "hl-card-danger"
            badge_color = "#F87171"
            badge_bg = "rgba(226,75,74,0.2)"
            badge_label = "CRITICAL"
        else:
            icon = "⚠️"
            card_class = "hl-card-warning"
            badge_color = "#FCD34D"
            badge_bg = "rgba(245,158,11,0.2)"
            badge_label = "WARNING"

        st.markdown(f"""
        <div class='{card_class}'>
          <div style='display:flex;align-items:flex-start;gap:14px;'>
            <div style='font-size:26px;flex-shrink:0;'>{icon}</div>
            <div style='flex:1;'>
              <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div style='font-size:14px;font-weight:700;color:white;'>{alert["name"]} — {alert["id"]}</div>
                <div style='background:{badge_bg};color:{badge_color};font-size:10px;font-weight:700;padding:3px 8px;border-radius:20px;'>{badge_label}</div>
              </div>
              <div style='font-size:12px;color:rgba(255,255,255,0.5);margin-top:2px;'>{alert["sub"]} · {alert["cond"]}</div>
              <div style='font-size:13px;color:rgba(255,255,255,0.75);margin-top:6px;line-height:1.5;'>{alert["msg"]}</div>
              {"" if not alert["ec_phone"] else f'<div style="display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.04);border-radius:8px;padding:8px 12px;margin-top:10px;"><span style=\\"font-size:18px;\\">📞</span><div><div style=\\"font-size:11px;color:rgba(255,255,255,0.35);\\">Emergency Contact</div><div style=\\"font-size:13px;font-weight:600;color:white;\\">{alert["ec_name"]} · {alert["ec_rel"]}</div></div><div style=\\"margin-left:auto;font-size:14px;font-weight:700;color:#F87171;\\">{alert["ec_phone"]}</div></div>'}
              <div style='font-size:11px;color:rgba(255,255,255,0.25);margin-top:8px;'>{alert["time"]}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        if alert["ec_phone"]:
            ac1, ac2, ac3 = st.columns([1,1,2])
            with ac1:
                if st.button(f"📞 Call", key=f"call_{alert['id']}"):
                    st.info(f"Initiating call to {alert['ec_phone']}")
            with ac2:
                if st.button(f"✅ Ack", key=f"ack_{alert['id']}"):
                    st.success("Alert acknowledged.")

# ══════════════════════════════════════════════════════════════
# SETTINGS
# ══════════════════════════════════════════════════════════════
elif page == "Settings":
    st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("<div class='hl-card'>", unsafe_allow_html=True)
        st.markdown("<b style='color:white;'>Coverage Area</b>", unsafe_allow_html=True)
        st.text_input("County", value="Nakuru")
        st.text_input("Sub-counties", value="All")
        st.number_input("Distance threshold (km)", value=35, min_value=5, max_value=100)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        st.markdown("<div class='hl-card'>", unsafe_allow_html=True)
        st.markdown("<b style='color:white;'>Alert Thresholds</b>", unsafe_allow_html=True)
        st.slider("High-risk flag (score above)", 0.0, 1.0, 0.75)
        st.selectbox("Export format", ["CSV","Excel","JSON"])
        st.toggle("Email alerts", value=True)
        st.toggle("SMS emergency alerts", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 Save Changes", use_container_width=False):
        st.success("Settings saved.")

    st.markdown("---")
    st.markdown(f"""
    <div class='hl-card-teal'>
      <b style='color:#5DCAA5;'>HealthLink Kenya — System Info</b><br>
      <div style='font-size:12px;color:rgba(255,255,255,0.5);margin-top:8px;line-height:2.0;'>
        Access Model: XGBoost (Tuned) · F1: 0.8091 · AUC: 0.8144<br>
        Retention Model: XGBoost Stage 2 (SMOTE) · AUC: 0.8292 · Dropout recall: 53.4%<br>
        Dataset: KNBS HSB Survey 2022 · n = 99,031<br>
        Author: Rutendo Julia Kandeya · ID: 168332 · Strathmore University · 2026<br>
        Supervisor: Dr. Esther Khakata
      </div>
    </div>""", unsafe_allow_html=True)
