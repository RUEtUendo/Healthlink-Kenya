import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

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
# DARK / LIGHT MODE
# ============================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ============================================================
# THEME COLOURS
# ============================================================
if st.session_state.dark_mode:
    BG      = "#07111F"; SURFACE = "#0D1E30"; CARD    = "#102234"
    BORDER  = "#1A3450"; TEXT    = "#D9E8F5"; MUTED   = "#5A7A99"
    HEAD    = "#FFFFFF";  ACCENT  = "#00D9A3"; GOLD    = "#F5A623"
    RED     = "#F87171"; SKY     = "#38BDF8"; PURPLE  = "#A78BFA"
    BTN_TXT = "#07111F"; MAP_TILE= "CartoDB dark_matter"
else:
    BG      = "#F0F7F4"; SURFACE = "#FFFFFF"; CARD    = "#FFFFFF"
    BORDER  = "#B8DCCF"; TEXT    = "#1A3A2A"; MUTED   = "#4A7A6A"
    HEAD    = "#0A4A3A"; ACCENT  = "#007A5A"; GOLD    = "#C47A00"
    RED     = "#B91C1C"; SKY     = "#0369A1"; PURPLE  = "#6D28D9"
    BTN_TXT = "#FFFFFF"; MAP_TILE= "CartoDB positron"

# ============================================================
# CSS
# ============================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background-color: {BG}; color: {TEXT}; }}
    section[data-testid="stSidebar"] {{ background-color: {SURFACE}; border-right: 2px solid {BORDER}; }}
    h1, h2, h3, h4 {{ color: {HEAD} !important; }}
    [data-testid="metric-container"] {{
        background: {CARD}; border: 1.5px solid {BORDER};
        border-radius: 14px; padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    [data-testid="metric-container"] label {{ color: {MUTED} !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.06em; }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{ color: {ACCENT} !important; font-size: 26px !important; font-weight: 700 !important; }}
    .stButton > button {{
        background: {ACCENT} !important; color: {BTN_TXT} !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 700 !important; padding: 10px 24px !important; font-size: 14px !important;
    }}
    .stButton > button:hover {{ opacity: 0.85 !important; }}
    .call-btn {{
        display: inline-block; background: {ACCENT}; color: {BTN_TXT} !important;
        border-radius: 8px; padding: 6px 14px; font-size: 12px; font-weight: 700;
        text-decoration: none !important; margin-top: 4px;
    }}
    .card {{ background: {CARD}; border: 1.5px solid {BORDER}; border-radius: 14px; padding: 18px 20px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .card-accent {{ border-left: 4px solid {ACCENT}; }}
    .card-gold   {{ border-left: 4px solid {GOLD}; }}
    .card-red    {{ border-left: 4px solid {RED}; }}
    .badge {{ display: inline-block; border-radius: 99px; padding: 2px 10px; font-size: 11px; font-weight: 700; margin-right: 4px; }}
    .badge-green  {{ background: {ACCENT}22; color: {ACCENT}; border: 1px solid {ACCENT}44; }}
    .badge-gold   {{ background: {GOLD}22;   color: {GOLD};   border: 1px solid {GOLD}44; }}
    .badge-red    {{ background: {RED}22;    color: {RED};    border: 1px solid {RED}44; }}
    .badge-sky    {{ background: {SKY}22;    color: {SKY};    border: 1px solid {SKY}44; }}
    .badge-purple {{ background: {PURPLE}22; color: {PURPLE}; border: 1px solid {PURPLE}44; }}
    .plain-box {{ background: {ACCENT}11; border: 1.5px solid {ACCENT}33; border-radius: 12px; padding: 16px 20px; margin-bottom: 14px; font-size: 14px; color: {TEXT}; line-height: 1.8; }}
    .stProgress > div > div {{ background-color: {ACCENT} !important; }}
    .stSelectbox label, .stSlider label, .stRadio label,
    .stTextArea label, .stSelectSlider label, .stTextInput label {{
        color: {MUTED} !important; font-size: 12px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 0.05em;
    }}
    hr {{ border-color: {BORDER}; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================
FACILITIES = pd.DataFrame([
    {"Name": "Kenyatta National Hospital",    "Type": "National Referral", "Sector": "Public",     "Dist_km": 0,    "Insurance_pct": 91, "Wealth": "Highest", "Access_pct": 94, "Retention_pct": 89, "Lat": -1.3006, "Lon": 36.8066, "Paradox": False, "Phone": "+254202726300"},
    {"Name": "Pumwani Maternity Hospital",    "Type": "County Hospital",   "Sector": "Public",     "Dist_km": 4.2,  "Insurance_pct": 62, "Wealth": "Middle",  "Access_pct": 81, "Retention_pct": 74, "Lat": -1.2841, "Lon": 36.8458, "Paradox": False, "Phone": "+254202216977"},
    {"Name": "Mathare North HC",             "Type": "Health Centre",     "Sector": "Public",     "Dist_km": 6.8,  "Insurance_pct": 31, "Wealth": "Lowest",  "Access_pct": 48, "Retention_pct": 44, "Lat": -1.2611, "Lon": 36.8590, "Paradox": True,  "Phone": "+254208020000"},
    {"Name": "Mbagathi District Hospital",   "Type": "County Hospital",   "Sector": "Public",     "Dist_km": 8.1,  "Insurance_pct": 55, "Wealth": "Middle",  "Access_pct": 77, "Retention_pct": 71, "Lat": -1.3217, "Lon": 36.7680, "Paradox": False, "Phone": "+254202705272"},
    {"Name": "Kayole Sub-County Hospital",   "Type": "Sub-County",        "Sector": "Public",     "Dist_km": 12.4, "Insurance_pct": 28, "Wealth": "Second",  "Access_pct": 43, "Retention_pct": 38, "Lat": -1.2718, "Lon": 36.9001, "Paradox": True,  "Phone": "+254208020000"},
    {"Name": "Dandora Dispensary",           "Type": "Dispensary",        "Sector": "Public",     "Dist_km": 18.3, "Insurance_pct": 19, "Wealth": "Lowest",  "Access_pct": 37, "Retention_pct": 30, "Lat": -1.2595, "Lon": 36.9087, "Paradox": True,  "Phone": "+254208020000"},
    {"Name": "Kangemi Health Centre",        "Type": "Health Centre",     "Sector": "Public",     "Dist_km": 21.1, "Insurance_pct": 33, "Wealth": "Second",  "Access_pct": 55, "Retention_pct": 48, "Lat": -1.2724, "Lon": 36.7369, "Paradox": False, "Phone": "+254208020000"},
    {"Name": "Thika Level 5 Hospital",       "Type": "County Hospital",   "Sector": "Public",     "Dist_km": 44.2, "Insurance_pct": 52, "Wealth": "Fourth",  "Access_pct": 24, "Retention_pct": 20, "Lat": -1.0332, "Lon": 37.0693, "Paradox": False, "Phone": "+254672203100"},
    # Faith-Based
    {"Name": "Mater Misericordiae Hospital", "Type": "County Hospital",   "Sector": "Faith-Based","Dist_km": 3.1,  "Insurance_pct": 70, "Wealth": "Middle",  "Access_pct": 82, "Retention_pct": 77, "Lat": -1.3056, "Lon": 36.8347, "Paradox": False, "Phone": "+254206902000"},
    {"Name": "St. Francis Community Hosp.", "Type": "Health Centre",     "Sector": "Faith-Based","Dist_km": 7.4,  "Insurance_pct": 48, "Wealth": "Middle",  "Access_pct": 71, "Retention_pct": 65, "Lat": -1.3102, "Lon": 36.8789, "Paradox": False, "Phone": "+254208020000"},
    {"Name": "Nairobi Baptist Hospital",     "Type": "Clinic",            "Sector": "Faith-Based","Dist_km": 9.2,  "Insurance_pct": 53, "Wealth": "Middle",  "Access_pct": 68, "Retention_pct": 62, "Lat": -1.2956, "Lon": 36.7823, "Paradox": False, "Phone": "+254203874000"},
    {"Name": "Coptic Hospital Nairobi",      "Type": "County Hospital",   "Sector": "Faith-Based","Dist_km": 5.8,  "Insurance_pct": 65, "Wealth": "Fourth",  "Access_pct": 79, "Retention_pct": 73, "Lat": -1.2780, "Lon": 36.8120, "Paradox": False, "Phone": "+254202710900"},
    # Private
    {"Name": "Aga Khan University Hospital", "Type": "National Referral", "Sector": "Private",    "Dist_km": 2.8,  "Insurance_pct": 95, "Wealth": "Highest", "Access_pct": 91, "Retention_pct": 88, "Lat": -1.2612, "Lon": 36.8242, "Paradox": False, "Phone": "+254203662000"},
    {"Name": "Nairobi Hospital",             "Type": "County Hospital",   "Sector": "Private",    "Dist_km": 3.5,  "Insurance_pct": 88, "Wealth": "Highest", "Access_pct": 89, "Retention_pct": 85, "Lat": -1.2949, "Lon": 36.8021, "Paradox": False, "Phone": "+254202845000"},
])

MODEL_PERF = pd.DataFrame([
    {"Algorithm": "XGBoost (Best Model)", "F1": 0.9034, "AUC": 0.6524, "Accuracy": 0.8240, "Top": True },
    {"Algorithm": "Gradient Boosting",    "F1": 0.9034, "AUC": 0.6463, "Accuracy": 0.8239, "Top": False},
    {"Algorithm": "AdaBoost",             "F1": 0.9034, "AUC": 0.6397, "Accuracy": 0.8238, "Top": False},
    {"Algorithm": "Combined Top 3",       "F1": 0.9034, "AUC": 0.6510, "Accuracy": 0.8238, "Top": False},
    {"Algorithm": "Decision Tree",        "F1": 0.7584, "AUC": 0.6445, "Accuracy": 0.6496, "Top": False},
    {"Algorithm": "Random Forest",        "F1": 0.7509, "AUC": 0.6528, "Accuracy": 0.6422, "Top": False},
    {"Algorithm": "Basic Logistic Model", "F1": 0.5152, "AUC": 0.5248, "Accuracy": 0.4281, "Top": False},
])

SHAP_DATA = pd.DataFrame([
    {"Feature": "Distance to facility",  "Importance": 0.41, "Category": "Enabling",     "Plain": "How far the patient lives from a hospital"},
    {"Feature": "Household wealth",      "Importance": 0.18, "Category": "Enabling",     "Plain": "How wealthy the patient's household is"},
    {"Feature": "Health insurance",      "Importance": 0.14, "Category": "Enabling",     "Plain": "Whether the patient has insurance cover"},
    {"Feature": "Urban vs Rural",        "Importance": 0.09, "Category": "Predisposing", "Plain": "Whether the patient lives in a city or village"},
    {"Feature": "Education level",       "Importance": 0.08, "Category": "Predisposing", "Plain": "How much education the patient has received"},
    {"Feature": "Age group",             "Importance": 0.05, "Category": "Predisposing", "Plain": "The age of the patient"},
    {"Feature": "Gender",                "Importance": 0.03, "Category": "Predisposing", "Plain": "Whether the patient is male or female"},
    {"Feature": "Facility type",         "Importance": 0.02, "Category": "Need",         "Plain": "The type of facility visited"},
])

GAM_DIST = [0,5,10,15,20,25,30,35,40,50,60,80,100]
GAM_PROB = [0.96,0.94,0.91,0.88,0.84,0.76,0.58,0.40,0.27,0.14,0.08,0.04,0.02]

SECTOR_COLORS = {"Public": "blue", "Faith-Based": "purple", "Private": "green"}
SECTOR_ICONS  = {"Public": "medkit", "Faith-Based": "heart", "Private": "plus-square"}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding:16px 0 8px 0;'>
        <div style='font-size:40px;'>⚕️</div>
        <div style='font-size:17px; font-weight:800; color:{HEAD}; margin-top:6px;'>HealthLink Kenya</div>
        <div style='font-size:11px; color:{MUTED}; margin-top:4px; line-height:1.7;'>
            Hospital Referral Decision Support<br>Strathmore University · MSc DSA 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col_dm1, col_dm2 = st.columns([3, 1])
    with col_dm1:
        st.markdown(f"<div style='color:{MUTED}; font-size:12px; font-weight:600; padding-top:8px;'>{'🌙 Dark Mode' if not st.session_state.dark_mode else '☀️ Light Mode'}</div>", unsafe_allow_html=True)
    with col_dm2:
        if st.button("Switch"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("---")
    module = st.radio("Navigate", [
        "🏠  Home",
        "🏥  Find a Hospital",
        "🗺️  Facility Map",
        "📊  Access & Retention",
        "🔬  How It Works",
        "⚙️  Model Results",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:10px; color:{MUTED}; line-height:2;'>
        <b>Data:</b> KNBS Health Survey 2022<br>
        <b>Records:</b> 99,031 observations<br>
        <b>Model:</b> XGBoost · F1: 0.90<br>
        <b>Key finding:</b> 25km access threshold
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HOME
# ============================================================
if "Home" in module:
    st.markdown(f"<h1>🏠 Welcome to HealthLink Kenya</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{MUTED}; font-size:14px;'>A decision-support tool for hospital referral planning · Strathmore University MSc Thesis 2026</p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='plain-box'>
        <b>What does this dashboard do?</b><br><br>
        This tool helps hospitals in Kenya decide <b>where to send patients</b> when they need care.
        It uses data from <b>99,031 real Kenyans</b> to predict whether a patient is likely to access care,
        and identifies which nearby hospitals are available, accessible, and well-resourced.<br><br>
        <b>Who is it for?</b> Hospital administrators, referral coordinators, and health planners.
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Patients Who Access Care",  "78.4%", "↑ 3.2% improvement")
    k2.metric("Patients Who Return",        "71.2%", "↑ 1.8% improvement")
    k3.metric("Critical Distance",          "25 km", "Access drops sharply beyond this")
    k4.metric("Hidden Barriers Found",      "3,484", "Urban patients blocked by hidden issues")

    st.markdown("---")
    st.markdown(f"<h3>📖 What Each Section Shows</h3>", unsafe_allow_html=True)

    sections = [
        ("🏥 Find a Hospital",   "Enter a patient's details to predict whether they will access care and get a referral recommendation.", ACCENT),
        ("🗺️ Facility Map",      "See all hospitals on an interactive map. Call a facility directly or plan a route.", GOLD),
        ("📊 Access & Retention","See which facility types have the highest and lowest access rates across Kenya.", SKY),
        ("🔬 How It Works",      "A plain-English explanation of which factors matter most in predicting access to care.", PURPLE),
        ("⚙️ Model Results",     "Technical performance results for researchers and supervisors.", MUTED),
    ]
    c1, c2 = st.columns(2)
    for i, (title, desc, color) in enumerate(sections):
        col = c1 if i % 2 == 0 else c2
        col.markdown(f"""
        <div class='card' style='border-left:4px solid {color};'>
            <div style='font-size:14px; font-weight:700; color:{color}; margin-bottom:6px;'>{title}</div>
            <div style='font-size:12px; color:{MUTED}; line-height:1.7;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card card-red' style='margin-top:8px;'>
        <div style='font-size:13px; font-weight:700; color:{RED}; margin-bottom:6px;'>⚠️ Key Finding: The Urban Proximity Paradox</div>
        <div style='font-size:12px; color:{MUTED}; line-height:1.8;'>
        3,484 patients lived <b>close to a hospital</b> but still did <b>not</b> access care.
        Hidden barriers — long wait times, indirect costs, poor service quality —
        are stopping people from getting help even when a hospital is nearby.
        </div>
    </div>""", unsafe_allow_html=True)


# ============================================================
# FIND A HOSPITAL (TRIAGE)
# ============================================================
elif "Find" in module:
    st.markdown(f"<h1>🏥 Find the Right Hospital</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{MUTED}; font-size:13px;'>Fill in the patient's details to get a care access prediction and referral recommendation.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='font-size:13px; font-weight:700; color:{HEAD}; margin-bottom:8px;'>👤 Patient Information</div>", unsafe_allow_html=True)
        age_group = st.selectbox("Patient Age Group", ["0–4 (Infant)", "5–14 (Child)", "15–24 (Young Adult)", "25–34 (Adult)", "35–49 (Adult)", "50–64 (Older Adult)", "65+ (Elderly)"])
        gender    = st.selectbox("Gender", ["Female", "Male"])
        residence = st.radio("Lives in", ["Urban area (city/town)", "Rural area (village)"], horizontal=True)

    with col2:
        st.markdown(f"<div style='font-size:13px; font-weight:700; color:{HEAD}; margin-bottom:8px;'>📍 Access Factors</div>", unsafe_allow_html=True)
        wealth_index = st.select_slider("Household Wealth Level", options=["Very Poor", "Poor", "Middle", "Comfortable", "Wealthy"])
        insurance    = st.radio("Has Health Insurance?", ["Yes", "No"], horizontal=True)
        distance_km  = st.slider("Distance to Nearest Hospital (km)", 0.0, 100.0, 5.0, 0.5)

    if distance_km > 25:
        st.markdown(f'<div class="card card-red"><b style="color:{RED};">⚠️ Beyond the 25km safe zone.</b> <span style="font-size:12px;color:{MUTED};">Access drops sharply here. Consider mobile clinic or ambulance dispatch.</span></div>', unsafe_allow_html=True)
    elif distance_km > 15:
        st.markdown(f'<div class="card card-gold"><span style="font-size:12px;color:{GOLD};">⚡ Caution zone (15–25km). Monitor and consider outreach support.</span></div>', unsafe_allow_html=True)

    clinical_notes = st.text_area("Any notes about the patient (optional)", placeholder="e.g. Patient has difficulty walking, no transport access...", height=80)

    if st.button("🔍 Check Access Likelihood"):
        age_map    = {"0–4 (Infant)": "0-4", "5–14 (Child)": "5-14", "15–24 (Young Adult)": "15-24", "25–34 (Adult)": "25-34", "35–49 (Adult)": "35-49", "50–64 (Older Adult)": "50-64", "65+ (Elderly)": "65+"}
        wealth_map = {"Very Poor": "Poorest", "Poor": "Poorer", "Middle": "Middle", "Comfortable": "Richer", "Wealthy": "Richest"}
        payload = {
            "distance_km": distance_km, "age_group": age_map.get(age_group, "25-34"),
            "gender": gender, "wealth_index": wealth_map.get(wealth_index, "Middle"),
            "insurance_status": 1 if insurance == "Yes" else 0,
            "residential_area_group": "Urban" if "Urban" in residence else "Rural",
            "survey_weight": 1.0, "clinical_notes": clinical_notes
        }
        try:
            with st.spinner("Running prediction..."):
                response = requests.post("http://127.0.0.1:8000/predict_access", json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                prob   = result["probability"]
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("Likelihood of Accessing Care", f"{prob}%")
                m2.metric("Recommendation", "✅ Likely to access" if result["prediction"] == 1 else "❌ At risk")
                m3.metric("Distance Risk", "⚠️ High" if distance_km > 25 else "✅ Safe zone")
                st.progress(prob / 100)

                if prob >= 70:
                    st.markdown(f'<div class="card card-accent"><b style="color:{ACCENT};">✅ Good news.</b> <span style="font-size:13px;color:{MUTED};">This patient is likely to access care. Proceed with standard referral.</span></div>', unsafe_allow_html=True)
                elif prob >= 40:
                    st.markdown(f'<div class="card card-gold"><b style="color:{GOLD};">⚡ Some concern.</b> <span style="font-size:13px;color:{MUTED};">This patient may face barriers. Consider calling ahead or arranging transport.</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="card card-red"><b style="color:{RED};">🚨 High risk.</b> <span style="font-size:13px;color:{MUTED};">This patient is unlikely to access care without help. Prioritise for community health worker or mobile clinic.</span></div>', unsafe_allow_html=True)

                st.markdown(f"<h3 style='margin-top:20px;'>📋 Recommended Nearby Facilities</h3>", unsafe_allow_html=True)
                nearby = FACILITIES[FACILITIES["Dist_km"] <= distance_km + 10].sort_values("Access_pct", ascending=False).head(3)
                for _, row in nearby.iterrows():
                    st.markdown(f"""
                    <div class='card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <div style='font-size:14px; font-weight:700; color:{HEAD};'>{row['Name']}</div>
                                <div style='font-size:11px; color:{MUTED}; margin-top:3px;'>{row['Type']} · {row['Sector']} · {row['Dist_km']} km away</div>
                                <div style='margin-top:6px;'>
                                    <span class='badge badge-green'>Access: {row['Access_pct']}%</span>
                                    <span class='badge badge-gold'>Retention: {row['Retention_pct']}%</span>
                                    <span class='badge badge-purple'>{row['Sector']}</span>
                                </div>
                            </div>
                            <a class='call-btn' href='tel:{row["Phone"]}'>📞 Call</a>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("🚨 Prediction engine not running. Start the API server first.")


# ============================================================
# FACILITY MAP
# ============================================================
elif "Map" in module:
    st.markdown(f"<h1>🗺️ Nairobi Facility Map</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{MUTED}; font-size:13px;'>Find hospitals near you · Call directly · Filter by sector · Plan a route</p>", unsafe_allow_html=True)

    # Location planner
    st.markdown(f'<div class="plain-box"><b>📍 Plan a Patient Journey</b><br>Enter the patient\'s current location and destination hospital to open directions in Google Maps.</div>', unsafe_allow_html=True)
    loc1, loc2, loc3 = st.columns([2, 2, 1])
    with loc1:
        current_loc = st.text_input("Patient's Current Location", placeholder="e.g. Westlands, Nairobi")
    with loc2:
        destination = st.text_input("Destination Hospital", placeholder="e.g. Kenyatta National Hospital")
    with loc3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗺️ Directions"):
            if current_loc and destination:
                maps_url = f"https://www.google.com/maps/dir/{current_loc.replace(' ', '+')}/{destination.replace(' ', '+')}"
                st.markdown(f"<a href='{maps_url}' target='_blank' class='call-btn'>Open in Google Maps →</a>", unsafe_allow_html=True)

    st.markdown("---")

    f1, f2, f3 = st.columns(3)
    with f1: max_dist       = st.slider("Show facilities within (km)", 1, 60, 30)
    with f2: sector_filter  = st.multiselect("Filter by Sector", ["Public", "Faith-Based", "Private"], default=["Public", "Faith-Based", "Private"])
    with f3: show_threshold = st.checkbox("Show 25km safety zone ring", value=True)

    filtered = FACILITIES[(FACILITIES["Dist_km"] <= max_dist) & (FACILITIES["Sector"].isin(sector_filter))]

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Facilities Shown",  len(filtered))
    s2.metric("Avg Access Rate",   f"{filtered['Access_pct'].mean():.1f}%")
    s3.metric("Faith-Based",       int((filtered["Sector"] == "Faith-Based").sum()))
    s4.metric("High-Risk Flagged", int(filtered["Paradox"].sum()))

    m = folium.Map(location=[-1.2921, 36.8219], zoom_start=11, tiles=MAP_TILE)

    if show_threshold:
        folium.Circle(
            location=[-1.3006, 36.8066], radius=25000,
            color="#F5A623", weight=2, fill=True, fill_color="#F5A623", fill_opacity=0.05,
            tooltip="25km GAM Critical Threshold"
        ).add_to(m)

    for _, row in filtered.iterrows():
        icon_color  = "red" if row["Paradox"] else SECTOR_COLORS.get(row["Sector"], "blue")
        paradox_txt = "<br><b style='color:red;'>⚠️ Urban Paradox — patients nearby still not accessing care</b>" if row["Paradox"] else ""
        popup_html  = f"""
        <div style='font-family:Arial; min-width:200px;'>
            <b style='font-size:13px;'>{row['Name']}</b><br>
            <span style='color:#666; font-size:11px;'>{row['Type']} · {row['Sector']}</span><br><br>
            📍 Distance: <b>{row['Dist_km']} km</b><br>
            ✅ Access Rate: <b>{row['Access_pct']}%</b><br>
            🔄 Retention Rate: <b>{row['Retention_pct']}%</b><br>
            💊 Insurance Coverage: <b>{row['Insurance_pct']}%</b><br><br>
            <a href='tel:{row["Phone"]}' style='background:#007A5A;color:white;padding:5px 12px;border-radius:6px;text-decoration:none;font-size:12px;font-weight:bold;'>📞 Call Now</a>
            {paradox_txt}
        </div>"""
        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            tooltip=f"{row['Name']} ({row['Sector']})",
            popup=folium.Popup(popup_html, max_width=260),
            icon=folium.Icon(color=icon_color, icon=SECTOR_ICONS.get(row["Sector"], "medkit"), prefix="fa")
        ).add_to(m)

    map_data = st_folium(m, width="100%", height=460, returned_objects=["last_clicked"])

    st.markdown(f"""
    <div style='display:flex; gap:20px; margin-top:10px; flex-wrap:wrap; font-size:12px; color:{MUTED};'>
        <span>🔵 Public Hospital</span>
        <span>🟣 Faith-Based / Religious Hospital</span>
        <span>🟢 Private Hospital</span>
        <span>🔴 High-Risk Facility (Urban Paradox)</span>
        <span>🟡 25km Safety Zone</span>
        <span style='color:{ACCENT};'>💡 Click anywhere on the map to find the nearest facility</span>
    </div>""", unsafe_allow_html=True)

    # ── Click handler ─────────────────────────────────────────
    if map_data and map_data.get("last_clicked"):
        import math

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
            return R * 2 * math.asin(math.sqrt(a))

        clat = map_data["last_clicked"]["lat"]
        clng = map_data["last_clicked"]["lng"]

        # Distance from click to every facility
        FACILITIES["click_dist"] = FACILITIES.apply(
            lambda r: haversine(clat, clng, r["Lat"], r["Lon"]), axis=1
        )
        nearest = FACILITIES.nsmallest(3, "click_dist")
        closest = nearest.iloc[0]

        zone_label = f"✅ Within 25km safe zone" if closest["click_dist"] <= 25 else f"⚠️ Beyond 25km — access risk zone"
        zone_color = ACCENT if closest["click_dist"] <= 25 else RED

        st.markdown(f"""
        <div class='card' style='border-left:4px solid {zone_color}; margin-top:16px;'>
            <div style='font-size:13px; font-weight:700; color:{zone_color}; margin-bottom:8px;'>
                📍 You clicked at ({clat:.4f}, {clng:.4f}) — {zone_label}
            </div>
            <div style='font-size:12px; color:{MUTED}; margin-bottom:12px;'>
                Distance from click to nearest facility: <b style='color:{HEAD};'>{closest['click_dist']:.1f} km</b>
            </div>
            <div style='font-size:12px; font-weight:700; color:{HEAD}; margin-bottom:6px;'>3 Nearest Facilities:</div>
        """, unsafe_allow_html=True)

        for _, row in nearest.iterrows():
            d = row["click_dist"]
            d_color = ACCENT if d <= 25 else GOLD if d <= 40 else RED
            access_badge = "badge-green" if row["Access_pct"] >= 70 else "badge-gold" if row["Access_pct"] >= 50 else "badge-red"
            sector_badge = "badge-purple" if row["Sector"] == "Faith-Based" else "badge-green" if row["Sector"] == "Private" else "badge-sky"
            st.markdown(f"""
            <div class='card' style='margin-bottom:8px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <div style='font-size:13px; font-weight:700; color:{HEAD};'>{row['Name']}</div>
                        <div style='font-size:11px; color:{MUTED}; margin:3px 0 6px;'>{row['Type']} · {row['Sector']}</div>
                        <span class='badge {sector_badge}'>{row['Sector']}</span>
                        <span class='badge {access_badge}'>Access: {row['Access_pct']}%</span>
                        <span class='badge badge-gold'>Retention: {row['Retention_pct']}%</span>
                        {'<span class="badge badge-red">⚠️ High-Risk</span>' if row["Paradox"] else ''}
                    </div>
                    <div style='text-align:right; min-width:130px;'>
                        <div style='font-size:16px; font-weight:800; color:{d_color};'>{d:.1f} km</div>
                        <div style='font-size:10px; color:{MUTED}; margin-bottom:6px;'>from your click</div>
                        <a class='call-btn' href='tel:{row["Phone"]}'>📞 Call</a>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='margin-top:24px;'>📋 Facility Directory</h3>", unsafe_allow_html=True)
    for _, row in filtered.sort_values("Dist_km").iterrows():
        access_badge  = "badge-red"    if row["Access_pct"] < 50 else "badge-gold" if row["Access_pct"] < 70 else "badge-green"
        sector_badge  = "badge-purple" if row["Sector"] == "Faith-Based" else "badge-green" if row["Sector"] == "Private" else "badge-sky"
        card_class    = "card-red" if row["Paradox"] else "card-accent"
        st.markdown(f"""
        <div class='card {card_class}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'>
                    <div style='font-size:14px; font-weight:700; color:{HEAD};'>{row['Name']}</div>
                    <div style='font-size:11px; color:{MUTED}; margin:4px 0 8px;'>{row['Type']} · {row['Dist_km']} km away</div>
                    <span class='badge {sector_badge}'>{row['Sector']}</span>
                    <span class='badge {access_badge}'>Access: {row['Access_pct']}%</span>
                    <span class='badge badge-gold'>Retention: {row['Retention_pct']}%</span>
                    {'<span class="badge badge-red">⚠️ High-Risk</span>' if row["Paradox"] else ''}
                </div>
                <div style='text-align:right; min-width:120px;'>
                    <div style='font-size:10px; color:{MUTED}; margin-bottom:6px;'>{row["Phone"]}</div>
                    <a class='call-btn' href='tel:{row["Phone"]}'>📞 Call Facility</a>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# ACCESS & RETENTION
# ============================================================
elif "Access" in module:
    st.markdown(f"<h1>📊 Access & Retention Rates</h1>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='plain-box'>
        <b>Access rate</b> = % of patients who successfully reach and use a health facility.<br>
        <b>Retention rate</b> = % of patients who <i>come back</i> for follow-up care.<br>
        A big gap between the two means patients visit once but don't return — often due to poor service quality or cost.
    </div>""", unsafe_allow_html=True)

    fac_types   = ["National Referral", "County Hospital", "Sub-County", "Health Centre", "Dispensary/Clinic"]
    access_vals = [94, 79, 61, 52, 37]
    ret_vals    = [89, 71, 53, 44, 30]
    gap_vals    = [a - r for a, r in zip(access_vals, ret_vals)]

    # Always-visible label colour — dark in light mode, light in dark mode
    TICK_COL = "#FFFFFF" if st.session_state.dark_mode else "#1A1A2E"

    c_l, c_r = st.columns(2)
    with c_l:
        st.markdown(f"<h3>Who is accessing care?</h3>", unsafe_allow_html=True)
        fig_a = go.Figure(go.Bar(x=access_vals, y=fac_types, orientation="h",
            marker_color=[ACCENT if v >= 50 else RED for v in access_vals],
            text=[f"{v}%" for v in access_vals], textposition="outside",
            textfont=dict(color=TICK_COL, size=13)))
        fig_a.update_layout(paper_bgcolor=CARD, plot_bgcolor=CARD, height=280,
            margin=dict(l=0, r=60, t=10, b=10),
            xaxis=dict(showgrid=False, range=[0, 110], tickfont=dict(color=TICK_COL)),
            yaxis=dict(tickfont=dict(color=TICK_COL, size=13)),
            showlegend=False)
        st.plotly_chart(fig_a, use_container_width=True)

    with c_r:
        st.markdown(f"<h3>Who is NOT coming back?</h3>", unsafe_allow_html=True)
        fig_g = go.Figure(go.Bar(x=gap_vals, y=fac_types, orientation="h",
            marker_color=[RED if g > 12 else GOLD if g > 8 else ACCENT for g in gap_vals],
            text=[f"{v}pp gap" for v in gap_vals], textposition="outside",
            textfont=dict(color=TICK_COL, size=13)))
        fig_g.update_layout(paper_bgcolor=CARD, plot_bgcolor=CARD, height=280,
            margin=dict(l=0, r=90, t=10, b=10),
            xaxis=dict(showgrid=False, range=[0, 25], tickfont=dict(color=TICK_COL),
                       title=dict(text="Access–Retention gap (pp)", font=dict(color=TICK_COL))),
            yaxis=dict(tickfont=dict(color=TICK_COL, size=13)),
            showlegend=False)
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown(f"""
    <div class='card card-red'>
        <b style='color:{RED};'>⚠️ Urban Proximity Paradox</b><br>
        <span style='font-size:12px; color:{MUTED};'>
        3,484 patients lived close to a hospital but still did not access care.
        Simply building hospitals nearby is not enough — service quality, cost, and wait times must also improve.
        </span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# HOW IT WORKS
# ============================================================
elif "Works" in module:
    st.markdown(f"<h1>🔬 How the Prediction Works</h1>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='plain-box'>
        <b>In plain English:</b><br><br>
        The system looks at information about a patient — like how far they live from a hospital,
        whether they have insurance, and how wealthy their household is — and calculates the
        <b>chance they will actually go to hospital</b> when they need care.<br><br>
        It was trained on data from <b>99,031 real Kenyans</b>.
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<h3>What matters most?</h3>", unsafe_allow_html=True)
    cat_colors = {"Enabling": GOLD, "Predisposing": PURPLE, "Need": ACCENT}
    fig_shap = go.Figure(go.Bar(
        x=SHAP_DATA["Importance"]*100, y=SHAP_DATA["Plain"], orientation="h",
        marker_color=[cat_colors[c] for c in SHAP_DATA["Category"]],
        text=[f"{v*100:.0f}%" for v in SHAP_DATA["Importance"]], textposition="outside"))
    fig_shap.update_layout(paper_bgcolor=CARD, plot_bgcolor=CARD, font_color=TEXT, height=340,
        xaxis=dict(title="How much this factor influences access (%)", color=MUTED, gridcolor=BORDER, range=[0,55]),
        yaxis=dict(color=TEXT, autorange="reversed"), margin=dict(l=10,r=60,t=10,b=10))
    st.plotly_chart(fig_shap, use_container_width=True)

    lc1, lc2, lc3 = st.columns(3)
    for col, (title, color, desc) in zip([lc1,lc2,lc3],[
        ("Structural Factors", GOLD,   "Distance, money, insurance — things that help or block access"),
        ("Personal Factors",   PURPLE, "Age, gender, education, where you live"),
        ("Health Need",        ACCENT, "Type of facility or care being sought"),
    ]):
        col.markdown(f'<div class="card" style="border-left:4px solid {color}; text-align:center;"><div style="font-size:11px;font-weight:700;color:{color};">{title}</div><div style="font-size:10px;color:{MUTED};margin-top:4px;line-height:1.6;">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown(f"<h3 style='margin-top:20px;'>📍 The 25km Rule</h3>", unsafe_allow_html=True)
    fig_gam = go.Figure()
    fig_gam.add_trace(go.Scatter(x=GAM_DIST, y=[p*100 for p in GAM_PROB], mode="lines+markers",
        line=dict(color=ACCENT, width=3), marker=dict(size=7, color=ACCENT),
        fill="tozeroy", fillcolor=f"{ACCENT}18", name="Chance of accessing care"))
    fig_gam.add_vline(x=25, line_dash="dash", line_color=GOLD, line_width=2,
        annotation_text="25km — access drops sharply here",
        annotation_font_color=GOLD, annotation_position="top right")
    fig_gam.update_layout(paper_bgcolor=CARD, plot_bgcolor=CARD, font_color=TEXT, height=300,
        xaxis=dict(title="Distance to nearest hospital (km)", color=MUTED, gridcolor=BORDER),
        yaxis=dict(title="Chance of accessing care (%)", color=MUTED, gridcolor=BORDER, range=[0,110]),
        margin=dict(l=20,r=20,t=20,b=20), showlegend=False)
    st.plotly_chart(fig_gam, use_container_width=True)

    st.markdown(f"""
    <div class='card card-gold'>
        <b style='color:{GOLD};'>💡 What this means for hospital planning</b><br>
        <span style='font-size:12px;color:{MUTED};'>
        Patients can still access care up to <b>25km away</b> — but beyond that, access drops dramatically.
        Mobile clinics and ambulance services should prioritise areas <b>beyond 25km</b>.
        </span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# MODEL RESULTS
# ============================================================
elif "Results" in module:
    st.markdown(f"<h1>⚙️ Model Performance Results</h1>", unsafe_allow_html=True)
    st.caption("For supervisors and researchers · Stratified 3-Fold Cross-Validation · KNBS 2022 · n=99,031")

    def style_row(row):
        if row["Algorithm"] == "XGBoost (Best Model)":
            return [f"background-color:{ACCENT}22; color:{ACCENT}; font-weight:700"] * len(row)
        return [f"color:{TEXT}"] * len(row)

    st.dataframe(MODEL_PERF.drop(columns=["Top"]).style.apply(style_row, axis=1),
                 use_container_width=True, hide_index=True)

    st.markdown("---")
    fig_m = go.Figure()
    for col_name, color in [("F1", ACCENT), ("AUC", SKY), ("Accuracy", PURPLE)]:
        fig_m.add_trace(go.Bar(name=col_name, x=MODEL_PERF["Algorithm"], y=MODEL_PERF[col_name], marker_color=color, opacity=0.85))
    fig_m.update_layout(barmode="group", paper_bgcolor=CARD, plot_bgcolor=CARD, font_color=TEXT, height=340,
        xaxis=dict(color=MUTED, gridcolor=BORDER, tickangle=-25),
        yaxis=dict(color=MUTED, gridcolor=BORDER, range=[0,1.05]),
        legend=dict(bgcolor=SURFACE, bordercolor=BORDER), margin=dict(l=10,r=10,t=10,b=80))
    st.plotly_chart(fig_m, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="card card-red"><b style="color:{RED};">⚖️ Class Imbalance</b><br><span style="font-size:11px;color:{MUTED};">Most survey respondents accessed care, so the model needed special tuning to also detect those who did not. Result: 3,484 False Positives · 5 False Negatives.</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card card-accent"><b style="color:{ACCENT};">✅ Why XGBoost Was Chosen</b><br><span style="font-size:11px;color:{MUTED};">Best balance of accuracy and fairness (AUC 0.6524, F1 0.9034). The combined model offered no meaningful improvement, so XGBoost alone was deployed.</span></div>', unsafe_allow_html=True)
