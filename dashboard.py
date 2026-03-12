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
# SESSION STATE DEFAULTS
# ============================================================
if "authenticated"  not in st.session_state: st.session_state.authenticated  = False
if "user"           not in st.session_state: st.session_state.user           = {}
if "theme"          not in st.session_state: st.session_state.theme          = "light"
if "accent"         not in st.session_state: st.session_state.accent         = "#0B3D6E"
if "font_size"      not in st.session_state: st.session_state.font_size      = "Medium"
if "map_style"      not in st.session_state: st.session_state.map_style      = "CartoDB positron"
if "show_paradox"   not in st.session_state: st.session_state.show_paradox   = True
if "api_url"        not in st.session_state: st.session_state.api_url        = "http://127.0.0.1:8000"

# ============================================================
# DYNAMIC THEME (responds to settings)
# ============================================================
acc   = st.session_state.accent
is_dark = st.session_state.theme == "dark"
bg    = "#0D1117" if is_dark else "#F7F9FC"
sbg   = "#161B22" if is_dark else "#FFFFFF"
card  = "#1C2333" if is_dark else "#FFFFFF"
border= "#30363D" if is_dark else "#E2EAF4"
text  = "#E6EDF3" if is_dark else "#1A2B40"
muted = "#8B949E" if is_dark else "#6B84A0"
card_b= "#1A2D4A" if is_dark else "#EEF5FF"
card_g= "#1A3A2A" if is_dark else "#EDFBF5"
card_a= "#3A2D10" if is_dark else "#FFFBEE"
card_r= "#3A1A1A" if is_dark else "#FFF5F5"
bdr_b = "#2D5490" if is_dark else "#C2D8F5"
bdr_g = "#2D7A5A" if is_dark else "#A8E6D0"
bdr_a = "#7A5A20" if is_dark else "#FDDDA0"
bdr_r = "#7A2D2D" if is_dark else "#FBCACA"
metric_val = acc

fs_map = {"Small": "11px", "Medium": "13px", "Large": "15px"}
fs = fs_map.get(st.session_state.font_size, "13px")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; font-size: {fs}; }}

    .stApp {{ background-color: {bg}; color: {text}; }}
    section[data-testid="stSidebar"] {{
        background-color: {sbg};
        border-right: 1px solid {border};
        box-shadow: 2px 0 8px rgba(0,0,0,0.06);
    }}

    h1 {{ color: {acc} !important; font-weight: 800 !important; }}
    h2 {{ color: {acc} !important; font-weight: 700 !important; }}
    h3, h4 {{ color: {text} !important; font-weight: 600 !important; }}
    p, span, div {{ color: {text}; }}

    /* ── Metric cards — solid white/dark, vivid values ── */
    [data-testid="metric-container"] {{
        background: {card} !important;
        border: 1.5px solid {border} !important;
        border-radius: 14px !important;
        padding: 20px 22px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }}
    [data-testid="metric-container"] label {{
        color: {muted} !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700 !important;
    }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {acc} !important;
        font-size: 28px !important;
        font-weight: 900 !important;
    }}
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {{
        color: #16A34A !important;
        font-weight: 600 !important;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background: {acc} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 10px 28px !important;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        filter: brightness(1.15) !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.20) !important;
    }}

    /* ── Inputs ── */
    .stSelectbox label, .stSlider label, .stRadio label,
    .stTextArea label, .stSelectSlider label, .stTextInput label,
    .stNumberInput label {{
        color: {muted} !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .stTextInput input, .stSelectbox > div > div, .stTextArea textarea {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        color: {text} !important;
    }}

    /* ── Sidebar nav items ── */
    .stRadio > div {{ gap: 3px; }}
    .stRadio label {{
        padding: 10px 14px !important;
        border-radius: 10px !important;
        transition: background 0.15s;
        font-size: 13px !important;
        font-weight: 500;
        color: {text} !important;
    }}
    .stRadio label:hover {{ background: {'#21262D' if is_dark else '#F0F4FA'} !important; }}

    /* ── Cards ── */
    .med-card {{
        background: {card};
        border: 1.5px solid {border};
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }}
    .med-card-blue  {{ background:{card_b}; border:1.5px solid {bdr_b}; border-radius:14px; padding:16px 20px; margin-bottom:12px; }}
    .med-card-green {{ background:{card_g}; border:1.5px solid {bdr_g}; border-radius:14px; padding:16px 20px; margin-bottom:12px; }}
    .med-card-amber {{ background:{card_a}; border:1.5px solid {bdr_a}; border-radius:14px; padding:16px 20px; margin-bottom:12px; }}
    .med-card-red   {{ background:{card_r}; border:1.5px solid {bdr_r}; border-radius:14px; padding:16px 20px; margin-bottom:12px; }}

    /* ── Badges ── */
    .badge-green {{ background:#DCFCE7; color:#15803D; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }}
    .badge-amber {{ background:#FEF9C3; color:#A16207; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }}
    .badge-red   {{ background:#FEE2E2; color:#DC2626; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }}
    .badge-blue  {{ background:#DBEAFE; color:#1D4ED8; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }}
    .badge-grey  {{ background:#F1F5F9; color:#64748B; border-radius:99px; padding:3px 12px; font-size:11px; font-weight:700; }}

    /* ── Patient rows ── */
    .pt-row {{ display:flex; justify-content:space-between; align-items:center;
               padding:10px 0; border-bottom:1px solid {border}; font-size:13px; }}
    .pt-label {{ color:{muted}; font-weight:600; font-size:11px; text-transform:uppercase; letter-spacing:0.04em; }}
    .pt-value {{ color:{text}; font-weight:600; }}

    /* ── Login card ── */
    .login-card {{
        background: {card};
        border: 1.5px solid {border};
        border-radius: 18px;
        padding: 40px 44px;
        box-shadow: 0 6px 28px rgba(0,0,0,0.10);
        max-width: 440px;
        margin: 0 auto;
    }}

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {{ background: {'#21262D' if is_dark else '#F0F4FA'}; border-radius: 10px; padding: 4px; }}
    .stTabs [data-baseweb="tab"] {{ color: {muted}; border-radius: 7px; font-weight: 500; }}
    .stTabs [aria-selected="true"] {{
        color: {acc} !important;
        background: {card} !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.10);
        font-weight: 700;
    }}

    hr {{ border-color: {border}; margin: 16px 0; }}
    .stProgress > div > div {{ background-color: {acc} !important; }}
    .stAlert {{ border-radius: 10px; }}
    [data-testid="stDataFrame"] {{ border-radius: 10px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# AUTH
# ============================================================
DEMO_USERS = {
    "admin@healthlink.ke":   {"pw": hashlib.sha256("Admin2024!".encode()).hexdigest(),  "role": "Administrator", "name": "Dr. Admin"},
    "doctor@healthlink.ke":  {"pw": hashlib.sha256("Doctor2024!".encode()).hexdigest(), "role": "Clinician",     "name": "Dr. Wanjiku"},
    "nurse@healthlink.ke":   {"pw": hashlib.sha256("Nurse2024!".encode()).hexdigest(),  "role": "Nurse",         "name": "Sr. Auma"},
    "planner@healthlink.ke": {"pw": hashlib.sha256("Plan2024!".encode()).hexdigest(),   "role": "Health Planner","name": "Mr. Omondi"},
}

def do_logout():
    st.session_state.authenticated = False
    st.session_state.user = {}

# ── Login screen ──────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown(f"""
    <div style='text-align:center; padding:48px 0 24px 0;'>
        <div style='font-size:56px;'>⚕️</div>
        <div style='font-size:30px; font-weight:800; color:{acc}; margin-top:8px;'>HealthLink Kenya</div>
        <div style='font-size:14px; color:{muted}; margin-top:6px; font-weight:500;'>
            Clinical Decision-Support Platform · Hospital Referral System
        </div>
    </div>""", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.4, 1])
    with col_c:
        mode_tab = st.radio("", ["🔑  Sign In", "📝  Create Account"],
                            horizontal=True, label_visibility="collapsed")
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if "Sign In" in mode_tab:
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;margin-bottom:20px;color:{acc};'>Sign In to Your Account</h3>", unsafe_allow_html=True)
            email    = st.text_input("Email Address", placeholder="you@healthlink.ke")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            if st.button("Sign In", use_container_width=True):
                hashed = hashlib.sha256(password.encode()).hexdigest()
                if email in DEMO_USERS and DEMO_USERS[email]["pw"] == hashed:
                    st.session_state.authenticated = True
                    st.session_state.user = {"email": email, **DEMO_USERS[email]}
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: doctor@healthlink.ke / Doctor2024!")
            st.markdown(f"""
            <div style='margin-top:16px;padding:12px 14px;background:{'#21262D' if is_dark else '#F7F9FC'};
                        border-radius:8px;font-size:11px;color:{muted};line-height:2.0;'>
                <b style='color:{acc};'>Demo accounts:</b><br>
                doctor@healthlink.ke · <i>Doctor2024!</i><br>
                nurse@healthlink.ke · <i>Nurse2024!</i><br>
                planner@healthlink.ke · <i>Plan2024!</i>
            </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='login-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;margin-bottom:20px;color:{acc};'>Create an Account</h3>", unsafe_allow_html=True)
            new_name     = st.text_input("Full Name", placeholder="Dr. Jane Njoroge")
            new_email    = st.text_input("Institutional Email", placeholder="you@hospital.ke")
            new_role     = st.selectbox("Role", ["Clinician","Nurse","Health Planner","Administrator","Research Officer"])
            new_facility = st.text_input("Facility / Organisation", placeholder="Kenyatta National Hospital")
            new_pw       = st.text_input("Password", type="password", placeholder="Create a strong password")
            new_pw2      = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            if st.button("Create Account", use_container_width=True):
                if not all([new_name, new_email, new_pw]):
                    st.warning("Please fill in all required fields.")
                elif new_pw != new_pw2:
                    st.error("Passwords do not match.")
                elif len(new_pw) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    st.success(f"✅ Account created for {new_name}. Please sign in.")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# DATA
# ============================================================
FACILITIES_DATA = pd.DataFrame([
    {"Name":"Kenyatta National Hospital",   "Type":"National Referral Hospital",    "Specialties":"Oncology, Cardiology, Neurology, Trauma, Burns, Transplant",         "Dist_km":0,    "Insurance_pct":91,"Wealth":"Highest","Access_pct":94,"Retention_pct":89,"Lat":-1.3006,"Lon":36.8066,"Paradox":False,"Beds":1800},
    {"Name":"Pumwani Maternity Hospital",   "Type":"County Hospital",               "Specialties":"Maternity, Neonatal ICU, Gynaecology",                               "Dist_km":4.2,  "Insurance_pct":62,"Wealth":"Middle", "Access_pct":81,"Retention_pct":74,"Lat":-1.2841,"Lon":36.8458,"Paradox":False,"Beds":320},
    {"Name":"Mathare North HC",             "Type":"Health Centre",                 "Specialties":"General OPD, Maternal Health, Immunisation",                         "Dist_km":6.8,  "Insurance_pct":31,"Wealth":"Lowest", "Access_pct":48,"Retention_pct":44,"Lat":-1.2611,"Lon":36.8590,"Paradox":True, "Beds":40},
    {"Name":"Mbagathi District Hospital",   "Type":"County Hospital",               "Specialties":"General Surgery, Infectious Disease, Psychiatry, Paediatrics",        "Dist_km":8.1,  "Insurance_pct":55,"Wealth":"Middle", "Access_pct":77,"Retention_pct":71,"Lat":-1.3217,"Lon":36.7680,"Paradox":False,"Beds":260},
    {"Name":"Kayole Sub-County Hospital",   "Type":"Sub-County Hospital",           "Specialties":"Emergency, Maternity, General OPD, Eye Clinic",                      "Dist_km":12.4, "Insurance_pct":28,"Wealth":"Second", "Access_pct":43,"Retention_pct":38,"Lat":-1.2718,"Lon":36.9001,"Paradox":True, "Beds":120},
    {"Name":"Ruaraka Health Centre",        "Type":"Clinic",                        "Specialties":"General OPD, Family Planning, HIV/ART",                              "Dist_km":15.0, "Insurance_pct":44,"Wealth":"Middle", "Access_pct":65,"Retention_pct":59,"Lat":-1.2488,"Lon":36.8756,"Paradox":False,"Beds":20},
    {"Name":"Dandora Dispensary",           "Type":"Dispensary",                    "Specialties":"Basic Primary Care, Immunisation, Wound Care",                       "Dist_km":18.3, "Insurance_pct":19,"Wealth":"Lowest", "Access_pct":37,"Retention_pct":30,"Lat":-1.2595,"Lon":36.9087,"Paradox":True, "Beds":10},
    {"Name":"Kangemi Health Centre",        "Type":"Health Centre",                 "Specialties":"General OPD, Maternal Health, TB/DOTS, Dental",                      "Dist_km":21.1, "Insurance_pct":33,"Wealth":"Second", "Access_pct":55,"Retention_pct":48,"Lat":-1.2724,"Lon":36.7369,"Paradox":False,"Beds":35},
    {"Name":"Nairobi West Hospital",        "Type":"Religious / Mission Hospital",  "Specialties":"Oncology, Orthopaedics, Cardiology, Dialysis, ICU",                  "Dist_km":9.5,  "Insurance_pct":74,"Wealth":"Fourth", "Access_pct":82,"Retention_pct":76,"Lat":-1.3146,"Lon":36.8100,"Paradox":False,"Beds":200},
    {"Name":"Aga Khan University Hospital", "Type":"Private Hospital",              "Specialties":"Neurosurgery, Oncology, Cardiology, Transplant, MRI/CT",             "Dist_km":3.1,  "Insurance_pct":96,"Wealth":"Highest","Access_pct":91,"Retention_pct":88,"Lat":-1.2702,"Lon":36.8074,"Paradox":False,"Beds":250},
    {"Name":"Limuru Sub-County Hospital",   "Type":"Sub-County Hospital",           "Specialties":"General Surgery, Maternity, Emergency",                              "Dist_km":31.7, "Insurance_pct":47,"Wealth":"Middle", "Access_pct":31,"Retention_pct":26,"Lat":-1.1140,"Lon":36.6480,"Paradox":False,"Beds":80},
    {"Name":"Thika Level 5 Hospital",       "Type":"County Referral Hospital",      "Specialties":"Oncology, Dialysis, Orthopaedics, ICU, Cardiology",                  "Dist_km":44.2, "Insurance_pct":52,"Wealth":"Fourth", "Access_pct":24,"Retention_pct":20,"Lat":-1.0332,"Lon":37.0693,"Paradox":False,"Beds":350},
    {"Name":"Meds Chemist Westlands",       "Type":"Pharmacy / Chemist",            "Specialties":"Pharmaceutical dispensing, OTC medications, Lab services",           "Dist_km":5.2,  "Insurance_pct":55,"Wealth":"Fourth", "Access_pct":88,"Retention_pct":72,"Lat":-1.2633,"Lon":36.8036,"Paradox":False,"Beds":0},
    {"Name":"St Francis Community Clinic",  "Type":"Religious / Mission Clinic",    "Specialties":"General OPD, HIV/ART, Nutrition, TB/DOTS",                           "Dist_km":14.0, "Insurance_pct":22,"Wealth":"Lowest", "Access_pct":58,"Retention_pct":50,"Lat":-1.2800,"Lon":36.8700,"Paradox":False,"Beds":15},
])

MODEL_PERF = pd.DataFrame([
    {"Algorithm":"XGBoost (Optimised)", "F1":0.9034,"AUC":0.6524,"Accuracy":0.8240,"Operational":True },
    {"Algorithm":"Gradient Boosting",   "F1":0.9034,"AUC":0.6463,"Accuracy":0.8239,"Operational":False},
    {"Algorithm":"AdaBoost",            "F1":0.9034,"AUC":0.6397,"Accuracy":0.8238,"Operational":False},
    {"Algorithm":"Ensemble (Top 3)",    "F1":0.9034,"AUC":0.6510,"Accuracy":0.8238,"Operational":False},
    {"Algorithm":"Decision Tree",       "F1":0.7584,"AUC":0.6445,"Accuracy":0.6496,"Operational":False},
    {"Algorithm":"Random Forest",       "F1":0.7509,"AUC":0.6528,"Accuracy":0.6422,"Operational":False},
    {"Algorithm":"Logistic Regression", "F1":0.5152,"AUC":0.5248,"Accuracy":0.4281,"Operational":False},
])

SHAP_DATA = pd.DataFrame([
    {"Feature":"Distance (km)",    "Importance":0.41,"Category":"Enabling"},
    {"Feature":"Wealth Index",     "Importance":0.18,"Category":"Enabling"},
    {"Feature":"Insurance Status", "Importance":0.14,"Category":"Enabling"},
    {"Feature":"Residence Type",   "Importance":0.09,"Category":"Predisposing"},
    {"Feature":"Education Level",  "Importance":0.08,"Category":"Predisposing"},
    {"Feature":"Age Group",        "Importance":0.05,"Category":"Predisposing"},
    {"Feature":"Gender",           "Importance":0.03,"Category":"Predisposing"},
    {"Feature":"Provider Type",    "Importance":0.02,"Category":"Need"},
])

GAM_DIST = [0,5,10,15,20,25,30,35,40,50,60,80,100]
GAM_PROB = [0.96,0.94,0.91,0.88,0.84,0.76,0.58,0.40,0.27,0.14,0.08,0.04,0.02]

FOLIUM_COLORS = {
    "National Referral Hospital":   "darkblue",
    "County Referral Hospital":     "blue",
    "County Hospital":              "cadetblue",
    "Sub-County Hospital":          "darkgreen",
    "Health Centre":                "green",
    "Clinic":                       "lightgreen",
    "Dispensary":                   "orange",
    "Pharmacy / Chemist":           "purple",
    "Religious / Mission Hospital": "red",
    "Religious / Mission Clinic":   "pink",
    "Private Hospital":             "darkpurple",
}
LEGEND_COLORS = {
    "National Referral Hospital":   "#1D4ED8",
    "County Referral Hospital":     "#2563EB",
    "County Hospital":              "#0891B2",
    "Sub-County Hospital":          "#0D9488",
    "Health Centre":                "#059669",
    "Clinic":                       "#65A30D",
    "Dispensary":                   "#CA8A04",
    "Pharmacy / Chemist":           "#9333EA",
    "Religious / Mission Hospital": "#E11D48",
    "Religious / Mission Clinic":   "#F43F5E",
    "Private Hospital":             "#7C3AED",
}

ALL_SPECIALTIES = sorted(set(
    s.strip() for row in FACILITIES_DATA["Specialties"] for s in row.split(",")
))

def make_facility_map(filtered_df, show_ring=True, tiles=None):
    tile = tiles or st.session_state.map_style
    m = folium.Map(location=[-1.2921, 36.8219], zoom_start=11, tiles=tile)
    if show_ring:
        folium.Circle(
            location=[-1.3006, 36.8066], radius=25000,
            color="#1D4ED8", weight=2, fill=True,
            fill_color="#1D4ED8", fill_opacity=0.05,
            tooltip="25km GAM Critical Threshold"
        ).add_to(m)
    for _, row in filtered_df.iterrows():
        f_color = "red" if (row["Paradox"] and st.session_state.show_paradox) else FOLIUM_COLORS.get(row["Type"], "gray")
        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            tooltip=f"{row['Name']} · {row['Type']}",
            popup=folium.Popup(
                f"""<div style='font-family:sans-serif;font-size:12px;min-width:200px;'>
                <b style='color:#0B3D6E;font-size:13px;'>{row['Name']}</b><br>
                <span style='color:#6B84A0;'>{row['Type']}</span><br><br>
                <b>Specialties:</b> {row['Specialties']}<br><br>
                <table style='width:100%;font-size:11px;'>
                  <tr><td style='color:#6B84A0;'>Distance:</td><td><b>{row['Dist_km']} km</b></td></tr>
                  <tr><td style='color:#6B84A0;'>Access Rate:</td><td><b>{row['Access_pct']}%</b></td></tr>
                  <tr><td style='color:#6B84A0;'>Retention Rate:</td><td><b>{row['Retention_pct']}%</b></td></tr>
                  <tr><td style='color:#6B84A0;'>Insurance:</td><td><b>{row['Insurance_pct']}%</b></td></tr>
                  {'<tr><td colspan=2 style="color:red;font-weight:bold;">⚠ Urban Proximity Paradox</td></tr>' if row['Paradox'] else ''}
                </table></div>""",
                max_width=260
            ),
            icon=folium.Icon(color=f_color, icon="plus-sign", prefix="glyphicon")
        ).add_to(m)
    return m

# ============================================================
# SIDEBAR
# ============================================================
user = st.session_state.user
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:20px 0 14px 0;'>
        <div style='font-size:42px;'>⚕️</div>
        <div style='font-size:17px;font-weight:800;color:{acc};margin-top:6px;'>HealthLink Kenya</div>
        <div style='font-size:11px;color:{muted};margin-top:4px;'>Clinical Decision-Support Platform</div>
    </div>
    <div style='background:{"#21262D" if is_dark else "#F0F4FA"};border-radius:10px;padding:10px 14px;margin-bottom:10px;'>
        <div style='font-size:12px;font-weight:700;color:{acc};'>👤 {user.get("name","User")}</div>
        <div style='font-size:11px;color:{muted};'>{user.get("role","")}</div>
        <div style='font-size:10px;color:{muted};margin-top:2px;opacity:0.7;'>{user.get("email","")}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    module = st.radio("Navigate", [
        "📊  Overview & Insights",
        "🏥  Triage & Facility Map",
        "🗺️  Geospatial Mapper",
        "👤  Patient Retention Record",
        "📍  Distance Decay (GAM)",
        "📈  Analytics & Visuals",
        "⚙️  Settings",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:10px;color:{muted};line-height:2.0;'>
        <b style='color:{muted}'>Model:</b> XGBoost · F1 0.9034<br>
        <b style='color:{muted}'>AUC:</b> 0.6524 · Acc: 0.8240<br>
        <b style='color:{muted}'>Data:</b> KNBS HSB Survey 2022<br>
        <b style='color:{muted}'>n =</b> 99,031 observations<br>
        <b style='color:{muted}'>Threshold:</b> 25km (GAM)<br>
        <b style='color:{muted}'>API:</b> {st.session_state.api_url}
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚪  Sign Out", use_container_width=True):
        do_logout()
        st.rerun()

# ============================================================
# PAGE 1: OVERVIEW & INSIGHTS
# ============================================================
if "Overview" in module:
    st.markdown("## 📊 Overview & Insights")
    st.caption("KNBS Health-Seeking Behaviour Survey 2022 · n = 99,031 · XGBoost Operational Model")

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Population Access Rate",  "78.4%",  "+3.2% vs prev. quarter")
    k2.metric("Retention Rate",          "71.2%",  "+1.8% vs prev. quarter")
    k3.metric("GAM Critical Threshold",  "25 km",  "Access drops sharply beyond")
    k4.metric("Urban Proximity Paradox", "3,484",  "Patients facing hidden barriers")
    st.markdown("---")

    st.markdown("### Andersen's Behavioural Model — Feature Weight by Category")
    col_a,col_b,col_c = st.columns(3)
    with col_a:
        st.markdown(f"""<div class='med-card-amber'>
            <div style='font-size:12px;font-weight:700;color:#92400E;letter-spacing:.04em;text-transform:uppercase;'>Enabling Factors · 73%</div>
            <div style='font-size:13px;color:{muted};margin-top:10px;line-height:2.2;'>
                Distance to Facility &nbsp;<b style='color:{text};'>41%</b><br>
                Wealth Index &nbsp;<b style='color:{text};'>18%</b><br>
                Insurance Status &nbsp;<b style='color:{text};'>14%</b>
            </div>
            <div style='font-size:10px;color:#B45309;margin-top:10px;font-weight:600;'>Dominant predictors of access</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""<div class='med-card-blue'>
            <div style='font-size:12px;font-weight:700;color:#1E3A8A;letter-spacing:.04em;text-transform:uppercase;'>Predisposing Factors · 25%</div>
            <div style='font-size:13px;color:{muted};margin-top:10px;line-height:2.2;'>
                Residence Type &nbsp;<b style='color:{text};'>9%</b><br>
                Education Level &nbsp;<b style='color:{text};'>8%</b><br>
                Age Group &nbsp;<b style='color:{text};'>5%</b> &nbsp; Gender &nbsp;<b style='color:{text};'>3%</b>
            </div>
            <div style='font-size:10px;color:#1D4ED8;margin-top:10px;font-weight:600;'>Demographic & social attributes</div>
        </div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""<div class='med-card-green'>
            <div style='font-size:12px;font-weight:700;color:#065F46;letter-spacing:.04em;text-transform:uppercase;'>Need Factors · 2%</div>
            <div style='font-size:13px;color:{muted};margin-top:10px;line-height:2.2;'>
                Provider Group &nbsp;<b style='color:{text};'>2%</b><br>
                Perceived health need<br>Triage classification
            </div>
            <div style='font-size:10px;color:#059669;margin-top:10px;font-weight:600;'>Lowest individual weight</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_l,col_r = st.columns(2)
    fac_types      = ["National Referral","County Hospital","Sub-County","Health Centre","Dispensary/Clinic"]
    access_vals    = [94,79,61,52,37]
    retention_vals = [89,71,53,44,30]

    with col_l:
        st.markdown("#### Access Rate by Facility Type")
        fig_a = go.Figure(go.Bar(
            x=access_vals, y=fac_types, orientation="h",
            marker_color=[acc if v>=50 else "#EF4444" for v in access_vals],
            text=[f"{v}%" for v in access_vals], textposition="outside",
        ))
        fig_a.update_layout(paper_bgcolor=card,plot_bgcolor=card,font_color=text,
            height=260,margin=dict(l=0,r=40,t=10,b=10),
            xaxis=dict(showgrid=True,gridcolor=border,range=[0,110],color=muted),
            yaxis=dict(color=text),showlegend=False)
        st.plotly_chart(fig_a, use_container_width=True)

    with col_r:
        st.markdown("#### Access → Retention Gap")
        gap_vals   = [a-r for a,r in zip(access_vals,retention_vals)]
        gap_colors = ["#EF4444" if g>12 else "#F59E0B" if g>8 else "#10B981" for g in gap_vals]
        fig_g = go.Figure(go.Bar(
            x=gap_vals,y=fac_types,orientation="h",marker_color=gap_colors,
            text=[f"{v}pp" for v in gap_vals],textposition="outside",
        ))
        fig_g.update_layout(paper_bgcolor=card,plot_bgcolor=card,font_color=text,
            height=260,margin=dict(l=0,r=40,t=10,b=10),
            xaxis=dict(showgrid=True,gridcolor=border,range=[0,25],color=muted,title="Access–Retention gap (pp)"),
            yaxis=dict(color=text),showlegend=False)
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown(f"""<div class='med-card-red'>
        <b style='color:#DC2626;'>⚠️ Urban Proximity Paradox Detected</b><br>
        <span style='font-size:12px;color:{muted};'>
        3,484 patients within &lt;50km failed to access care despite favourable profiles.
        Flagged: <b style='color:{text};'>Mathare North HC · Kayole Sub-County · Dandora Dispensary</b>.
        </span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# PAGE 2: TRIAGE & FACILITY MAP (combined)
# ============================================================
elif "Triage" in module:
    st.markdown("## 🏥 Predictive Triage & Nearby Facilities")
    st.caption("Enter patient profile → get access probability → see nearby facilities on map")

    # ── Triage form ──────────────────────────────────────────
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### Patient Demographics")
        age_group = st.selectbox("Age Group", ["0-4","5-14","15-24","25-34","35-49","50-64","65+"])
        gender    = st.selectbox("Gender", ["Female","Male"])
        residence = st.radio("Residence Type", ["Urban","Rural"], horizontal=True)
    with col2:
        st.markdown("#### Enabling Factors")
        wealth_index = st.select_slider("Wealth Index", options=["Poorest","Poorer","Middle","Richer","Richest"])
        insurance    = st.radio("Insurance Status", ["Insured","Uninsured"], horizontal=True)
        distance_km  = st.slider("Distance to Nearest Facility (km)", 0.0, 100.0, 5.0, 0.5)

    if distance_km > 25:
        st.markdown(f"""<div class='med-card-red' style='margin-top:8px;'>
            <b style='color:#DC2626;'>📍 Beyond GAM Threshold (25km)</b> —
            <span style='font-size:12px;color:{muted};'>Access probability drops sharply. Consider mobile clinic or ambulance dispatch.</span>
        </div>""", unsafe_allow_html=True)
    elif distance_km > 15:
        st.markdown(f"""<div class='med-card-amber' style='margin-top:8px;'>
            <span style='font-size:12px;color:#92400E;'>⚡ Approaching critical zone (15–25km). Monitor this catchment.</span>
        </div>""", unsafe_allow_html=True)

    clinical_notes = st.text_area("Clinical Notes (Optional NLP Input)",
        value="Patient reports fever and difficulty travelling to facility.", height=70)

    if st.button("🔍  Run Access Prediction"):
        payload = {
            "distance_km":distance_km,"age_group":age_group,"gender":gender,
            "wealth_index":wealth_index,"insurance_status":1 if insurance=="Insured" else 0,
            "residential_area_group":residence,"survey_weight":1.0,"clinical_notes":clinical_notes
        }
        try:
            with st.spinner("Querying FastAPI inference engine..."):
                response = requests.post(f"{st.session_state.api_url}/predict_access", json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                prob   = result["probability"]
                st.markdown("---")
                m1,m2,m3 = st.columns(3)
                m1.metric("Access Probability", f"{prob}%")
                m2.metric("Prediction", "Will Access ✅" if result["prediction"]==1 else "Will NOT Access ❌")
                m3.metric("Distance Zone", ">25km ⚠️" if distance_km>25 else "Safe Zone ✅")
                st.progress(prob/100)
                if prob>=70:
                    st.markdown(f'<div class="med-card-green"><b style="color:#065F46;">✅ High likelihood of access.</b></div>', unsafe_allow_html=True)
                elif prob>=40:
                    st.markdown(f'<div class="med-card-amber"><b style="color:#92400E;">⚡ Moderate likelihood — consider outreach support.</b></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="med-card-red"><b style="color:#DC2626;">🚨 Low likelihood — prioritise mobile clinic or CHW intervention.</b></div>', unsafe_allow_html=True)
                if clinical_notes and result.get("nlp_analysis",{}).get("cleaned_keywords"):
                    st.info(f"**NLP Keywords:** {result['nlp_analysis']['cleaned_keywords']}")
            else:
                st.error(f"API Error {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("🚨 Cannot connect to FastAPI. Run: `.venv\\Scripts\\python.exe -m uvicorn api:app` in a separate terminal.")
        except requests.exceptions.Timeout:
            st.error("Request timed out.")

    # ── Facility mini-map below triage ───────────────────────
    st.markdown("---")
    st.markdown("#### 🗺️ Nearby Facilities — Based on Patient Distance")
    nearby = FACILITIES_DATA[FACILITIES_DATA["Dist_km"] <= max(distance_km + 10, 15)].copy()
    si1,si2,si3 = st.columns(3)
    si1.metric("Facilities Within Range", len(nearby))
    si2.metric("Avg Access Rate", f"{nearby['Access_pct'].mean():.1f}%")
    si3.metric("Paradox Facilities", int(nearby["Paradox"].sum()))

    m_triage = make_facility_map(nearby, show_ring=True)
    st_folium(m_triage, width="100%", height=400)

    st.markdown("#### Facility Quick Reference")
    qref = nearby[["Name","Type","Dist_km","Access_pct","Specialties"]].copy()
    qref.columns = ["Facility","Type","Dist (km)","Access %","Specialties Available"]
    st.dataframe(qref, use_container_width=True, hide_index=True)


# ============================================================
# PAGE 3: FULL GEOSPATIAL MAPPER
# ============================================================
elif "Mapper" in module:
    st.markdown("## 🗺️ Geospatial Facility Mapper")
    st.caption("Full facility map · Type legends · Specialised treatment filter · Nairobi County")

    fc1,fc2,fc3 = st.columns([2,2,1])
    with fc1:
        selected_types = st.multiselect("Filter by Facility Type",
            options=sorted(FACILITIES_DATA["Type"].unique()),
            default=list(FACILITIES_DATA["Type"].unique()))
    with fc2:
        selected_spec = st.multiselect("Filter by Specialised Treatment",
            options=ALL_SPECIALTIES, placeholder="All specialties shown")
    with fc3:
        max_dist   = st.slider("Max distance (km)", 1, 60, 50)
        show_ring  = st.checkbox("25km GAM ring", value=True)

    filtered = FACILITIES_DATA[
        (FACILITIES_DATA["Dist_km"] <= max_dist) &
        (FACILITIES_DATA["Type"].isin(selected_types))
    ].copy()
    if selected_spec:
        filtered = filtered[filtered["Specialties"].apply(
            lambda s: any(sp in s for sp in selected_spec))]

    si1,si2,si3,si4 = st.columns(4)
    si1.metric("Facilities in Range", len(filtered))
    si2.metric("Avg Access Rate", f"{filtered['Access_pct'].mean():.1f}%" if len(filtered) else "—")
    si3.metric("Paradox Facilities", int(filtered["Paradox"].sum()))
    si4.metric("Types Shown", len(filtered["Type"].unique()))

    m_full = make_facility_map(filtered, show_ring=show_ring)
    st_folium(m_full, width="100%", height=520)

    st.markdown("#### Map Legend — Facility Types")
    leg_cols = st.columns(4)
    for i,(ftype,col) in enumerate(LEGEND_COLORS.items()):
        leg_cols[i%4].markdown(
            f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px;'>"
            f"<div style='width:12px;height:12px;border-radius:50%;background:{col};flex-shrink:0;'></div>"
            f"<span style='font-size:11px;color:{muted};'>{ftype}</span></div>",
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Facility Details")
    disp = filtered[["Name","Type","Specialties","Dist_km","Access_pct","Retention_pct","Insurance_pct","Paradox"]].copy()
    disp.columns = ["Facility","Type","Specialties","Dist (km)","Access %","Retention %","Insurance %","⚠ Paradox"]
    st.dataframe(disp, use_container_width=True, hide_index=True)


# ============================================================
# PAGE 4: PATIENT RETENTION RECORD
# ============================================================
elif "Retention" in module:
    st.markdown("## 👤 Patient Retention Record")
    st.caption("Existing patient follow-up · Visit history · Treatment continuity · Care plan status")

    col_s,col_btn = st.columns([3,1])
    with col_s:
        pt_id = st.text_input("Search by Patient ID or National ID", placeholder="e.g.  PT-2024-00142")
    with col_btn:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        st.button("Load Patient Record", use_container_width=True)

    st.markdown("---")
    pt = {
        "id":"PT-2024-00142","name":"Amina Wanjiru Kariuki","dob":"14 March 1987","age":37,
        "gender":"Female","national_id":"23456781","nhif_no":"NHIF-KE-882341",
        "insurance":"NHIF (Active)","facility":"Mbagathi District Hospital",
        "clinician":"Dr. P. Ochieng","blood_group":"O+","allergies":"Penicillin, Sulfonamides",
        "phone":"+254 712 345 678","county":"Nairobi","distance_km":8.1,
        "wealth":"Middle","residence":"Urban","access_prob":77,"retention_prob":71,
        "next_appointment":"28 March 2026","last_visit":"12 February 2026",
        "visits_ytd":4,"total_visits":17,
        "conditions":["Hypertension","Type 2 Diabetes"],
        "medications":[
            {"Drug":"Amlodipine 5mg",   "Dose":"1 tab OD","Refill Due":"28 Mar 2026","Status":"Active"},
            {"Drug":"Metformin 500mg",   "Dose":"1 tab BD","Refill Due":"28 Mar 2026","Status":"Active"},
            {"Drug":"Atorvastatin 20mg","Dose":"1 tab ON","Refill Due":"28 Mar 2026","Status":"Active"},
        ],
        "visits":[
            {"Date":"12 Feb 2026","Facility":"Mbagathi District Hospital","Type":"Chronic Disease Review","Clinician":"Dr. P. Ochieng","BP":"138/88","Sugar":"7.4 mmol/L","Notes":"Well-controlled. Refill issued."},
            {"Date":"10 Jan 2026","Facility":"Mbagathi District Hospital","Type":"Routine OPD","Clinician":"Dr. P. Ochieng","BP":"142/92","Sugar":"8.1 mmol/L","Notes":"Metformin dose increased."},
            {"Date":"05 Nov 2025","Facility":"Mbagathi District Hospital","Type":"Emergency (Hypertensive)","Clinician":"Dr. R. Njoroge","BP":"178/104","Sugar":"9.2 mmol/L","Notes":"IV antihypertensive. Admitted overnight."},
            {"Date":"22 Sep 2025","Facility":"Ruaraka Health Centre","Type":"Chronic Disease Review","Clinician":"Sr. M. Auma","BP":"136/86","Sugar":"7.0 mmol/L","Notes":"Stable. Routine refill."},
        ],
        "investigations":[
            {"Test":"HbA1c",          "Date":"12 Feb 2026","Result":"7.8%",          "Normal Range":"<7.0%",         "Flag":"⚠️ Elevated"},
            {"Test":"Fasting Glucose","Date":"12 Feb 2026","Result":"7.4 mmol/L",    "Normal Range":"3.9–5.5 mmol/L","Flag":"⚠️ Elevated"},
            {"Test":"Lipid Panel",    "Date":"10 Jan 2026","Result":"LDL 3.2 mmol/L","Normal Range":"<2.6 mmol/L",   "Flag":"⚠️ Borderline"},
            {"Test":"BP",            "Date":"12 Feb 2026","Result":"138/88 mmHg",   "Normal Range":"<130/80 mmHg",  "Flag":"⚠️ Elevated"},
            {"Test":"Renal Function","Date":"10 Jan 2026","Result":"Creatinine 82", "Normal Range":"62–106 µmol/L", "Flag":"✅ Normal"},
        ],
        "referrals":[
            {"Date":"12 Feb 2026","Referred To":"KNH — Cardiology","Reason":"Uncontrolled hypertension, cardiac risk assessment","Status":"Pending"},
        ],
    }

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
        </div>
    </div>""", unsafe_allow_html=True)

    a1,a2,a3,a4 = st.columns(4)
    a1.metric("Access Probability",    f"{pt['access_prob']}%",   "XGBoost model")
    a2.metric("Retention Probability", f"{pt['retention_prob']}%","Retention model")
    a3.metric("Next Appointment",      pt["next_appointment"])
    a4.metric("Visits YTD / Total",    f"{pt['visits_ytd']} / {pt['total_visits']}")

    tab_sum,tab_vis,tab_med,tab_lab,tab_ref = st.tabs(
        ["📋 Summary","🗓 Visit History","💊 Medications","🔬 Investigations","🔀 Referrals"])

    with tab_sum:
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("#### Personal Details")
            for label,val in [("Date of Birth",pt["dob"]),("County",pt["county"]),
                ("Phone",pt["phone"]),("Residence",pt["residence"]),("Wealth Index",pt["wealth"]),
                ("Distance to Facility",f"{pt['distance_km']} km"),("Last Visit",pt["last_visit"])]:
                st.markdown(f"<div class='pt-row'><span class='pt-label'>{label}</span><span class='pt-value'>{val}</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("#### Active Conditions")
            for cond in pt["conditions"]:
                st.markdown(f"<div class='med-card-blue' style='margin-bottom:8px;'><span style='font-size:13px;font-weight:600;color:#1D4ED8;'>🩺 {cond}</span></div>", unsafe_allow_html=True)
            dist = pt["distance_km"]
            if dist<=25:   zc,zl,zb="#065F46","✅ Safe Zone (≤25km)","#EDFBF5"
            elif dist<=50: zc,zl,zb="#92400E","⚠️ Transition Zone","#FFFBEE"
            else:          zc,zl,zb="#DC2626","🚨 Exclusion Zone","#FFF5F5"
            st.markdown(f"<div style='background:{zb};border-radius:10px;padding:14px 16px;margin-top:12px;'><div style='font-size:11px;color:{muted};text-transform:uppercase;font-weight:600;'>GAM Distance Zone</div><div style='font-size:16px;font-weight:800;color:{zc};margin-top:4px;'>{zl}</div><div style='font-size:12px;color:{muted};margin-top:2px;'>{dist} km from registered facility</div></div>", unsafe_allow_html=True)

    with tab_vis:
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

    with tab_med:
        for med in pt["medications"]:
            st.markdown(f"""<div class='med-card' style='display:flex;justify-content:space-between;'>
                <div><div style='font-size:14px;font-weight:700;color:{acc};'>💊 {med["Drug"]}</div>
                <div style='font-size:12px;color:{muted};margin-top:3px;'>Dose: <b style='color:{text};'>{med["Dose"]}</b></div></div>
                <div style='text-align:right;'>
                    <div style='font-size:11px;color:{muted};'>Refill Due</div>
                    <div style='font-size:13px;font-weight:700;color:{acc};'>{med["Refill Due"]}</div>
                    <span class='badge-green'>{med["Status"]}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    with tab_lab:
        st.dataframe(pd.DataFrame(pt["investigations"]), use_container_width=True, hide_index=True)

    with tab_ref:
        for ref in pt["referrals"]:
            st.markdown(f"""<div class='med-card-blue'>
                <div style='font-size:13px;font-weight:700;color:#1D4ED8;'>🔀 {ref["Referred To"]}</div>
                <div style='font-size:12px;color:{muted};margin-top:4px;'>Date: <b style='color:{text};'>{ref["Date"]}</b> &nbsp;·&nbsp; Status: <span class='badge-amber'>{ref["Status"]}</span></div>
                <div style='font-size:12px;color:{muted};margin-top:6px;'>{ref["Reason"]}</div>
            </div>""", unsafe_allow_html=True)


# ============================================================
# PAGE 5: DISTANCE DECAY (GAM)
# ============================================================
elif "Decay" in module:
    st.markdown("## 📍 Distance Decay — GAM Analysis")
    st.caption("Generalised Additive Model spline · Critical inflection at 25km · KNBS 2022")

    fig = go.Figure()
    safe_dist   = [d for d in GAM_DIST if d<=25]
    safe_prob   = [p for d,p in zip(GAM_DIST,GAM_PROB) if d<=25]
    danger_dist = [d for d in GAM_DIST if d>=25]
    danger_prob = [p for d,p in zip(GAM_DIST,GAM_PROB) if d>=25]

    fig.add_trace(go.Scatter(x=safe_dist+[25],y=safe_prob+[0.76],
        fill="tozeroy",fillcolor="rgba(16,185,129,0.10)",
        line=dict(color="rgba(0,0,0,0)"),showlegend=False))
    fig.add_trace(go.Scatter(x=danger_dist,y=danger_prob,
        fill="tozeroy",fillcolor="rgba(239,68,68,0.08)",
        line=dict(color="rgba(0,0,0,0)"),showlegend=False))
    fig.add_trace(go.Scatter(x=GAM_DIST,y=GAM_PROB,
        mode="lines+markers",line=dict(color=acc,width=3),
        marker=dict(size=7,color=acc),
        name="P(Access | Distance)",hovertemplate="Distance: %{x}km<br>Access Prob: %{y:.0%}"))
    fig.add_vline(x=25,line_dash="dash",line_color="#F59E0B",line_width=2,
        annotation_text="25km Inflection",annotation_font_color="#F59E0B",annotation_position="top right")
    fig.add_trace(go.Scatter(x=[25],y=[0.76],mode="markers",
        marker=dict(size=12,color="#F59E0B",symbol="circle"),
        name="Critical Inflection",hovertemplate="25km → 76% access probability"))
    fig.update_layout(paper_bgcolor=card,plot_bgcolor=card,font_color=text,height=420,
        xaxis=dict(title="Distance to Nearest Facility (km)",color=muted,gridcolor=border,linecolor=border),
        yaxis=dict(title="Probability of Accessing Care",tickformat=".0%",color=muted,gridcolor=border),
        legend=dict(bgcolor=card,bordercolor=border),margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(fig, use_container_width=True)

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(f"""<div class='med-card-green'><b style='color:#065F46;'>0–25km · Safe Zone</b><br><span style='font-size:11px;color:{muted};'>Access probability 76–96%. Effective catchment for standard facility deployment and ambulance dispatch.</span></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class='med-card-amber'><b style='color:#92400E;'>25km · Critical Inflection</b><br><span style='font-size:11px;color:{muted};'>GAM-derived empirical threshold. Evidence base for mobile clinic deployment radius and policy recalibration.</span></div>""", unsafe_allow_html=True)
    with c3: st.markdown(f"""<div class='med-card-red'><b style='color:#DC2626;'>&gt;25km · Danger Zone</b><br><span style='font-size:11px;color:{muted};'>Access drops precipitously toward zero. Priority zone for mobile health unit deployment and transport subsidies.</span></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class='med-card-blue' style='margin-top:16px;'>
        <b style='color:#1D4ED8;'>📋 Policy Implication (Ministry of Health)</b><br>
        <span style='font-size:12px;color:{muted};'>The 25km catchment standard should supplement the linear 5km buffer currently used in epidemiological planning. Mobile clinic deployment and ambulance dispatch radius should be recalibrated to this empirically derived GAM threshold.</span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# PAGE 6: ANALYTICS & VISUALS
# ============================================================
elif "Analytics" in module:
    st.markdown("## 📈 Analytics & Model Visuals")
    st.caption("SHAP feature importance · Algorithm tournament · Model performance comparison")

    vtab1,vtab2 = st.tabs(["🧠 SHAP Interpretability","⚙️ Model Performance"])

    with vtab1:
        col_chart,col_insight = st.columns([3,2])
        with col_chart:
            cat_colors = {"Enabling":"#F59E0B","Predisposing":"#6366F1","Need":"#10B981"}
            bar_colors = [cat_colors[c] for c in SHAP_DATA["Category"]]
            fig_shap = go.Figure(go.Bar(
                x=SHAP_DATA["Importance"]*100, y=SHAP_DATA["Feature"],
                orientation="h", marker_color=bar_colors,
                text=[f"{v*100:.0f}%" for v in SHAP_DATA["Importance"]],
                textposition="outside",
                hovertemplate="%{y}<br>Importance: %{x:.1f}%<extra></extra>"
            ))
            fig_shap.update_layout(paper_bgcolor=card,plot_bgcolor=card,font_color=text,height=340,
                xaxis=dict(title="SHAP Importance (%)",color=muted,gridcolor=border,range=[0,55]),
                yaxis=dict(color=text,autorange="reversed"),margin=dict(l=10,r=50,t=10,b=10))
            st.plotly_chart(fig_shap, use_container_width=True)
            lcols = st.columns(3)
            for i,(cat,col) in enumerate(cat_colors.items()):
                total = SHAP_DATA[SHAP_DATA["Category"]==cat]["Importance"].sum()*100
                lcols[i].markdown(f"""<div style='background:{col}18;border:1px solid {col}40;border-radius:8px;padding:8px 12px;text-align:center;'>
                    <div style='font-size:10px;color:{col};font-weight:700;text-transform:uppercase;'>{cat}</div>
                    <div style='font-size:20px;font-weight:900;color:{col};'>{total:.0f}%</div>
                    <div style='font-size:10px;color:{muted};'>combined weight</div>
                </div>""", unsafe_allow_html=True)
        with col_insight:
            st.markdown(f"""
            <div class='med-card-amber' style='margin-bottom:12px;'>
                <b style='color:#92400E;'>🎯 Dominant Signal: Distance</b><br>
                <span style='font-size:11px;color:{muted};'>Distance_km drives 41% of model decisions — more than all socioeconomic features combined. Validates the 25km GAM threshold.</span>
            </div>
            <div class='med-card-blue' style='margin-bottom:12px;'>
                <b style='color:#1D4ED8;'>💰 Enabling: 73% Combined</b><br>
                <span style='font-size:11px;color:{muted};'>Distance + Wealth + Insurance = 73% of model weight. Targeting all three simultaneously yields the highest policy ROI.</span>
            </div>
            <div class='med-card-green'>
                <b style='color:#065F46;'>👤 Predisposing: 25%</b><br>
                <span style='font-size:11px;color:{muted};'>Residence type (urban vs rural) is the strongest predisposing signal. Education and age have smaller but consistent contributions.</span>
            </div>""", unsafe_allow_html=True)

    with vtab2:
        def style_row(row):
            if row["Algorithm"]=="XGBoost (Optimised)":
                return [f"background-color:{card_b};color:{acc};font-weight:600"]*len(row)
            return [f"color:{text}"]*len(row)
        display = MODEL_PERF.drop(columns=["Operational"])
        st.dataframe(display.style.apply(style_row,axis=1), use_container_width=True, hide_index=True)
        st.markdown("---")
        fig_m = go.Figure()
        for col_name,color in [("F1",acc),("AUC","#0891B2"),("Accuracy","#6366F1")]:
            fig_m.add_trace(go.Bar(name=col_name,x=MODEL_PERF["Algorithm"],y=MODEL_PERF[col_name],
                marker_color=color,opacity=0.85))
        fig_m.update_layout(barmode="group",paper_bgcolor=card,plot_bgcolor=card,font_color=text,height=350,
            xaxis=dict(color=muted,gridcolor=border,tickangle=-25),
            yaxis=dict(color=muted,gridcolor=border,range=[0,1.05]),
            legend=dict(bgcolor=card,bordercolor=border),margin=dict(l=10,r=10,t=10,b=80))
        st.plotly_chart(fig_m, use_container_width=True)

        c1,c2 = st.columns(2)
        with c1: st.markdown(f"""<div class='med-card-red'><b style='color:#DC2626;'>⚖️ Class Imbalance</b><br><span style='font-size:11px;color:{muted};'>scale_pos_weight corrects heavy skew. Result: 3,484 FPs (Urban Proximity Paradox) · 5 FNs.</span></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class='med-card-green'><b style='color:#065F46;'>✅ Why XGBoost</b><br><span style='font-size:11px;color:{muted};'>Highest single-model AUC (0.6524). Ensemble marginally stabilised variance without material gain — XGBoost selected for deployment.</span></div>""", unsafe_allow_html=True)


# ============================================================
# PAGE 7: SETTINGS
# ============================================================
elif "Settings" in module:
    st.markdown("## ⚙️ Dashboard Settings")
    st.caption("Personalise your HealthLink Kenya experience")

    s1,s2 = st.columns(2)

    with s1:
        st.markdown(f"<div class='med-card'>", unsafe_allow_html=True)
        st.markdown("#### 🎨 Appearance")

        new_theme = st.radio("Colour Theme", ["light","dark"],
            index=0 if st.session_state.theme=="light" else 1, horizontal=True)

        accent_options = {
            "Navy Blue (#0B3D6E)":  "#0B3D6E",
            "Teal (#0891B2)":       "#0891B2",
            "Forest Green (#065F46)":"#065F46",
            "Deep Purple (#5B21B6)":"#5B21B6",
            "Crimson (#B91C1C)":    "#B91C1C",
        }
        new_accent_label = st.selectbox("Accent Colour",
            options=list(accent_options.keys()),
            index=list(accent_options.values()).index(st.session_state.accent)
                if st.session_state.accent in accent_options.values() else 0)

        new_font = st.radio("Font Size", ["Small","Medium","Large"],
            index=["Small","Medium","Large"].index(st.session_state.font_size), horizontal=True)

        if st.button("Apply Appearance Settings", use_container_width=True):
            st.session_state.theme     = new_theme
            st.session_state.accent    = accent_options[new_accent_label]
            st.session_state.font_size = new_font
            st.success("✅ Appearance updated — refreshing...")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown(f"<div class='med-card'>", unsafe_allow_html=True)
        st.markdown("#### 🗺️ Map Settings")
        map_options = [
            "CartoDB positron",
            "CartoDB dark_matter",
            "OpenStreetMap",
            "Stamen Terrain",
        ]
        new_map = st.selectbox("Map Tile Style", map_options,
            index=map_options.index(st.session_state.map_style)
                if st.session_state.map_style in map_options else 0)
        new_paradox = st.checkbox("Highlight Urban Proximity Paradox facilities in red",
            value=st.session_state.show_paradox)

        st.markdown("#### 🔌 API Configuration")
        new_api = st.text_input("FastAPI Base URL", value=st.session_state.api_url)

        if st.button("Save Map & API Settings", use_container_width=True):
            st.session_state.map_style   = new_map
            st.session_state.show_paradox= new_paradox
            st.session_state.api_url     = new_api
            st.success("✅ Settings saved.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div class='med-card'>", unsafe_allow_html=True)
    st.markdown("#### 👤 Account Information")
    ac1,ac2,ac3 = st.columns(3)
    ac1.metric("Logged in as", user.get("name","—"))
    ac2.metric("Role",         user.get("role","—"))
    ac3.metric("Session",      datetime.now().strftime("%d %b %Y · %H:%M"))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""<div class='med-card-blue' style='margin-top:12px;'>
        <b style='color:#1D4ED8;'>ℹ️ About HealthLink Kenya</b><br>
        <span style='font-size:12px;color:{muted};'>
        Version 2.0 · MSc Data Science & Analytics · Strathmore University · April 2026<br>
        Model: XGBoost · Data: KNBS Health-Seeking Behaviour Survey 2022 · n = 99,031<br>
        Researcher: Rutendo Julia Kandeya (168332) · Supervisor: Dr. Esther Khakata
        </span>
    </div>""", unsafe_allow_html=True)
