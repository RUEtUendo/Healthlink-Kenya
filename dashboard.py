"""
HealthLink Kenya — Social Worker Operations Dashboard
Rutendo Julia Kandeya · Strathmore University · 2026
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import joblib, requests, os, math, warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="HealthLink Kenya", page_icon="🏥", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Sora:wght@400;600;700&display=swap');

/* ── RESET & BASE ── */
html,body,[class*="css"]{font-family:'DM Sans',sans-serif !important;background:#0A1929 !important;color:#e2e8f0;}
.stApp{background:#0A1929 !important;}
section[data-testid="stSidebar"]{display:none !important;}
[data-testid="collapsedControl"]{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
h1,h2,h3{font-family:'Sora',sans-serif !important;color:white !important;margin-bottom:4px !important;}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton{display:none;}

/* ── TABS — match HTML nav ── */
.stTabs [data-baseweb="tab-list"]{
  background:#0C2340 !important;
  border-bottom:1px solid rgba(255,255,255,0.06) !important;
  padding:0 24px !important;
  gap:0 !important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent !important;
  color:rgba(255,255,255,0.45) !important;
  border:none !important;
  border-bottom:3px solid transparent !important;
  border-radius:0 !important;
  padding:14px 18px !important;
  font-size:13px !important;
  font-weight:500 !important;
  font-family:'DM Sans',sans-serif !important;
}
.stTabs [aria-selected="true"]{
  color:#5DCAA5 !important;
  border-bottom-color:#5DCAA5 !important;
  font-weight:600 !important;
  background:transparent !important;
}
.stTabs [data-baseweb="tab"]:hover{color:rgba(255,255,255,0.85) !important;background:rgba(255,255,255,0.04) !important;}
.stTabs [data-baseweb="tab-panel"]{padding:28px 32px !important;background:#0A1929 !important;}

/* ── METRICS ── */
div[data-testid="metric-container"]{
  background:#0C2340 !important;
  border:1px solid rgba(255,255,255,0.08) !important;
  border-radius:8px !important;
  padding:16px !important;
}
div[data-testid="metric-container"] label{color:rgba(255,255,255,0.4) !important;font-size:11px !important;text-transform:uppercase;letter-spacing:.06em;}
div[data-testid="metric-container"] [data-testid="stMetricValue"]{color:white !important;font-family:'Sora',sans-serif !important;font-size:26px !important;font-weight:700 !important;}
div[data-testid="metric-container"] [data-testid="stMetricDelta"]{color:#5DCAA5 !important;font-weight:600 !important;}

/* ── INPUTS ── */
.stTextInput>div>div>input,.stSelectbox>div>div{background:rgba(255,255,255,0.06) !important;border:1px solid rgba(255,255,255,0.12) !important;color:white !important;border-radius:6px !important;}
.stRadio label,.stCheckbox label,.stSlider label{color:rgba(255,255,255,0.7) !important;}
.stSelectbox label,.stTextInput label,.stSlider label,.stNumberInput label{color:rgba(255,255,255,0.4) !important;font-size:11px !important;text-transform:uppercase;letter-spacing:.05em;}

/* ── BUTTONS ── */
.stButton>button{
  background:linear-gradient(135deg,#1D9E75,#0F6E56) !important;
  color:white !important;border:none !important;border-radius:6px !important;
  font-size:13px !important;font-weight:600 !important;
  padding:8px 18px !important;
  font-family:'DM Sans',sans-serif !important;
}
.stButton>button[kind="secondary"]{
  background:rgba(255,255,255,0.07) !important;
  border:1px solid rgba(255,255,255,0.12) !important;
  color:rgba(255,255,255,0.7) !important;
}
.stButton>button:hover{opacity:.88 !important;}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"]{border-radius:8px;overflow:hidden;}
.stDataFrame th{background:#0C2340 !important;color:rgba(255,255,255,0.4) !important;font-size:11px !important;text-transform:uppercase;letter-spacing:.05em;}
.stDataFrame td{background:#091a2e !important;color:rgba(255,255,255,0.8) !important;font-size:13px !important;border-bottom:1px solid rgba(255,255,255,0.04) !important;}

/* ── CARDS ── */
.card{background:#0C2340;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:20px;margin-bottom:14px;}
.card-title{font-size:11px;font-weight:600;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px;}
.card-danger{background:rgba(226,75,74,0.07);border-left:4px solid #F87171;border-radius:12px;padding:18px 20px;margin-bottom:12px;}
.card-warning{background:rgba(245,158,11,0.07);border-left:4px solid #FCD34D;border-radius:12px;padding:18px 20px;margin-bottom:12px;}
.card-teal{background:rgba(29,158,117,0.07);border:1px solid rgba(29,158,117,0.25);border-radius:12px;padding:16px;margin-bottom:12px;}

/* ── HUB BUTTONS ── */
.hub-btn{background:#0F2847;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:24px 14px 20px;text-align:center;cursor:pointer;transition:all .2s;margin-bottom:8px;}
.hub-btn:hover{background:rgba(29,158,117,0.1);border-color:#5DCAA5;}

/* ── RISK PILLS ── */
.pill-high{background:rgba(226,75,74,0.18);color:#F87171;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;}
.pill-med{background:rgba(245,158,11,0.18);color:#FCD34D;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;}
.pill-low{background:rgba(16,185,129,0.18);color:#6EE7B7;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;}

/* ── MISC ── */
hr{border-color:rgba(255,255,255,0.07) !important;}
p,span,div,label{color:rgba(255,255,255,0.8);}
a{color:#5DCAA5 !important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    base = os.path.dirname(os.path.abspath(__file__))
    for a,r in [("health_access_pipeline.pkl","retention_pipeline.pkl"),
                (os.path.join(base,"health_access_pipeline.pkl"),os.path.join(base,"retention_pipeline.pkl"))]:
        try:
            if os.path.exists(a) and os.path.exists(r):
                return joblib.load(a), joblib.load(r), True
        except: pass
    return None, None, False

access_model, retention_model, models_ok = load_models()

def predict_access(dist,age,gender,wealth,insured,residence):
    if not access_model: return 72.0
    try:
        df=pd.DataFrame([{"distance_from_facility":dist,"insurance_status":"Yes" if insured else "No","education_level":"Secondary","age_group":age,"wealth_index1":wealth,"resid":residence,"gender":gender,"working_status":"Unknown"}])
        return round(float(access_model.predict_proba(df)[0][1])*100,1)
    except: return 72.0

def predict_retention(dist,age,gender,wealth,insured,residence):
    if not retention_model: return 65.0
    try:
        df=pd.DataFrame([{"distance_from_facility":dist,"insurance_status":"Yes" if insured else "No","education_level":"Secondary","age_group":age,"wealth_index1":wealth,"resid":residence,"gender":gender,"working_status":"Unknown"}])
        return round(float(retention_model.predict_proba(df)[0][1])*100,1)
    except: return 65.0

# ─────────────────────────────────────────────────────────────
# API
# ─────────────────────────────────────────────────────────────
API = "https://healthlink-kenya-production.up.railway.app"

def api_get(path, params=None):
    try:
        r = requests.get(f"{API}{path}", params=params, timeout=5)
        if r.status_code == 200: return r.json()
    except: pass
    return None

# ─────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────
FACILITIES = [
    {"name":"Nakuru PGH","lat":-0.2929,"lng":36.0763,"type":"hospital"},
    {"name":"Naivasha District Hospital","lat":-0.7145,"lng":36.4335,"type":"hospital"},
    {"name":"Bahati District Hospital","lat":-0.1703,"lng":36.1237,"type":"hospital"},
    {"name":"Molo District Hospital","lat":-0.2500,"lng":35.7337,"type":"hospital"},
    {"name":"Gilgil Sub-District Hospital","lat":-0.4987,"lng":36.3225,"type":"hospital"},
    {"name":"Subukia SDH","lat":-0.0003,"lng":36.2283,"type":"hospital"},
    {"name":"Lanet Health Centre","lat":-0.2699,"lng":36.1071,"type":"clinic"},
    {"name":"Njoro Health Centre","lat":-0.3355,"lng":35.9394,"type":"clinic"},
    {"name":"Rongai Health Centre","lat":-0.2029,"lng":35.9612,"type":"clinic"},
    {"name":"Bahati Dispensary","lat":-0.1540,"lng":36.1536,"type":"dispensary"},
    {"name":"Mbaruk Dispensary","lat":-0.4996,"lng":36.3237,"type":"dispensary"},
]

HH = [
    {"id":"HH-NK-00234","name":"Rutendo Nyamari","age":34,"cond":"Hypertension","risk":"High","dist":41.2,"ins":"None","sub":"Bahati","lat":-0.154,"lng":36.140},
    {"id":"HH-NK-00891","name":"Joseph Mwangi","age":52,"cond":"Diabetes T2","risk":"High","dist":28.5,"ins":"None","sub":"Njoro","lat":-0.368,"lng":35.970},
    {"id":"HH-NK-01102","name":"Aisha Karimi","age":29,"cond":"Maternal Care","risk":"Medium","dist":19.3,"ins":"NHIF","sub":"Rongai","lat":-0.190,"lng":35.980},
    {"id":"HH-NK-00455","name":"Samuel Otieno","age":45,"cond":"TB Follow-up","risk":"Medium","dist":36.7,"ins":"None","sub":"Subukia","lat":0.020,"lng":36.220},
    {"id":"HH-NK-00678","name":"Fatuma Hassan","age":38,"cond":"HIV Care","risk":"Low","dist":3.1,"ins":"Partial","sub":"Nakuru Town","lat":-0.303,"lng":36.075},
    {"id":"HH-NK-00312","name":"Grace Wambui","age":61,"cond":"Hypertension","risk":"High","dist":52.3,"ins":"None","sub":"Molo","lat":-0.270,"lng":35.760},
    {"id":"HH-NK-00549","name":"Daniel Kimani","age":44,"cond":"Diabetes T2","risk":"Medium","dist":22.1,"ins":"NHIF","sub":"Gilgil","lat":-0.480,"lng":36.300},
    {"id":"HH-NK-00763","name":"Susan Njoki","age":33,"cond":"Maternal Care","risk":"Low","dist":7.8,"ins":"NHIF","sub":"Bahati","lat":-0.185,"lng":36.130},
    {"id":"HH-NK-00988","name":"Peter Koech","age":58,"cond":"TB Screening","risk":"High","dist":47.0,"ins":"None","sub":"Kuresoi","lat":-0.420,"lng":35.690},
    {"id":"HH-NK-01055","name":"Mary Auma","age":27,"cond":"Child Nutrition","risk":"Low","dist":11.2,"ins":"NHIF","sub":"Rongai","lat":-0.150,"lng":36.020},
]

ALERTS_DATA = [
    {"id":"HH-NK-00234","name":"Rutendo Nyamari","sub":"Bahati","cond":"Hypertension","sev":"critical",
     "msg":"Reported chest pain and difficulty breathing. Missed follow-up scheduled 5 Apr 2026.",
     "ec":"James Nyamari","rel":"Spouse","phone":"+254 712 445 678","time":"Today at 08:14 AM"},
    {"id":"HH-NK-00312","name":"Grace Wambui","sub":"Molo","cond":"Hypertension","sev":"critical",
     "msg":"New registration flagged risk score 0.91. Distance 52.3km — beyond decay threshold. No insurance.",
     "ec":"Grace Wanjiku","rel":"Mother","phone":"+254 728 990 112","time":"Today at 09:32 AM"},
    {"id":"HH-NK-00891","name":"Joseph Mwangi","sub":"Njoro","cond":"Diabetes T2","sev":"critical",
     "msg":"Missed 2 consecutive follow-up appointments. Last contact 15 Feb 2026. Dropout risk elevated.",
     "ec":"Peter Kamau","rel":"Brother","phone":"+254 700 334 891","time":"Yesterday at 04:45 PM"},
    {"id":"HH-NK-00455","name":"Samuel Otieno","sub":"Subukia","cond":"TB Follow-up","sev":"warning",
     "msg":"Distance 36.7km exceeds 35km decay threshold. Utilisation probability dropped to 38%.",
     "ec":"","rel":"","phone":"","time":"2 days ago"},
]

USERS = {
    "amara@healthlink.ke":{"pw":"sw2026","name":"Amara Ochieng","initials":"AO","role":"Social Worker","county":"Nakuru"},
    "admin@healthlink.ke":{"pw":"admin2026","name":"Supervisor Admin","initials":"SA","role":"Supervisor","county":"Nakuru"},
    "doctor@healthlink.ke":{"pw":"Doctor2024!","name":"Dr. Wanjiku","initials":"DW","role":"Clinician","county":"Nairobi"},
}

def hav(lat1,lng1,lat2,lng2):
    R=6371;dlat=math.radians(lat2-lat1);dlng=math.radians(lng2-lng1)
    a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k,v in [("auth",False),("user",{}),("db_page",1),("sel_hh",None)]:
    if k not in st.session_state: st.session_state[k]=v

# ─────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────
if not st.session_state.auth:
    st.markdown("""
    <div style='min-height:100vh;background:linear-gradient(135deg,#0C2D5E 0%,#185FA5 50%,#1D9E75 100%);
         display:flex;align-items:center;justify-content:center;padding:40px;'>
    """, unsafe_allow_html=True)
    _,col,_ = st.columns([1,1,1])
    with col:
        st.markdown("""
        <div style='background:white;border-radius:20px;padding:48px;box-shadow:0 20px 60px rgba(0,0,0,0.25);'>
          <div style='display:flex;align-items:center;gap:12px;margin-bottom:28px;'>
            <div style='width:44px;height:44px;background:linear-gradient(135deg,#1D9E75,#185FA5);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;'>🏥</div>
            <div style='font-family:Sora,sans-serif;font-size:20px;font-weight:700;color:#0C2D5E;'>Health<span style='color:#1D9E75;'>Link</span> Kenya</div>
          </div>
          <div style='font-family:Sora,sans-serif;font-size:24px;font-weight:700;color:#0C2D5E;margin-bottom:4px;'>Welcome back</div>
          <div style='font-size:14px;color:#6b7a8d;margin-bottom:28px;'>Sign in to your Social Worker dashboard</div>
          <div style='border:2px solid #1D9E75;border-radius:12px;padding:20px;text-align:center;background:#E1F5EE;margin-bottom:24px;'>
            <div style='font-size:32px;margin-bottom:8px;'>🧑‍💼</div>
            <div style='font-size:15px;font-weight:700;color:#0C2D5E;'>Social Worker</div>
            <div style='font-size:12px;color:#0F6E56;font-weight:600;margin-top:3px;'>Nakuru County Field Officer</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="you@healthlink.ke", label_visibility="collapsed",
                              key="login_email")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Enter password",
                                 label_visibility="collapsed", key="login_pw")
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("Sign In →", use_container_width=True):
            if email in USERS and USERS[email]["pw"] == password:
                st.session_state.auth = True
                st.session_state.user = USERS[email]
                st.rerun()
            else:
                st.error("Invalid credentials. Try: amara@healthlink.ke / sw2026")
        st.markdown("""
        <div style='margin-top:16px;padding:10px 14px;background:#F7F9FC;border-radius:8px;font-size:11px;color:#6b7a8d;line-height:2.0;'>
          <b style='color:#1D9E75;'>Demo accounts:</b><br>
          amara@healthlink.ke · <i>sw2026</i><br>
          admin@healthlink.ke · <i>admin2026</i>
        </div>""", unsafe_allow_html=True)
    st.stop()

user = st.session_state.user

# ─────────────────────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:#0C2340;padding:16px 32px;display:flex;align-items:center;
     justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);'>
  <div style='display:flex;align-items:center;gap:12px;'>
    <div style='width:32px;height:32px;background:linear-gradient(135deg,#1D9E75,#185FA5);
         border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;'>🏥</div>
    <div style='font-family:Sora,sans-serif;font-size:15px;font-weight:700;color:white;'>
      Health<span style='color:#5DCAA5;'>Link</span></div>
  </div>
  <div style='display:flex;align-items:center;gap:14px;'>
    <div style='display:flex;align-items:center;gap:8px;'>
      <div style='width:30px;height:30px;border-radius:50%;background:#0F6E56;display:flex;
           align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;'>{user.get("initials","AO")}</div>
      <div>
        <div style='font-size:12px;font-weight:600;color:white;'>{user.get("name","User")}</div>
        <div style='font-size:10px;color:#5DCAA5;'>{user.get("role","")} · {user.get("county","")}</div>
      </div>
    </div>
    {'<div style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);border-radius:6px;padding:4px 10px;font-size:11px;color:#6EE7B7;">✅ Models active</div>' if models_ok else '<div style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);border-radius:6px;padding:4px 10px;font-size:11px;color:#FCD34D;">⚠️ Fallback mode</div>'}
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MAIN TABS — single click, matches HTML nav exactly
# ─────────────────────────────────────────────────────────────
tabs = st.tabs(["⊞  Outreach Hub", "🗺️  Geospatial", "🚐  Mobile Clinic",
                "👥  Triage", "🗄️  Patient Database", "📊  Reports",
                "🔔  Alerts", "⚙️  Settings"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — OUTREACH HUB
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;'>
      <div>
        <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Outreach Hub</div>
        <div style='font-size:13px;color:rgba(255,255,255,0.45);margin-top:2px;'>Nakuru County — select a module to begin</div>
      </div>
      <span style='background:rgba(29,158,117,0.15);border:1px solid rgba(29,158,117,0.3);color:#5DCAA5;
            font-size:11px;font-weight:600;padding:5px 12px;border-radius:20px;'>📍 Nakuru County</span>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    stats = api_get("/analytics/dashboard/stats") or {"total":30,"high_risk":9,"medium_risk":11,"coverage_rate":70.0}
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("High-risk households", "1,284", "↑ 12% this month")
    c2.metric("Health-evasive profiles", stats.get("total",30), f"High: {stats.get('high_risk',9)}")
    c3.metric("Active outreach routes", "23", "↑ 3 added")
    c4.metric("Avg. retention score", f"{stats.get('coverage_rate',70)}%", "↑ 2pts vs last month")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Hub grid
    hub = [
        ("🗺️","Geospatial Mapper","Risk zones, facilities & household IDs"),
        ("📊","Reports","Triage, SHAP & distance decay"),
        ("👥","Patient Triage","View patient profiles & risk"),
        ("🚐","Mobile Clinic Routing","Household IDs on field map"),
        ("📉","Distance Decay","Pin-drop household range analysis"),
        ("🔔","Alerts","Emergency contacts · High-risk flags"),
        ("📤","Export","Download county reports"),
        ("🗄️","Patient Database","All registered patients — full records"),
    ]
    cols = st.columns(4)
    for i,(icon,label,desc) in enumerate(hub):
        with cols[i%4]:
            st.markdown(f"""
            <div class='hub-btn'>
              <div style='font-size:30px;margin-bottom:10px;'>{icon}</div>
              <div style='font-size:13px;font-weight:600;color:white;'>{label}</div>
              <div style='font-size:11px;color:rgba(255,255,255,0.4);margin-top:4px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px;color:rgba(255,255,255,0.3);margin-bottom:16px;'>↑ Use the tabs above to navigate to any module</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Active alerts preview
    st.markdown("<div style='font-family:Sora,sans-serif;font-size:16px;font-weight:600;color:white;margin-bottom:14px;'>Recent Alerts</div>", unsafe_allow_html=True)
    for a in ALERTS_DATA[:2]:
        st.markdown(f"""
        <div class='card-danger'>
          <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
            <div style='font-size:14px;font-weight:700;color:white;'>🚨 {a["name"]} — {a["id"]}</div>
            <span style='background:rgba(226,75,74,0.2);color:#F87171;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;'>CRITICAL</span>
          </div>
          <div style='font-size:12px;color:rgba(255,255,255,0.5);margin-top:3px;'>{a["sub"]} · {a["cond"]}</div>
          <div style='font-size:13px;color:rgba(255,255,255,0.7);margin-top:6px;line-height:1.5;'>{a["msg"]}</div>
          <div style='font-size:11px;color:rgba(255,255,255,0.25);margin-top:6px;'>{a["time"]}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2 — GEOSPATIAL MAPPER
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;'>
      <div>
        <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Geospatial Mapper</div>
        <div style='font-size:13px;color:rgba(255,255,255,0.45);'>Facility coverage, household IDs & distance decay — Nakuru County</div>
      </div>
    </div>""", unsafe_allow_html=True)

    ctrl1,ctrl2,ctrl3,ctrl4 = st.columns(4)
    show_hh   = ctrl1.checkbox("Households", value=True)
    show_risk = ctrl2.checkbox("Risk zones",  value=True)
    show_fac  = ctrl3.checkbox("Facilities",  value=True)
    decay_km  = ctrl4.slider("Decay ring (km)", 10, 60, 35, label_visibility="visible")

    m = folium.Map(location=[-0.310,36.080], zoom_start=9, tiles="CartoDB dark_matter")

    if show_fac:
        for f in FACILITIES:
            c = "#1D9E75" if f["type"]=="hospital" else "#185FA5" if f["type"]=="clinic" else "#8B5CF6"
            sz = 8 if f["type"]=="hospital" else 6 if f["type"]=="clinic" else 5
            folium.CircleMarker([f["lat"],f["lng"]], radius=sz, color="white", weight=1.5,
                fill=True, fill_color=c, fill_opacity=0.9,
                tooltip=f["name"], popup=folium.Popup(f"<b>{f['name']}</b><br>{f['type'].title()}", max_width=180)).add_to(m)

    if show_hh:
        for hh in HH:
            rc = "#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            folium.CircleMarker([hh["lat"],hh["lng"]], radius=8, color="white", weight=2,
                fill=True, fill_color=rc, fill_opacity=0.9,
                tooltip=f"{hh['id']} · {hh['name']} · {hh['risk']} Risk",
                popup=folium.Popup(f"<b>{hh['id']}</b><br>{hh['name']}, {hh['age']}yrs<br>{hh['cond']}<br>{hh['dist']}km · {hh['ins']}", max_width=200)).add_to(m)

    if show_risk:
        for z in [{"lat":-0.17,"lng":36.12,"r":8000,"c":"#E24B4A","l":"Bahati High-Risk Zone"},
                  {"lat":-0.42,"lng":35.70,"r":12000,"c":"#E24B4A","l":"Kuresoi High-Risk Zone"},
                  {"lat":0.04,"lng":36.22,"r":7000,"c":"#F59E0B","l":"Subukia Medium Zone"},
                  {"lat":-0.50,"lng":36.33,"r":5000,"c":"#10B981","l":"Gilgil Low-Risk Zone"}]:
            folium.Circle([z["lat"],z["lng"]], radius=z["r"], color=z["c"], fill=True,
                fill_color=z["c"], fill_opacity=0.12, weight=1.5, tooltip=z["l"]).add_to(m)

    folium.Circle([-0.293,36.076], radius=decay_km*1000, color="#F59E0B",
        fill=False, weight=2, dash_array="8 6", tooltip=f"{decay_km}km decay threshold").add_to(m)

    map_out = st_folium(m, width="100%", height=440, returned_objects=["last_clicked"])

    # Stats row below map
    s1,s2,s3,s4 = st.columns(4)
    s1.metric("Facilities in view", len(FACILITIES))
    s2.metric("Households mapped", len(HH) if show_hh else 0)
    s3.metric("Decay threshold", f"{decay_km} km")
    s4.metric("Top barrier", "Distance")

    # Legend
    st.markdown("""
    <div class='card' style='margin-top:14px;'>
      <div class='card-title'>Legend</div>
      <div style='display:flex;gap:24px;flex-wrap:wrap;'>
        <div style='display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.6);'>
          <div style='width:10px;height:10px;background:#1D9E75;border-radius:2px;'></div>Hospital / District H.</div>
        <div style='display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.6);'>
          <div style='width:10px;height:10px;background:#185FA5;border-radius:2px;'></div>Health Centre / Clinic</div>
        <div style='display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.6);'>
          <div style='width:10px;height:10px;background:#8B5CF6;border-radius:50%;'></div>Dispensary</div>
        <div style='display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.6);'>
          <div style='width:10px;height:10px;background:#F87171;border-radius:50%;'></div>High evasion risk HH</div>
        <div style='display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.6);'>
          <div style='width:10px;height:10px;background:#FCD34D;border-radius:50%;'></div>Medium risk HH</div>
        <div style='display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.6);'>
          <div style='width:10px;height:10px;background:#6EE7B7;border-radius:50%;'></div>Low risk HH</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Click analysis
    if map_out and map_out.get("last_clicked"):
        clat = map_out["last_clicked"]["lat"]; clng = map_out["last_clicked"]["lng"]
        nearest = sorted(FACILITIES, key=lambda f: hav(clat,clng,f["lat"],f["lng"]))[:3]
        st.markdown(f"<div class='card-teal'><b style='color:#5DCAA5;'>📌 Pin dropped at ({clat:.4f}, {clng:.4f})</b></div>", unsafe_allow_html=True)
        nc = st.columns(3)
        for i,f in enumerate(nearest):
            d = hav(clat,clng,f["lat"],f["lng"])
            col = "#6EE7B7" if d<=decay_km else "#F87171"
            with nc[i]:
                st.markdown(f"""<div class='card' style='padding:14px;'>
                  <div style='font-size:12px;font-weight:600;color:white;'>{f["name"]}</div>
                  <div style='font-size:11px;color:rgba(255,255,255,0.4);'>{f["type"].title()}</div>
                  <div style='font-size:18px;font-weight:700;color:{col};margin-top:6px;'>{d:.1f} km</div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 3 — MOBILE CLINIC ROUTING
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;'>
      <div>
        <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Mobile Clinic Routing</div>
        <div style='font-size:13px;color:rgba(255,255,255,0.45);'>Select a household to locate on map — nearest facilities shown automatically</div>
      </div>
    </div>""", unsafe_allow_html=True)

    rf = st.radio("Filter by risk", ["All","High","Medium","Low"], horizontal=True)
    filtered = [h for h in HH if rf=="All" or h["risk"]==rf]

    col_list, col_map = st.columns([1,2.2])

    with col_list:
        st.markdown(f"<div style='font-size:10px;font-weight:700;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px;padding-left:2px;'>{len(filtered)} Households</div>", unsafe_allow_html=True)
        for hh in filtered:
            rc = "#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            is_sel = st.session_state.sel_hh and st.session_state.sel_hh["id"]==hh["id"]
            bg = "rgba(29,158,117,0.1)" if is_sel else "#0C2340"
            bdr = "#5DCAA5" if is_sel else "rgba(255,255,255,0.07)"
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {bdr};border-radius:8px;padding:11px 14px;
                 margin-bottom:5px;cursor:pointer;'>
              <div style='display:flex;align-items:center;gap:8px;'>
                <div style='width:7px;height:7px;border-radius:50%;background:{rc};flex-shrink:0;'></div>
                <div style='min-width:0;'>
                  <div style='font-size:12px;font-weight:700;color:{rc};font-family:monospace;'>{hh["id"]}</div>
                  <div style='font-size:11px;color:rgba(255,255,255,0.5);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{hh["name"]} · {hh["sub"]}</div>
                  <div style='font-size:10px;color:rgba(255,255,255,0.3);'>{hh["dist"]} km · {hh["cond"]}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button("Select", key=f"mc_{hh['id']}", use_container_width=True):
                st.session_state.sel_hh = hh
                st.rerun()

    with col_map:
        sel = st.session_state.sel_hh or (filtered[0] if filtered else None)
        center = [sel["lat"],sel["lng"]] if sel else [-0.310,36.080]
        m2 = folium.Map(location=center, zoom_start=11 if sel else 9, tiles="CartoDB dark_matter")

        for f in FACILITIES:
            c = "#1D9E75" if f["type"]=="hospital" else "#185FA5" if f["type"]=="clinic" else "#8B5CF6"
            folium.CircleMarker([f["lat"],f["lng"]], radius=6, color="white", weight=1.5,
                fill=True, fill_color=c, fill_opacity=0.85, tooltip=f["name"]).add_to(m2)

        for hh in filtered:
            rc = "#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            is_sel = sel and hh["id"]==sel["id"]
            folium.CircleMarker([hh["lat"],hh["lng"]], radius=11 if is_sel else 7,
                color="white", weight=3 if is_sel else 1.5, fill=True, fill_color=rc,
                fill_opacity=0.95 if is_sel else 0.8, tooltip=f"{hh['id']} · {hh['risk']}").add_to(m2)

        if sel:
            nf = sorted(FACILITIES, key=lambda f: hav(sel["lat"],sel["lng"],f["lat"],f["lng"]))[0]
            folium.PolyLine([[sel["lat"],sel["lng"]],[nf["lat"],nf["lng"]]],
                color="#F59E0B", weight=2.5, dash_array="8 5", opacity=0.85).add_to(m2)

        st_folium(m2, width="100%", height=500)

    # Detail card
    if sel:
        nfacs = sorted(FACILITIES, key=lambda f: hav(sel["lat"],sel["lng"],f["lat"],f["lng"]))[:3]
        rc = "#F87171" if sel["risk"]=="High" else "#FCD34D" if sel["risk"]=="Medium" else "#6EE7B7"
        ic = "#6EE7B7" if sel["ins"]=="NHIF" else "#FCD34D" if sel["ins"]=="Partial" else "#F87171"

        st.markdown(f"""
        <div class='card' style='margin-top:14px;'>
          <div style='display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:20px;'>
            <div style='width:42px;height:42px;border-radius:50%;background:{rc}22;border:2px solid {rc}55;
                 display:flex;align-items:center;justify-content:center;font-size:18px;'>🏠</div>
            <div>
              <div style='font-family:Sora,sans-serif;font-size:15px;font-weight:700;color:white;'>{sel["id"]}</div>
              <div style='font-size:12px;color:rgba(255,255,255,0.45);margin-top:2px;'>{sel["name"]} · {sel["age"]} yrs · {sel["sub"]}</div>
            </div>
            <div style='text-align:right;'>
              <div style='font-size:13px;font-weight:700;color:{rc};'>{sel["risk"]} Risk</div>
              <div style='font-size:12px;font-weight:600;color:{ic};'>{sel["ins"]}</div>
            </div>
          </div>
          <div style='margin-top:14px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.07);'>
            <div style='font-size:10px;font-weight:700;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px;'>3 nearest facilities</div>
            <div style='display:flex;gap:10px;'>
              {"".join([f'<div style="flex:1;background:#0F2847;border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:10px 12px;"><div style="font-size:12px;font-weight:600;color:white;">{f["name"]}</div><div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:2px;">{hav(sel["lat"],sel["lng"],f["lat"],f["lng"]):.1f} km · {f["type"]}</div></div>' for f in nfacs])}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 4 — PREDICTIVE TRIAGE
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("""
    <div style='margin-bottom:20px;'>
      <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Patient Triage</div>
      <div style='font-size:13px;color:rgba(255,255,255,0.45);'>Enter patient profile → live XGBoost prediction → nearest facilities</div>
    </div>""", unsafe_allow_html=True)

    cf, cr = st.columns([1,1])

    with cf:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Patient Profile</div>", unsafe_allow_html=True)
        age    = st.selectbox("Age Group", ["0-4","5-14","15-24","25-34","35-49","50-64","65+"])
        gender = st.selectbox("Gender", ["Female","Male"])
        res    = st.radio("Residence Type", ["Urban","Rural","Peri-Urban"], horizontal=True)
        wealth = st.select_slider("Wealth Index", options=["Poorest","Poorer","Middle","Richer","Richest"])
        ins    = st.radio("Insurance Status", ["Insured","Uninsured"], horizontal=True)
        dist   = st.slider("Distance to Nearest Facility (km)", 0.0, 100.0, 5.0, 0.5)

        if dist > 35:
            st.markdown("<div class='card-danger' style='padding:10px 14px;font-size:12px;'>📍 Beyond 35km GAM threshold — access probability drops sharply.</div>", unsafe_allow_html=True)

        run = st.button("🔍 Run Access Prediction", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with cr:
        if run:
            acc = predict_access(dist,age,gender,wealth,ins=="Insured",res)
            ret = predict_retention(dist,age,gender,wealth,ins=="Insured",res)
            st.session_state.triage_result = {"acc":acc,"ret":ret,"dist":dist}

        if "triage_result" in st.session_state:
            p = st.session_state.triage_result
            acc,ret,d = p["acc"],p["ret"],p["dist"]
            ac = "#6EE7B7" if acc>=70 else "#FCD34D" if acc>=40 else "#F87171"
            rc = "#6EE7B7" if ret>=70 else "#FCD34D" if ret>=40 else "#F87171"

            st.markdown(f"""
            <div class='card'>
              <div class='card-title'>Prediction Results</div>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;'>
                <div style='text-align:center;background:#0F2847;border-radius:10px;padding:20px 10px;'>
                  <div style='font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;'>Access Probability</div>
                  <div style='font-family:Sora,sans-serif;font-size:38px;font-weight:700;color:{ac};'>{acc}%</div>
                  <div style='font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px;'>XGBoost · Live</div>
                </div>
                <div style='text-align:center;background:#0F2847;border-radius:10px;padding:20px 10px;'>
                  <div style='font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;'>Retention Probability</div>
                  <div style='font-family:Sora,sans-serif;font-size:38px;font-weight:700;color:{rc};'>{ret}%</div>
                  <div style='font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px;'>Stage 2 · SMOTE</div>
                </div>
              </div>
              <div style='font-size:13px;font-weight:600;color:{"#6EE7B7" if d<=35 else "#F87171"};margin-bottom:12px;'>
                {"🟢 Safe Zone (≤35km)" if d<=35 else "🔴 Beyond 35km Threshold"} · {d} km
              </div>
            </div>""", unsafe_allow_html=True)

            if acc>=70:   st.markdown("<div class='card-teal'>✅ <b>High likelihood of access.</b> Standard outreach schedule appropriate.</div>", unsafe_allow_html=True)
            elif acc>=40: st.markdown("<div class='card-warning'>⚡ <b>Moderate likelihood.</b> Consider transport support or CHW follow-up.</div>", unsafe_allow_html=True)
            else:         st.markdown("<div class='card-danger'>🚨 <b>Low likelihood.</b> Prioritise mobile clinic or immediate CHW dispatch.</div>", unsafe_allow_html=True)

            fig = go.Figure(go.Bar(
                x=[acc,ret], y=["Access","Retention"], orientation="h",
                marker_color=[ac,rc], text=[f"{acc}%",f"{ret}%"],
                textposition="outside", textfont=dict(color="white",size=13)))
            fig.update_layout(paper_bgcolor="#0C2340", plot_bgcolor="#0C2340", height=140,
                margin=dict(l=10,r=70,t=10,b=10), showlegend=False,
                xaxis=dict(range=[0,115], showgrid=False, tickfont=dict(color="rgba(255,255,255,0.35)")),
                yaxis=dict(tickfont=dict(color="white",size=13)))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class='card' style='text-align:center;padding:60px 20px;'>
              <div style='font-size:44px;margin-bottom:14px;'>🔍</div>
              <div style='font-size:14px;color:rgba(255,255,255,0.4);'>Fill in the patient profile and click<br>Run Access Prediction</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 5 — PATIENT DATABASE
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""
    <div style='margin-bottom:20px;'>
      <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Patient Database</div>
      <div style='font-size:13px;color:rgba(255,255,255,0.45);'>All registered patients — Nakuru County</div>
    </div>""", unsafe_allow_html=True)

    fc1,fc2,fc3,fc4 = st.columns([2.5,1,1,1])
    with fc1: srch = st.text_input("🔍 Search name, ID, sub-county...", placeholder="Search...", label_visibility="collapsed")
    with fc2: rf   = st.selectbox("Risk Level", ["","High","Medium","Low"], label_visibility="collapsed")
    with fc3: sf   = st.selectbox("Sub-county", ["","Nakuru Town","Bahati","Njoro","Rongai","Subukia","Kuresoi","Molo","Gilgil","Naivasha"], label_visibility="collapsed")
    with fc4:
        if st.button("⬇ Export CSV", use_container_width=True): pass

    data = api_get("/patients/", params={"page":st.session_state.db_page,"page_size":10,
        **({"risk":rf} if rf else {}), **({"sub_county":sf} if sf else {}), **({"search":srch} if srch else {})})

    if data:
        total   = data.get("total",0)
        patients = data.get("data",[])
        m1,m2,m3,m4,m5 = st.columns(5)
        m1.metric("Total Registered", total)
        m2.metric("High Risk",  sum(1 for p in patients if p.get("risk")=="High"))
        m3.metric("Medium Risk",sum(1 for p in patients if p.get("risk")=="Medium"))
        m4.metric("Low Risk",   sum(1 for p in patients if p.get("risk")=="Low"))
        m5.metric("NHIF",       sum(1 for p in patients if p.get("insurance")=="NHIF"))

        rows = []
        for p in patients:
            rows.append({
                "Patient ID": p.get("id",""),
                "Name": p.get("name",""),
                "Age": p.get("age",""),
                "Gender": p.get("gender",""),
                "Sub-county": p.get("sub_county",""),
                "Condition": p.get("condition",""),
                "Risk": p.get("risk",""),
                "Dist (km)": p.get("distance_km",""),
                "Insurance": p.get("insurance",""),
                "Last Visit": p.get("last_visit") or "N/A",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True, height=420)

        total_pages = max(1,math.ceil(total/10))
        pc1,pc2,pc3 = st.columns([1,3,1])
        with pc1:
            if st.button("← Prev", disabled=st.session_state.db_page<=1):
                st.session_state.db_page-=1; st.rerun()
        with pc2:
            st.markdown(f"<div style='text-align:center;color:rgba(255,255,255,0.35);font-size:12px;padding-top:10px;'>Showing page {st.session_state.db_page} of {total_pages} · {total} records</div>", unsafe_allow_html=True)
        with pc3:
            if st.button("Next →", disabled=st.session_state.db_page>=total_pages):
                st.session_state.db_page+=1; st.rerun()

        if st.session_state.get("export_csv"):
            st.download_button("Download CSV", df.to_csv(index=False), "nakuru_patients.csv", "text/csv")
    else:
        st.markdown("<div class='card-warning'>⚠️ FastAPI backend offline — showing static fallback data</div>", unsafe_allow_html=True)
        fb = pd.DataFrame(HH)[["id","name","age","cond","risk","dist","ins","sub"]]
        fb.columns = ["Patient ID","Name","Age","Condition","Risk","Distance (km)","Insurance","Sub-county"]
        st.dataframe(fb, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 6 — REPORTS
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("""
    <div style='margin-bottom:20px;'>
      <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Reports</div>
      <div style='font-size:13px;color:rgba(255,255,255,0.45);'>Predictive triage · SHAP attribution · Distance decay analytics</div>
    </div>""", unsafe_allow_html=True)

    rt1,rt2,rt3 = st.tabs(["Predictive Risk Triage","SHAP Feature Importance","Distance Decay — GAM"])

    with rt1:
        st.markdown("<div class='card-title' style='margin-top:8px;'>Predictive risk triage — Nakuru County</div>", unsafe_allow_html=True)
        triage_data = [
            {"id":"HH-NK-00234","sub":"Bahati","risk":"High 0.87","barrier":"Distance","dist":41.2,"ins":"None"},
            {"id":"HH-NK-00891","sub":"Njoro","risk":"High 0.82","barrier":"Education","dist":28.5,"ins":"None"},
            {"id":"HH-NK-01102","sub":"Rongai","risk":"Med 0.65","barrier":"Wealth","dist":19.3,"ins":"NHIF"},
            {"id":"HH-NK-00455","sub":"Subukia","risk":"Med 0.61","barrier":"Distance","dist":36.7,"ins":"None"},
            {"id":"HH-NK-00678","sub":"Nakuru Town","risk":"Low 0.31","barrier":"Insurance","dist":3.1,"ins":"Partial"},
        ]
        tr = pd.DataFrame(triage_data)
        tr.columns = ["Household ID","Sub-county","Risk Score","Primary Barrier","Distance (km)","Insurance"]
        st.dataframe(tr, use_container_width=True, hide_index=True)

    with rt2:
        shap_df = pd.DataFrame([
            {"Feature":"Education Level","Importance":73.2,"Category":"Predisposing"},
            {"Feature":"Distance (km)","Importance":12.9,"Category":"Enabling"},
            {"Feature":"Wealth Index","Importance":8.4,"Category":"Enabling"},
            {"Feature":"Insurance Status","Importance":5.5,"Category":"Enabling"},
        ])
        colors = {"Predisposing":"#6366F1","Enabling":"#F59E0B"}
        fig = go.Figure(go.Bar(
            x=shap_df["Importance"], y=shap_df["Feature"], orientation="h",
            marker_color=[colors[c] for c in shap_df["Category"]],
            text=[f"{v}%" for v in shap_df["Importance"]],
            textposition="outside", textfont=dict(color="white",size=13)))
        fig.update_layout(paper_bgcolor="#0C2340", plot_bgcolor="#0C2340", height=300,
            margin=dict(l=10,r=80,t=16,b=10), showlegend=False,
            xaxis=dict(range=[0,95], tickfont=dict(color="rgba(255,255,255,0.4)"), gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(tickfont=dict(color="white",size=13), autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

        rc1,rc2 = st.columns(2)
        rc1.markdown("<div class='card-warning'><b style='color:#F59E0B;'>Enabling Factors · 26.8%</b><br><span style='font-size:12px;color:rgba(255,255,255,0.5);'>Distance + Wealth Index + Insurance Status</span></div>", unsafe_allow_html=True)
        rc2.markdown("<div class='card' style='border-left:3px solid #6366F1;'><b style='color:#A78BFA;'>Predisposing Factors · 73.2%</b><br><span style='font-size:12px;color:rgba(255,255,255,0.5);'>Education level dominates model predictions</span></div>", unsafe_allow_html=True)

    with rt3:
        GAM_D = [0,5,10,15,20,25,30,35,40,50,60]
        GAM_P = [0.899,0.905,0.910,0.914,0.916,0.918,0.910,0.895,0.875,0.840,0.800]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=[d for d in GAM_D if d<=35]+[35],
            y=[p for d,p in zip(GAM_D,GAM_P) if d<=35]+[0.895],
            fill="tozeroy", fillcolor="rgba(16,185,129,0.08)",
            line=dict(color="rgba(0,0,0,0)"), showlegend=False))
        fig2.add_trace(go.Scatter(
            x=[d for d in GAM_D if d>=35],
            y=[p for d,p in zip(GAM_D,GAM_P) if d>=35],
            fill="tozeroy", fillcolor="rgba(239,68,68,0.07)",
            line=dict(color="rgba(0,0,0,0)"), showlegend=False))
        fig2.add_trace(go.Scatter(
            x=GAM_D, y=GAM_P, mode="lines+markers",
            line=dict(color="#1D9E75",width=3),
            marker=dict(size=7,color="#5DCAA5"),
            name="P(Access | Distance)",
            hovertemplate="Distance: %{x} km<br>Access Prob: %{y:.1%}"))
        fig2.add_vline(x=35, line_dash="dash", line_color="#F59E0B", line_width=2,
            annotation_text="35 km — decay accelerates",
            annotation_font_color="#F59E0B", annotation_position="top right")
        fig2.update_layout(
            paper_bgcolor="#0C2340", plot_bgcolor="#0C2340", height=400,
            xaxis=dict(title="Distance to Nearest Facility (km)", color="rgba(255,255,255,0.5)",
                       gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="rgba(255,255,255,0.5)")),
            yaxis=dict(title="Access Probability", tickformat=".0%", color="rgba(255,255,255,0.5)",
                       gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="rgba(255,255,255,0.5)")),
            legend=dict(bgcolor="#0C2340", bordercolor="rgba(255,255,255,0.1)"),
            margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig2, use_container_width=True)
        g1,g2,g3 = st.columns(3)
        g1.markdown("<div class='card-teal'><b style='color:#5DCAA5;'>0–35 km · Stable Zone</b><br><span style='font-size:12px;color:rgba(255,255,255,0.5);'>Access 89.9–91.8% within surveyed cohort.</span></div>", unsafe_allow_html=True)
        g2.markdown("<div class='card-warning'><b style='color:#FCD34D;'>35 km · Decay Threshold</b><br><span style='font-size:12px;color:rgba(255,255,255,0.5);'>GAM inflection — mobile clinic boundary.</span></div>", unsafe_allow_html=True)
        g3.markdown("<div class='card-danger'><b style='color:#F87171;'>&gt;35 km · Declining Zone</b><br><span style='font-size:12px;color:rgba(255,255,255,0.5);'>Access declines to 84.0% at 50 km.</span></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 7 — ALERTS
# ══════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;'>
      <div>
        <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Alerts</div>
        <div style='font-size:13px;color:rgba(255,255,255,0.45);'>Emergency contacts, high-risk flags and urgent outreach actions</div>
        </div><span style='background:rgba(226,75,74,0.2);color:#F87171;font-size:12px;font-weight:700;padding:7px 14px;border-radius:6px;'>
          {sum(1 for a in ALERTS_DATA if a["sev"]=="critical")} Critical
      </span>
    </div>""".format(sum=sum, ALERTS_DATA=ALERTS_DATA), unsafe_allow_html=True)

    for alert in ALERTS_DATA:
        if alert["sev"]=="critical":
            card="card-danger"; icon="🚨"; badge="CRITICAL"; bc="#F87171"; bbg="rgba(226,75,74,0.2)"
        else:
            card="card-warning"; icon="⚠️"; badge="WARNING"; bc="#FCD34D"; bbg="rgba(245,158,11,0.2)"

        st.markdown(f"""
        <div class='{card}'>
          <div style='display:flex;align-items:flex-start;gap:14px;'>
            <div style='font-size:24px;flex-shrink:0;margin-top:2px;'>{icon}</div>
            <div style='flex:1;'>
              <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div style='font-size:14px;font-weight:700;color:white;'>
                  Emergency: {alert["name"]} — {alert["id"]}</div>
                <div style='background:{bbg};color:{bc};font-size:10px;font-weight:700;padding:3px 8px;border-radius:20px;'>{badge}</div>
              </div>
              <div style='font-size:12px;color:rgba(255,255,255,0.5);margin-top:2px;'>{alert["sub"]} · {alert["cond"]}</div>
              <div style='font-size:13px;color:rgba(255,255,255,0.75);margin-top:7px;line-height:1.5;'>{alert["msg"]}</div>
              {f"<div style='display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.04);border-radius:8px;padding:10px 14px;margin-top:10px;'><span style='font-size:20px;'>📞</span><div><div style='font-size:11px;color:rgba(255,255,255,0.35);'>Emergency Contact</div><div style='font-size:13px;font-weight:600;color:white;'>{alert['ec']} · {alert['rel']}</div></div><div style='margin-left:auto;font-size:14px;font-weight:700;color:#F87171;'>{alert['phone']}</div></div>" if alert["phone"] else ""}
              <div style='font-size:11px;color:rgba(255,255,255,0.25);margin-top:8px;'>{alert["time"]}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        if alert["phone"]:
            ac1,ac2,_ = st.columns([1,1,4])
            with ac1:
                if st.button(f"📞 Call", key=f"call_{alert['id']}"):
                    st.info(f"📞 Initiating call to {alert['phone']}")
            with ac2:
                if st.button("✅ Acknowledge", key=f"ack_{alert['id']}"):
                    st.success("Alert acknowledged.")

# ══════════════════════════════════════════════════════════════
# TAB 8 — SETTINGS
# ══════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown("""
    <div style='margin-bottom:20px;'>
      <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;color:white;'>Settings</div>
      <div style='font-size:13px;color:rgba(255,255,255,0.45);'>Coverage area, alert thresholds and export preferences</div>
    </div>""", unsafe_allow_html=True)

    sc1,sc2 = st.columns(2)
    with sc1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Coverage Area</div>", unsafe_allow_html=True)
        st.text_input("County", value="Nakuru")
        st.text_input("Sub-counties", value="All")
        st.number_input("Distance threshold (km)", value=35, min_value=5, max_value=100)
        st.markdown("</div>", unsafe_allow_html=True)

    with sc2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Alert Thresholds</div>", unsafe_allow_html=True)
        st.slider("High-risk flag (score above)", 0.0, 1.0, 0.75)
        st.selectbox("Export format", ["CSV","Excel","JSON"])
        st.toggle("Email alerts", value=True)
        st.toggle("SMS emergency contact alerts", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 Save changes"):
        st.success("Settings saved successfully.")

    st.markdown("---")
    st.markdown(f"""
    <div class='card-teal'>
      <div style='font-size:12px;font-weight:700;color:#5DCAA5;margin-bottom:8px;'>HealthLink Kenya — System Information</div>
      <div style='font-size:12px;color:rgba(255,255,255,0.5);line-height:2.2;'>
        <b style='color:rgba(255,255,255,0.7);'>FastAPI Backend:</b> {API}<br>
        <b style='color:rgba(255,255,255,0.7);'>Access Model:</b> XGBoost (Tuned) · F1: 0.8091 · AUC: 0.8144<br>
        <b style='color:rgba(255,255,255,0.7);'>Retention Model:</b> XGBoost Stage 2 (SMOTE) · AUC: 0.8292 · Recall: 53.4%<br>
        <b style='color:rgba(255,255,255,0.7);'>Dataset:</b> KNBS HSB Survey 2022 · n = 99,031<br>
        <b style='color:rgba(255,255,255,0.7);'>Author:</b> Rutendo Julia Kandeya · ID: 168332 · Strathmore University · 2026<br>
        <b style='color:rgba(255,255,255,0.7);'>Supervisor:</b> Dr. Esther Khakata
      </div>
    </div>""", unsafe_allow_html=True)

    if st.button("← Sign Out"):
        st.session_state.auth = False
        st.session_state.user = {}
        st.rerun()
      
