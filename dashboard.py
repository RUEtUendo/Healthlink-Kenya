"""
HealthLink Kenya — Social Worker Operations Dashboard
Rutendo Julia Kandeya · Strathmore University · 2026
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import joblib
import requests
import os
import math
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="HealthLink Kenya",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Sora:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0A1929 !important; color: #e2e8f0; }
.stApp { background-color: #0A1929 !important; }
section[data-testid="stSidebar"] { display: none !important; }
button[kind="header"] { display: none !important; }
h1,h2,h3 { font-family: 'Sora', sans-serif !important; color: white !important; }
.stButton > button { background: linear-gradient(135deg, #1D9E75, #0F6E56) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }
.stButton > button[kind="secondary"] { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.12) !important; }
div[data-testid="metric-container"] { background: #0C2340 !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 12px !important; padding: 16px !important; }
div[data-testid="metric-container"] label { color: rgba(255,255,255,0.4) !important; font-size:11px !important; text-transform:uppercase; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: white !important; font-family: 'Sora', sans-serif !important; font-size:26px !important; font-weight:700 !important; }
.stSelectbox > div > div, .stTextInput > div > div > input { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.12) !important; color: white !important; border-radius: 8px !important; }
.stRadio label { color: rgba(255,255,255,0.7) !important; }
p, span, div, label { color: rgba(255,255,255,0.8); }
hr { border-color: rgba(255,255,255,0.08) !important; }
.hl-card { background: #0C2340; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 12px; }
.hl-card-teal { background: rgba(29,158,117,0.08); border: 1px solid rgba(29,158,117,0.25); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.hl-card-danger { background: rgba(226,75,74,0.08); border-left: 4px solid #F87171; border-radius: 12px; padding: 18px 20px; margin-bottom: 12px; }
.hl-card-warning { background: rgba(245,158,11,0.08); border-left: 4px solid #FCD34D; border-radius: 12px; padding: 18px 20px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── MODELS ────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    base = os.path.dirname(os.path.abspath(__file__))
    for a,r in [("health_access_pipeline.pkl","retention_pipeline.pkl"),
                (os.path.join(base,"health_access_pipeline.pkl"), os.path.join(base,"retention_pipeline.pkl"))]:
        try:
            if os.path.exists(a) and os.path.exists(r):
                return joblib.load(a), joblib.load(r), True
        except: pass
    return None, None, False

access_model, retention_model, models_ok = load_models()

def predict_access(dist, age, gender, wealth, insured, residence):
    if access_model is None: return 72.0
    try:
        df = pd.DataFrame([{"distance_from_facility":dist,"insurance_status":"Yes" if insured else "No",
            "education_level":"Secondary","age_group":age,"wealth_index1":wealth,"resid":residence,"gender":gender,"working_status":"Unknown"}])
        return round(float(access_model.predict_proba(df)[0][1])*100,1)
    except: return 72.0

def predict_retention(dist, age, gender, wealth, insured, residence):
    if retention_model is None: return 65.0
    try:
        df = pd.DataFrame([{"distance_from_facility":dist,"insurance_status":"Yes" if insured else "No",
            "education_level":"Secondary","age_group":age,"wealth_index1":wealth,"resid":residence,"gender":gender,"working_status":"Unknown"}])
        return round(float(retention_model.predict_proba(df)[0][1])*100,1)
    except: return 65.0

API_BASE = "https://healthlink-kenya-production.up.railway.app"

def get_patients(page=1, risk=None, sub=None, search=None):
    try:
        params = {"page":page,"page_size":10}
        if risk: params["risk"]=risk
        if sub: params["sub_county"]=sub
        if search: params["search"]=search
        r = requests.get(f"{API_BASE}/patients/", params=params, timeout=5)
        if r.status_code==200: return r.json()
    except: pass
    return None

def get_stats():
    try:
        r = requests.get(f"{API_BASE}/analytics/dashboard/stats", timeout=5)
        if r.status_code==200: return r.json()
    except: pass
    return {"total":30,"high_risk":9,"medium_risk":11,"coverage_rate":70.0}

def haversine(lat1,lng1,lat2,lng2):
    R=6371; dlat=math.radians(lat2-lat1); dlng=math.radians(lng2-lng1)
    a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

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
]

HOUSEHOLDS = [
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

ALERTS = [
    {"id":"HH-NK-00234","name":"Rutendo Nyamari","sub":"Bahati","cond":"Hypertension","type":"critical","msg":"Reported chest pain. Missed follow-up 5 Apr 2026.","ec_name":"James Nyamari","ec_rel":"Spouse","ec_phone":"+254 712 445 678","time":"Today 08:14 AM"},
    {"id":"HH-NK-00312","name":"Grace Wambui","sub":"Molo","cond":"Hypertension","type":"critical","msg":"New registration. Risk score 0.91. Distance 52.3km. No insurance.","ec_name":"Grace Wanjiku","ec_rel":"Mother","ec_phone":"+254 728 990 112","time":"Today 09:32 AM"},
    {"id":"HH-NK-00891","name":"Joseph Mwangi","sub":"Njoro","cond":"Diabetes T2","type":"critical","msg":"Missed 2 consecutive follow-ups. Last contact 15 Feb 2026.","ec_name":"Peter Kamau","ec_rel":"Brother","ec_phone":"+254 700 334 891","time":"Yesterday 04:45 PM"},
    {"id":"HH-NK-00455","name":"Samuel Otieno","sub":"Subukia","cond":"TB Follow-up","type":"warning","msg":"Distance 36.7km exceeds 35km threshold.","ec_name":"","ec_rel":"","ec_phone":"","time":"2 days ago"},
]

USERS = {
    "amara@healthlink.ke":{"pw":"sw2026","name":"Amara Ochieng","role":"Social Worker","county":"Nakuru"},
    "admin@healthlink.ke":{"pw":"admin2026","name":"Supervisor Admin","role":"Supervisor","county":"Nakuru"},
    "doctor@healthlink.ke":{"pw":"Doctor2024!","name":"Dr. Wanjiku","role":"Clinician","county":"Nairobi"},
}

for k,v in [("auth",False),("user",{}),("page","Hub"),("db_page",1)]:
    if k not in st.session_state: st.session_state[k]=v

# ── LOGIN ─────────────────────────────────────────────────────
if not st.session_state.auth:
    _,col,_ = st.columns([1,1.2,1])
    with col:
        st.markdown("""<div style='text-align:center;padding:60px 0 32px;'>
          <div style='font-size:56px;'>🏥</div>
          <div style='font-family:Sora,sans-serif;font-size:30px;font-weight:700;color:white;margin-top:10px;'>
            Health<span style='color:#1D9E75;'>Link</span> Kenya</div>
          <div style='font-size:13px;color:rgba(255,255,255,0.4);margin-top:6px;'>Social Worker Console · Nakuru County</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='hl-card'>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font-size:36px;margin-bottom:16px;'>🧑‍💼</div>", unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="you@healthlink.ke")
        password = st.text_input("Password", type="password")
        if st.button("Sign In →", use_container_width=True):
            if email in USERS and USERS[email]["pw"]==password:
                st.session_state.auth=True; st.session_state.user=USERS[email]; st.rerun()
            else: st.error("Invalid credentials.")
        st.markdown("<div style='margin-top:12px;padding:10px;background:rgba(255,255,255,0.04);border-radius:8px;font-size:11px;color:rgba(255,255,255,0.4);line-height:2.0;'><b style='color:#5DCAA5;'>Demo:</b> amara@healthlink.ke · sw2026<br>admin@healthlink.ke · admin2026</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

user = st.session_state.user

# ── TOP BAR ───────────────────────────────────────────────────
st.markdown(f"""<div style='background:#0C2340;border-bottom:1px solid rgba(255,255,255,0.08);
  padding:12px 24px;display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;'>
  <div style='display:flex;align-items:center;gap:12px;'>
    <span style='font-size:22px;'>🏥</span>
    <span style='font-family:Sora,sans-serif;font-size:16px;font-weight:700;color:white;'>
      Health<span style='color:#5DCAA5;'>Link</span> Kenya</span>
    <span style='font-size:11px;color:rgba(255,255,255,0.3);'>Nakuru County</span>
  </div>
  <div style='font-size:12px;color:#5DCAA5;font-weight:600;'>
    👤 {user.get("name","User")} · {user.get("role","")}</div>
</div>""", unsafe_allow_html=True)

# ── NAV TABS ──────────────────────────────────────────────────
PAGES = ["Hub","Geospatial","Mobile Clinic","Triage","Patient DB","Reports","Alerts","Settings"]
nav_cols = st.columns(len(PAGES)+1)
for i,p in enumerate(PAGES):
    with nav_cols[i]:
        is_active = st.session_state.page==p
        if st.button(p, key=f"nav_{p}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.page=p; st.rerun()
with nav_cols[-1]:
    if st.button("↩ Out", use_container_width=True, type="secondary"):
        st.session_state.auth=False; st.rerun()

st.markdown(f"{'<div style=background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:6px;padding:5px 12px;font-size:11px;color:#6EE7B7;display:inline-block;margin:8px 0 16px;>✅ ML Models active</div>' if models_ok else '<div style=background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:6px;padding:5px 12px;font-size:11px;color:#FCD34D;display:inline-block;margin:8px 0 16px;>⚠️ Fallback mode</div>'}", unsafe_allow_html=True)
st.markdown("---")
page = st.session_state.page

# ══════════════════════════════════════════════════════════════
if page=="Hub":
    st.markdown("<h2>Outreach Hub</h2>", unsafe_allow_html=True)
    stats=get_stats()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total Patients",stats.get("total",30))
    c2.metric("High Risk",stats.get("high_risk",9),delta_color="inverse")
    c3.metric("Medium Risk",stats.get("medium_risk",11))
    c4.metric("Coverage Rate",f"{stats.get('coverage_rate',70)}%","+2pts")
    st.markdown("---")
    st.markdown("<h3>Quick Access</h3>", unsafe_allow_html=True)
    items=[("🗺️","Geospatial","Risk zones & facilities"),("👥","Triage","XGBoost predictions"),
           ("🚐","Mobile Clinic","Field routing map"),("🗄️","Patient DB","Live from FastAPI"),
           ("📊","Reports","SHAP & GAM charts"),("🔔","Alerts","Emergency contacts"),
           ("⚙️","Settings","Thresholds & config"),("📍","Reports","Distance decay")]
    cols=st.columns(4)
    for i,(icon,label,desc) in enumerate(items):
        with cols[i%4]:
            target = label if label in PAGES else "Reports"
            st.markdown(f"""<div class='hl-card' style='text-align:center;padding:18px 10px;'>
              <div style='font-size:26px;margin-bottom:6px;'>{icon}</div>
              <div style='font-family:Sora,sans-serif;font-size:13px;font-weight:600;color:white;'>{label}</div>
              <div style='font-size:11px;color:rgba(255,255,255,0.35);margin-top:3px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open", key=f"hub_{i}", use_container_width=True):
                st.session_state.page=target; st.rerun()
    st.markdown("---")
    st.markdown("<h3>🔔 Active Alerts</h3>", unsafe_allow_html=True)
    for a in ALERTS[:2]:
        st.markdown(f"""<div class='hl-card-danger'>
          <b style='color:white;'>{a["name"]} — {a["id"]}</b>
          <div style='font-size:12px;color:rgba(255,255,255,0.5);'>{a["sub"]} · {a["cond"]}</div>
          <div style='font-size:12px;color:rgba(255,255,255,0.7);margin-top:4px;'>{a["msg"]}</div>
        </div>""", unsafe_allow_html=True)

elif page=="Geospatial":
    st.markdown("<h2>Geospatial Mapper</h2>", unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    show_hh=c1.checkbox("Households",value=True)
    show_risk=c2.checkbox("Risk Zones",value=True)
    decay_km=c3.slider("Decay (km)",10,60,35)
    m=folium.Map(location=[-0.310,36.080],zoom_start=9,tiles="CartoDB dark_matter")
    for f in FACILITIES:
        color="#1D9E75" if f["type"]=="hospital" else "#185FA5" if f["type"]=="clinic" else "#8B5CF6"
        folium.CircleMarker([f["lat"],f["lng"]],radius=7,color="white",weight=1.5,fill=True,fill_color=color,fill_opacity=0.9,tooltip=f["name"]).add_to(m)
    if show_hh:
        for hh in HOUSEHOLDS:
            rc="#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            folium.CircleMarker([hh["lat"],hh["lng"]],radius=8,color="white",weight=2,fill=True,fill_color=rc,fill_opacity=0.9,
                tooltip=f"{hh['id']} · {hh['risk']}",popup=folium.Popup(f"<b>{hh['id']}</b><br>{hh['name']}<br>{hh['cond']}<br>{hh['dist']}km",max_width=180)).add_to(m)
    if show_risk:
        for z in [{"lat":-0.17,"lng":36.12,"r":8000,"c":"#E24B4A","l":"Bahati High-Risk"},
                  {"lat":-0.42,"lng":35.70,"r":12000,"c":"#E24B4A","l":"Kuresoi High-Risk"},
                  {"lat":0.04,"lng":36.22,"r":7000,"c":"#F59E0B","l":"Subukia Medium"}]:
            folium.Circle([z["lat"],z["lng"]],radius=z["r"],color=z["c"],fill=True,fill_color=z["c"],fill_opacity=0.12,weight=1.5,tooltip=z["l"]).add_to(m)
    folium.Circle([-0.293,36.076],radius=decay_km*1000,color="#F59E0B",fill=False,weight=2,dash_array="8 6",tooltip=f"{decay_km}km threshold").add_to(m)
    map_data=st_folium(m,width="100%",height=500,returned_objects=["last_clicked"])
    s1,s2,s3=st.columns(3)
    s1.metric("Facilities",len(FACILITIES)); s2.metric("Households",len(HOUSEHOLDS) if show_hh else 0); s3.metric("Threshold",f"{decay_km}km")
    if map_data and map_data.get("last_clicked"):
        clat=map_data["last_clicked"]["lat"]; clng=map_data["last_clicked"]["lng"]
        nearest=sorted(FACILITIES,key=lambda f:haversine(clat,clng,f["lat"],f["lng"]))[:3]
        st.markdown(f"<div class='hl-card-teal'><b style='color:#5DCAA5;'>📍 ({clat:.4f}, {clng:.4f})</b></div>",unsafe_allow_html=True)
        for f in nearest:
            d=haversine(clat,clng,f["lat"],f["lng"]); c="#6EE7B7" if d<=decay_km else "#F87171"
            st.markdown(f"<div class='hl-card'><b style='color:white;'>{f['name']}</b><span style='color:{c};float:right;font-weight:700;'>{d:.1f}km</span></div>",unsafe_allow_html=True)

elif page=="Mobile Clinic":
    st.markdown("<h2>Mobile Clinic Routing</h2>", unsafe_allow_html=True)
    rf=st.radio("Filter",["All","High","Medium","Low"],horizontal=True)
    filtered=[h for h in HOUSEHOLDS if rf=="All" or h["risk"]==rf]
    cl,cm=st.columns([1,2])
    with cl:
        st.markdown(f"<div style='font-size:11px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:8px;'>{len(filtered)} Households</div>",unsafe_allow_html=True)
        for hh in filtered:
            rc="#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            ca,cb=st.columns([3,1])
            with ca:
                st.markdown(f"""<div class='hl-card' style='padding:10px;margin-bottom:4px;'>
                  <div style='font-size:11px;font-weight:700;color:{rc};font-family:monospace;'>{hh["id"]}</div>
                  <div style='font-size:11px;color:rgba(255,255,255,0.5);'>{hh["name"]} · {hh["sub"]}</div>
                  <div style='font-size:10px;color:rgba(255,255,255,0.3);'>{hh["dist"]}km · {hh["cond"]}</div>
                </div>""",unsafe_allow_html=True)
            with cb:
                if st.button("→",key=f"sel_{hh['id']}"):
                    st.session_state["sel_hh"]=hh
    with cm:
        sel=st.session_state.get("sel_hh",filtered[0] if filtered else None)
        m2=folium.Map(location=[sel["lat"],sel["lng"]] if sel else [-0.310,36.080],zoom_start=11,tiles="CartoDB dark_matter")
        for f in FACILITIES:
            c="#1D9E75" if f["type"]=="hospital" else "#185FA5" if f["type"]=="clinic" else "#8B5CF6"
            folium.CircleMarker([f["lat"],f["lng"]],radius=6,color="white",weight=1.5,fill=True,fill_color=c,fill_opacity=0.85,tooltip=f["name"]).add_to(m2)
        for hh in filtered:
            rc="#F87171" if hh["risk"]=="High" else "#FCD34D" if hh["risk"]=="Medium" else "#6EE7B7"
            is_sel=sel and hh["id"]==sel["id"]
            folium.CircleMarker([hh["lat"],hh["lng"]],radius=10 if is_sel else 7,color="white",weight=3 if is_sel else 1.5,fill=True,fill_color=rc,fill_opacity=0.95 if is_sel else 0.8,tooltip=hh["id"]).add_to(m2)
        if sel:
            nf=sorted(FACILITIES,key=lambda f:haversine(sel["lat"],sel["lng"],f["lat"],f["lng"]))[0]
            folium.PolyLine([[sel["lat"],sel["lng"]],[nf["lat"],nf["lng"]]],color="#F59E0B",weight=2.5,dash_array="8 5").add_to(m2)
        st_folium(m2,width="100%",height=480)
    if sel:
        nfacs=sorted(FACILITIES,key=lambda f:haversine(sel["lat"],sel["lng"],f["lat"],f["lng"]))[:3]
        rc="#F87171" if sel["risk"]=="High" else "#FCD34D" if sel["risk"]=="Medium" else "#6EE7B7"
        st.markdown(f"""<div class='hl-card'><b style='color:white;font-size:15px;'>{sel["id"]} — {sel["name"]}</b>
          <span style='color:{rc};float:right;'>{sel["risk"]}</span><br>
          <span style='font-size:12px;color:rgba(255,255,255,0.5);'>{sel["sub"]} · {sel["cond"]} · {sel["ins"]}</span>
          <div style='display:flex;gap:8px;margin-top:10px;'>
            {"".join([f'<div style="flex:1;background:#0F2847;border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:8px;"><div style="font-size:11px;font-weight:600;color:white;">{f["name"]}</div><div style="font-size:10px;color:rgba(255,255,255,0.35);">{haversine(sel["lat"],sel["lng"],f["lat"],f["lng"]):.1f}km</div></div>' for f in nfacs])}
          </div></div>""",unsafe_allow_html=True)

elif page=="Triage":
    st.markdown("<h2>Predictive Triage</h2>", unsafe_allow_html=True)
    cf,cr=st.columns([1,1])
    with cf:
        st.markdown("<div class='hl-card'>",unsafe_allow_html=True)
        st.markdown("<b style='color:white;font-size:14px;'>Patient Profile</b>",unsafe_allow_html=True)
        age=st.selectbox("Age Group",["0-4","5-14","15-24","25-34","35-49","50-64","65+"])
        gender=st.selectbox("Gender",["Female","Male"])
        residence=st.radio("Residence",["Urban","Rural","Peri-Urban"],horizontal=True)
        wealth=st.select_slider("Wealth",options=["Poorest","Poorer","Middle","Richer","Richest"])
        insurance=st.radio("Insurance",["Insured","Uninsured"],horizontal=True)
        dist=st.slider("Distance (km)",0.0,100.0,5.0,0.5)
        if st.button("🔍 Run Prediction",use_container_width=True):
            acc=predict_access(dist,age,gender,wealth,insurance=="Insured",residence)
            ret=predict_retention(dist,age,gender,wealth,insurance=="Insured",residence)
            st.session_state.last_pred={"acc":acc,"ret":ret,"dist":dist}
        st.markdown("</div>",unsafe_allow_html=True)
    with cr:
        if "last_pred" in st.session_state:
            p=st.session_state.last_pred; acc,ret,d=p["acc"],p["ret"],p["dist"]
            ac="#6EE7B7" if acc>=70 else "#FCD34D" if acc>=40 else "#F87171"
            rc="#6EE7B7" if ret>=70 else "#FCD34D" if ret>=40 else "#F87171"
            st.markdown(f"""<div class='hl-card'>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;'>
                <div style='text-align:center;background:#0F2847;border-radius:10px;padding:18px 8px;'>
                  <div style='font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;'>Access</div>
                  <div style='font-family:Sora,sans-serif;font-size:34px;font-weight:700;color:{ac};'>{acc}%</div>
                </div>
                <div style='text-align:center;background:#0F2847;border-radius:10px;padding:18px 8px;'>
                  <div style='font-size:10px;color:rgba(255,255,255,0.35);text-transform:uppercase;'>Retention</div>
                  <div style='font-family:Sora,sans-serif;font-size:34px;font-weight:700;color:{rc};'>{ret}%</div>
                </div>
              </div>
              <div style='font-size:13px;color:{"#6EE7B7" if d<=35 else "#F87171"};font-weight:600;margin-bottom:10px;'>
                {"🟢 Safe Zone ≤35km" if d<=35 else "🔴 Beyond 35km"} · {d}km
              </div>
            </div>""",unsafe_allow_html=True)
            if acc>=70: st.markdown("<div class='hl-card-teal'>✅ High access — standard outreach schedule.</div>",unsafe_allow_html=True)
            elif acc>=40: st.markdown("<div class='hl-card-warning'>⚡ Moderate — consider CHW visit.</div>",unsafe_allow_html=True)
            else: st.markdown("<div class='hl-card-danger'>🚨 Low — prioritise mobile clinic.</div>",unsafe_allow_html=True)
            fig=go.Figure(go.Bar(x=[acc,ret],y=["Access","Retention"],orientation="h",
                marker_color=[ac,rc],text=[f"{acc}%",f"{ret}%"],textposition="outside",textfont=dict(color="white",size=13)))
            fig.update_layout(paper_bgcolor="#0C2340",plot_bgcolor="#0C2340",height=130,
                margin=dict(l=10,r=60,t=10,b=10),showlegend=False,
                xaxis=dict(range=[0,115],showgrid=False,tickfont=dict(color="rgba(255,255,255,0.4)")),
                yaxis=dict(tickfont=dict(color="white",size=13)))
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.markdown("<div class='hl-card' style='text-align:center;padding:60px;'><div style='font-size:48px;'>🔍</div><div style='color:rgba(255,255,255,0.4);margin-top:12px;'>Run a prediction to see results</div></div>",unsafe_allow_html=True)

elif page=="Patient DB":
    st.markdown("<h2>Patient Database</h2>", unsafe_allow_html=True)
    sc1,sc2,sc3=st.columns([2,1,1])
    with sc1: search=st.text_input("🔍 Search...")
    with sc2: risk_f=st.selectbox("Risk",["","High","Medium","Low"])
    with sc3: sub_f=st.selectbox("Sub-county",["","Nakuru Town","Bahati","Njoro","Rongai","Subukia","Kuresoi","Molo","Gilgil","Naivasha"])
    data=get_patients(page=st.session_state.db_page,risk=risk_f or None,sub=sub_f or None,search=search or None)
    if data:
        total=data.get("total",0); patients=data.get("data",[])
        m1,m2,m3,m4=st.columns(4)
        m1.metric("Total",total)
        m2.metric("High Risk",sum(1 for p in patients if p.get("risk")=="High"))
        m3.metric("Medium Risk",sum(1 for p in patients if p.get("risk")=="Medium"))
        m4.metric("NHIF",sum(1 for p in patients if p.get("insurance")=="NHIF"))
        if patients:
            rows=[{"ID":p.get("id",""),"Name":p.get("name",""),"Age":p.get("age",""),
                "Sub-county":p.get("sub_county",""),"Condition":p.get("condition",""),
                "Risk":p.get("risk",""),"Dist(km)":p.get("distance_km",""),
                "Insurance":p.get("insurance",""),"Last Visit":p.get("last_visit") or "N/A"} for p in patients]
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True,height=400)
            total_pages=max(1,math.ceil(total/10))
            pc1,pc2,pc3=st.columns(3)
            with pc1:
                if st.button("← Prev",disabled=st.session_state.db_page<=1):
                    st.session_state.db_page-=1; st.rerun()
            with pc2:
                st.markdown(f"<div style='text-align:center;color:rgba(255,255,255,0.4);padding-top:8px;font-size:12px;'>Page {st.session_state.db_page} of {total_pages}</div>",unsafe_allow_html=True)
            with pc3:
                if st.button("Next →",disabled=st.session_state.db_page>=total_pages):
                    st.session_state.db_page+=1; st.rerun()
            if st.button("⬇️ Export CSV"):
                st.download_button("Download",pd.DataFrame(rows).to_csv(index=False),"patients.csv","text/csv")
    else:
        st.markdown("<div class='hl-card-warning'>⚠️ API offline — showing static fallback data</div>",unsafe_allow_html=True)
        fb=pd.DataFrame(HOUSEHOLDS)[["id","name","age","cond","risk","dist","ins","sub"]]
        fb.columns=["ID","Name","Age","Condition","Risk","Distance","Insurance","Sub-county"]
        st.dataframe(fb,use_container_width=True,hide_index=True)

elif page=="Reports":
    st.markdown("<h2>Reports & Analytics</h2>", unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["SHAP Analysis","Distance Decay","Model Performance"])
    with t1:
        st.markdown("<h3>TreeSHAP Feature Importance</h3>",unsafe_allow_html=True)
        shap_df=pd.DataFrame([{"f":"Education Level","v":73.2,"c":"Predisposing"},{"f":"Distance (km)","v":12.9,"c":"Enabling"},{"f":"Wealth Index","v":8.4,"c":"Enabling"},{"f":"Insurance","v":5.5,"c":"Enabling"}])
        fig=go.Figure(go.Bar(x=shap_df["v"],y=shap_df["f"],orientation="h",
            marker_color=["#6366F1" if c=="Predisposing" else "#F59E0B" for c in shap_df["c"]],
            text=[f"{v}%" for v in shap_df["v"]],textposition="outside",textfont=dict(color="white",size=13)))
        fig.update_layout(paper_bgcolor="#0C2340",plot_bgcolor="#0C2340",height=280,margin=dict(l=10,r=70,t=10,b=10),showlegend=False,
            xaxis=dict(range=[0,95],tickfont=dict(color="rgba(255,255,255,0.4)"),gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(tickfont=dict(color="white",size=13),autorange="reversed"))
        st.plotly_chart(fig,use_container_width=True)
        c1,c2,c3=st.columns(3)
        c1.markdown("<div class='hl-card-warning'><b style='color:#F59E0B;'>Enabling: 26.8%</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Distance + Wealth + Insurance</span></div>",unsafe_allow_html=True)
        c2.markdown("<div class='hl-card'><b style='color:#A78BFA;'>Predisposing: 73.2%</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Education dominates</span></div>",unsafe_allow_html=True)
        c3.markdown("<div class='hl-card-teal'><b style='color:#5DCAA5;'>Distance: 12.9%</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Strongest single feature</span></div>",unsafe_allow_html=True)
    with t2:
        GAM_D=[0,5,10,15,20,25,30,35,40,50,60]; GAM_P=[0.899,0.905,0.910,0.914,0.916,0.918,0.910,0.895,0.875,0.840,0.800]
        fig2=go.Figure()
        fig2.add_trace(go.Scatter(x=[d for d in GAM_D if d<=35]+[35],y=[p for d,p in zip(GAM_D,GAM_P) if d<=35]+[0.895],fill="tozeroy",fillcolor="rgba(16,185,129,0.08)",line=dict(color="rgba(0,0,0,0)"),showlegend=False))
        fig2.add_trace(go.Scatter(x=[d for d in GAM_D if d>=35],y=[p for d,p in zip(GAM_D,GAM_P) if d>=35],fill="tozeroy",fillcolor="rgba(239,68,68,0.07)",line=dict(color="rgba(0,0,0,0)"),showlegend=False))
        fig2.add_trace(go.Scatter(x=GAM_D,y=GAM_P,mode="lines+markers",line=dict(color="#1D9E75",width=3),marker=dict(size=7,color="#5DCAA5"),name="P(Access)"))
        fig2.add_vline(x=35,line_dash="dash",line_color="#F59E0B",line_width=2,annotation_text="35km threshold",annotation_font_color="#F59E0B")
        fig2.update_layout(paper_bgcolor="#0C2340",plot_bgcolor="#0C2340",height=360,
            xaxis=dict(title="Distance (km)",gridcolor="rgba(255,255,255,0.06)",tickfont=dict(color="rgba(255,255,255,0.5)")),
            yaxis=dict(title="Access Probability",tickformat=".0%",gridcolor="rgba(255,255,255,0.06)",tickfont=dict(color="rgba(255,255,255,0.5)")),
            margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig2,use_container_width=True)
        g1,g2,g3=st.columns(3)
        g1.markdown("<div class='hl-card-teal'><b style='color:#5DCAA5;'>0–35km · Stable</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>89–92% access</span></div>",unsafe_allow_html=True)
        g2.markdown("<div class='hl-card-warning'><b style='color:#FCD34D;'>35km · Inflection</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Mobile clinic boundary</span></div>",unsafe_allow_html=True)
        g3.markdown("<div class='hl-card-danger'><b style='color:#F87171;'>&gt;35km · Declining</b><br><span style='font-size:11px;color:rgba(255,255,255,0.5);'>Drops to 84% at 50km</span></div>",unsafe_allow_html=True)
    with t3:
        perf=pd.DataFrame([{"Algorithm":"XGBoost ✅","F1":0.8091,"AUC":0.8144,"Accuracy":0.7222},
            {"Algorithm":"Gradient Boosting","F1":0.9342,"AUC":0.5762,"Accuracy":0.8766},
            {"Algorithm":"AdaBoost","F1":0.9343,"AUC":0.5501,"Accuracy":0.8766},
            {"Algorithm":"Random Forest","F1":0.6573,"AUC":0.5932,"Accuracy":0.5282},
            {"Algorithm":"Logistic Regression","F1":0.6611,"AUC":0.6143,"Accuracy":0.5342}])
        fig3=go.Figure()
        for col,color in [("F1","#1D9E75"),("AUC","#185FA5"),("Accuracy","#6366F1")]:
            fig3.add_trace(go.Bar(name=col,x=perf["Algorithm"],y=perf[col],marker_color=color,opacity=0.85))
        fig3.update_layout(barmode="group",paper_bgcolor="#0C2340",plot_bgcolor="#0C2340",height=320,
            xaxis=dict(tickfont=dict(color="white"),tickangle=-20,gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(range=[0,1.05],gridcolor="rgba(255,255,255,0.06)",tickfont=dict(color="rgba(255,255,255,0.5)")),
            legend=dict(bgcolor="#0C2340"),margin=dict(l=10,r=10,t=10,b=80))
        st.plotly_chart(fig3,use_container_width=True)
        st.dataframe(perf,use_container_width=True,hide_index=True)

elif page=="Alerts":
    st.markdown("<h2>Alerts & Emergency Contacts</h2>", unsafe_allow_html=True)
    crit=sum(1 for a in ALERTS if a["type"]=="critical")
    st.markdown(f"<div style='background:rgba(226,75,74,0.15);color:#F87171;font-size:12px;font-weight:700;padding:7px 14px;border-radius:8px;display:inline-block;margin-bottom:16px;'>{crit} Critical</div>",unsafe_allow_html=True)
    for alert in ALERTS:
        card="hl-card-danger" if alert["type"]=="critical" else "hl-card-warning"
        icon="🚨" if alert["type"]=="critical" else "⚠️"
        bc="#F87171" if alert["type"]=="critical" else "#FCD34D"
        badge="CRITICAL" if alert["type"]=="critical" else "WARNING"
        st.markdown(f"""<div class='{card}'>
          <div style='display:flex;justify-content:space-between;'>
            <b style='color:white;'>{icon} {alert["name"]} — {alert["id"]}</b>
            <span style='color:{bc};font-size:10px;font-weight:700;'>{badge}</span>
          </div>
          <div style='font-size:12px;color:rgba(255,255,255,0.5);'>{alert["sub"]} · {alert["cond"]}</div>
          <div style='font-size:13px;color:rgba(255,255,255,0.75);margin-top:5px;'>{alert["msg"]}</div>
          {f'<div style="background:rgba(255,255,255,0.04);border-radius:6px;padding:8px;margin-top:8px;display:flex;justify-content:space-between;"><span style="color:white;font-size:12px;">{alert["ec_name"]} · {alert["ec_rel"]}</span><span style="color:#F87171;font-weight:700;">{alert["ec_phone"]}</span></div>' if alert["ec_phone"] else ""}
          <div style='font-size:11px;color:rgba(255,255,255,0.25);margin-top:6px;'>{alert["time"]}</div>
        </div>""",unsafe_allow_html=True)
        if alert["ec_phone"]:
            a1,a2,_=st.columns([1,1,4])
            with a1:
                if st.button(f"📞 Call",key=f"call_{alert['id']}"): st.info(f"Calling {alert['ec_phone']}")
            with a2:
                if st.button(f"✅ Ack",key=f"ack_{alert['id']}"): st.success("Acknowledged")

elif page=="Settings":
    st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown("<div class='hl-card'>",unsafe_allow_html=True)
        st.markdown("<b style='color:white;'>Coverage Area</b>",unsafe_allow_html=True)
        st.text_input("County",value="Nakuru")
        st.number_input("Distance threshold (km)",value=35,min_value=5,max_value=100)
        st.markdown("</div>",unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='hl-card'>",unsafe_allow_html=True)
        st.markdown("<b style='color:white;'>Alerts & Export</b>",unsafe_allow_html=True)
        st.slider("High-risk score threshold",0.0,1.0,0.75)
        st.selectbox("Export format",["CSV","Excel","JSON"])
        st.toggle("Email alerts",value=True)
        st.toggle("SMS alerts",value=True)
        st.markdown("</div>",unsafe_allow_html=True)
    if st.button("💾 Save"): st.success("Saved.")
    st.markdown(f"""<div class='hl-card-teal' style='margin-top:16px;'>
      <b style='color:#5DCAA5;'>System Info</b><br>
      <div style='font-size:12px;color:rgba(255,255,255,0.5);margin-top:8px;line-height:2.0;'>
        API: {API_BASE}<br>
        Access Model: XGBoost · F1: 0.8091 · AUC: 0.8144<br>
        Retention: SMOTE · AUC: 0.8292 · Recall: 53.4%<br>
        Rutendo Julia Kandeya · ID: 168332 · Strathmore University · 2026
      </div></div>""",unsafe_allow_html=True)
