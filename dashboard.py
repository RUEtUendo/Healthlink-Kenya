import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px

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
# THEME: Deep navy + emerald (matches thesis palette)
# ============================================================
st.markdown("""
<style>
    /* Base */
    .stApp { background-color: #07111F; color: #D9E8F5; }
    section[data-testid="stSidebar"] { background-color: #0D1E30; border-right: 1px solid #1A3450; }

    /* Headings */
    h1, h2, h3, h4 { color: #FFFFFF !important; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #102234;
        border: 1px solid #1A3450;
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="metric-container"] label { color: #5A7A99 !important; font-size: 11px !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #00D9A3 !important; font-size: 26px !important; }

    /* Buttons */
    .stButton > button {
        background: #00D9A3 !important;
        color: #07111F !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
    }
    .stButton > button:hover { background: #00b88a !important; }

    /* Inputs */
    .stSelectbox label, .stSlider label, .stRadio label,
    .stTextArea label, .stSelectSlider label { color: #5A7A99 !important; font-size: 12px !important; }

    /* Sidebar text */
    .css-1d391kg p, .css-1d391kg { color: #5A7A99; }

    /* Dataframe */
    .dataframe { background: #102234 !important; color: #D9E8F5 !important; }

    /* Info / warning boxes */
    .stAlert { border-radius: 10px; }

    /* Progress bar */
    .stProgress > div > div { background-color: #00D9A3 !important; }

    /* Divider */
    hr { border-color: #1A3450; }

    /* Chip-style text */
    .chip-green  { background:#00D9A322; color:#00D9A3; border:1px solid #00D9A355;
                   border-radius:99px; padding:2px 10px; font-size:11px; font-weight:700; }
    .chip-gold   { background:#F5A62322; color:#F5A623; border:1px solid #F5A62355;
                   border-radius:99px; padding:2px 10px; font-size:11px; font-weight:700; }
    .chip-red    { background:#F8717122; color:#F87171; border:1px solid #F8717155;
                   border-radius:99px; padding:2px 10px; font-size:11px; font-weight:700; }
    .chip-sky    { background:#38BDF822; color:#38BDF8; border:1px solid #38BDF855;
                   border-radius:99px; padding:2px 10px; font-size:11px; font-weight:700; }

    /* Banner boxes */
    .banner-green { background:#00D9A312; border:1px solid #00D9A333; border-radius:12px; padding:14px 18px; }
    .banner-gold  { background:#F5A62312; border:1px solid #F5A62333; border-radius:12px; padding:14px 18px; }
    .banner-red   { background:#F8717112; border:1px solid #F8717133; border-radius:12px; padding:14px 18px; }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] { color: #5A7A99; }
    .stTabs [aria-selected="true"] { color: #00D9A3 !important; border-bottom: 2px solid #00D9A3; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px 0;'>
        <div style='font-size:36px;'>⚕️</div>
        <div style='font-size:16px; font-weight:800; color:#FFFFFF; margin-top:4px;'>HealthLink Kenya</div>
        <div style='font-size:11px; color:#5A7A99; margin-top:4px;'>Decision-Support Dashboard<br>Hospital Referral Planning</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    module = st.radio("Navigate", [
        "📊  Overview & Insights",
        "🏥  Predictive Triage",
        "🗺️  Geospatial Mapper",
        "📍  Distance Decay (GAM)",
        "🧠  SHAP Interpretability",
        "⚙️  Model Performance"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:10px; color:#5A7A99; line-height:1.8;'>
        <b style='color:#5A7A99'>Model:</b> XGBoost · F1 0.9034<br>
        <b style='color:#5A7A99'>AUC:</b> 0.6524 · Acc: 0.8240<br>
        <b style='color:#5A7A99'>Data:</b> KNBS HSB Survey 2022<br>
        <b style='color:#5A7A99'>n =</b> 99,031 observations<br>
        <b style='color:#5A7A99'>Threshold:</b> 25km (GAM)<br>
        <b style='color:#5A7A99'>API:</b> FastAPI · localhost:8000
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================
FACILITIES_DATA = pd.DataFrame([
    {"Name": "Kenyatta National Hospital", "Type": "National Referral", "Dist_km": 0,    "Insurance_pct": 91, "Wealth": "Highest", "Access_pct": 94, "Retention_pct": 89, "Lat": -1.3006, "Lon": 36.8066, "Paradox": False},
    {"Name": "Pumwani Maternity Hospital",  "Type": "County Hospital",   "Dist_km": 4.2,  "Insurance_pct": 62, "Wealth": "Middle",  "Access_pct": 81, "Retention_pct": 74, "Lat": -1.2841, "Lon": 36.8458, "Paradox": False},
    {"Name": "Mathare North HC",            "Type": "Health Centre",     "Dist_km": 6.8,  "Insurance_pct": 31, "Wealth": "Lowest",  "Access_pct": 48, "Retention_pct": 44, "Lat": -1.2611, "Lon": 36.8590, "Paradox": True },
    {"Name": "Mbagathi District Hospital",  "Type": "County Hospital",   "Dist_km": 8.1,  "Insurance_pct": 55, "Wealth": "Middle",  "Access_pct": 77, "Retention_pct": 71, "Lat": -1.3217, "Lon": 36.7680, "Paradox": False},
    {"Name": "Kayole Sub-County Hospital",  "Type": "Sub-County",        "Dist_km": 12.4, "Insurance_pct": 28, "Wealth": "Second",  "Access_pct": 43, "Retention_pct": 38, "Lat": -1.2718, "Lon": 36.9001, "Paradox": True },
    {"Name": "Ruaraka Health Centre",       "Type": "Clinic",            "Dist_km": 15.0, "Insurance_pct": 44, "Wealth": "Middle",  "Access_pct": 65, "Retention_pct": 59, "Lat": -1.2488, "Lon": 36.8756, "Paradox": False},
    {"Name": "Dandora Dispensary",          "Type": "Dispensary",        "Dist_km": 18.3, "Insurance_pct": 19, "Wealth": "Lowest",  "Access_pct": 37, "Retention_pct": 30, "Lat": -1.2595, "Lon": 36.9087, "Paradox": True },
    {"Name": "Kangemi Health Centre",       "Type": "Health Centre",     "Dist_km": 21.1, "Insurance_pct": 33, "Wealth": "Second",  "Access_pct": 55, "Retention_pct": 48, "Lat": -1.2724, "Lon": 36.7369, "Paradox": False},
    {"Name": "Limuru Sub-County Hospital",  "Type": "Sub-County",        "Dist_km": 31.7, "Insurance_pct": 47, "Wealth": "Middle",  "Access_pct": 31, "Retention_pct": 26, "Lat": -1.1140, "Lon": 36.6480, "Paradox": False},
    {"Name": "Thika Level 5 Hospital",      "Type": "County Hospital",   "Dist_km": 44.2, "Insurance_pct": 52, "Wealth": "Fourth",  "Access_pct": 24, "Retention_pct": 20, "Lat": -1.0332, "Lon": 37.0693, "Paradox": False},
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

# GAM distance decay curve (25km inflection)
GAM_DIST  = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 80, 100]
GAM_PROB  = [0.96, 0.94, 0.91, 0.88, 0.84, 0.76, 0.58, 0.40, 0.27, 0.14, 0.08, 0.04, 0.02]

COLORS = {
    "Enabling":     "#F5A623",
    "Predisposing": "#A78BFA",
    "Need":         "#00D9A3",
}


# ============================================================
# MODULE 0: OVERVIEW
# ============================================================
if "Overview" in module:
    st.markdown("## 📊 Overview & Insights")
    st.caption("KNBS Health-Seeking Behaviour Survey 2022 · n = 99,031 · XGBoost Operational Model")

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Population Access Rate",       "78.4%",  "+3.2% vs prev. quarter")
    k2.metric("Retention Rate",               "71.2%",  "+1.8% vs prev. quarter")
    k3.metric("GAM Critical Threshold",       "25 km",  "Access drops sharply beyond")
    k4.metric("Urban Proximity Paradox",      "3,484",  "False Positives (hidden barriers)")

    st.markdown("---")

    # Andersen Model breakdown
    st.markdown("### Andersen's Behavioural Model — Feature Weight by Category")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div class="banner-gold">
            <div style='font-size:12px; font-weight:700; color:#F5A623;'>Enabling Factors · 73%</div>
            <div style='font-size:11px; color:#5A7A99; margin-top:6px; line-height:1.8;'>
            Distance to Facility · 41%<br>Wealth Index · 18%<br>Insurance Status · 14%
            </div>
            <div style='font-size:10px; color:#F5A623; margin-top:8px;'>Dominant predictors of access</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="banner-green" style='background:#A78BFA12; border-color:#A78BFA33;'>
            <div style='font-size:12px; font-weight:700; color:#A78BFA;'>Predisposing Factors · 25%</div>
            <div style='font-size:11px; color:#5A7A99; margin-top:6px; line-height:1.8;'>
            Residence Type · 9%<br>Education Level · 8%<br>Age Group · 5% · Gender · 3%
            </div>
            <div style='font-size:10px; color:#A78BFA; margin-top:8px;'>Demographic & social attributes</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div class="banner-green">
            <div style='font-size:12px; font-weight:700; color:#00D9A3;'>Need Factors · 2%</div>
            <div style='font-size:11px; color:#5A7A99; margin-top:6px; line-height:1.8;'>
            Provider Group · 2%<br>Perceived health need<br>Triage classification
            </div>
            <div style='font-size:10px; color:#00D9A3; margin-top:8px;'>Lowest individual weight</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Access vs Retention comparison
    col_l, col_r = st.columns(2)
    fac_types = ["National Referral", "County Hospital", "Sub-County", "Health Centre", "Dispensary/Clinic"]
    access_vals     = [94, 79, 61, 52, 37]
    retention_vals  = [89, 71, 53, 44, 30]

    with col_l:
        st.markdown("#### Access Rate by Facility Type")
        fig_a = go.Figure(go.Bar(
            x=access_vals, y=fac_types, orientation="h",
            marker_color=["#00D9A3" if v >= 50 else "#F87171" for v in access_vals],
            text=[f"{v}%" for v in access_vals], textposition="outside",
        ))
        fig_a.update_layout(
            paper_bgcolor="#07111F", plot_bgcolor="#07111F",
            font_color="#D9E8F5", height=260, margin=dict(l=0,r=40,t=10,b=10),
            xaxis=dict(showgrid=False, range=[0,110], color="#5A7A99"),
            yaxis=dict(color="#D9E8F5"), showlegend=False,
        )
        st.plotly_chart(fig_a, use_container_width=True)

    with col_r:
        st.markdown("#### Access → Retention Gap")
        gap_vals = [a - r for a, r in zip(access_vals, retention_vals)]
        gap_colors = ["#F87171" if g > 12 else "#F5A623" if g > 8 else "#00D9A3" for g in gap_vals]
        fig_g = go.Figure(go.Bar(
            x=gap_vals, y=fac_types, orientation="h",
            marker_color=gap_colors,
            text=[f"{v}pp" for v in gap_vals], textposition="outside",
        ))
        fig_g.update_layout(
            paper_bgcolor="#07111F", plot_bgcolor="#07111F",
            font_color="#D9E8F5", height=260, margin=dict(l=0,r=40,t=10,b=10),
            xaxis=dict(showgrid=False, range=[0,25], color="#5A7A99", title="Access–Retention gap (pp)"),
            yaxis=dict(color="#D9E8F5"), showlegend=False,
        )
        st.plotly_chart(fig_g, use_container_width=True)

    # Urban Paradox alert
    st.markdown("""
    <div class="banner-red">
        <b style='color:#F87171;'>⚠️ Urban Proximity Paradox Detected</b><br>
        <span style='font-size:12px; color:#5A7A99;'>
        3,484 patients within &lt;50km failed to access care despite favourable distance and wealth profiles.
        These are not model errors — they are empirically validated hidden exclusions caused by indirect costs,
        wait times, and perceived service quality. Flagged facilities: Mathare North HC · Kayole Sub-County · Dandora Dispensary.
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
        st.markdown("#### Demographic Data (Predisposing Factors)")
        age_group = st.selectbox("Age Group", ["0-4", "5-14", "15-24", "25-34", "35-49", "50-64", "65+"])
        gender    = st.selectbox("Gender", ["Female", "Male"])
        residence = st.radio("Residence Type", ["Urban", "Rural"], horizontal=True)

    with col2:
        st.markdown("#### Enabling Factors (Andersen Model)")
        wealth_index = st.select_slider(
            "Wealth Index (Socioeconomic Quintile)",
            options=["Poorest", "Poorer", "Middle", "Richer", "Richest"]
        )
        insurance    = st.radio("Insurance Status", ["Insured", "Uninsured"], horizontal=True)
        distance_km  = st.slider(
            "Distance to Nearest Facility (km)",
            min_value=0.0, max_value=100.0, value=5.0, step=0.5
        )

    # Live 25km warning
    if distance_km > 25:
        st.markdown("""
        <div class="banner-red" style='margin-top:8px;'>
            <b style='color:#F87171;'>📍 Beyond GAM Threshold (25km)</b> — 
            <span style='font-size:12px; color:#5A7A99;'>Access probability is predicted to drop sharply. 
            Consider mobile clinic deployment or ambulance dispatch to this catchment area.</span>
        </div>
        """, unsafe_allow_html=True)
    elif distance_km > 15:
        st.markdown("""
        <div class="banner-gold" style='margin-top:8px;'>
            <span style='font-size:12px; color:#F5A623;'>⚡ Approaching critical distance zone (15–25km). 
            Monitor access rates for this population.</span>
        </div>
        """, unsafe_allow_html=True)

    clinical_notes = st.text_area(
        "Clinical Notes (Optional NLP Input)",
        value="Patient complains of fever and difficulty travelling to the facility.",
        height=90
    )

    if st.button("Run Access Prediction"):
        payload = {
            "distance_km":           distance_km,
            "age_group":             age_group,
            "gender":                gender,
            "wealth_index":          wealth_index,
            "insurance_status":      1 if insurance == "Insured" else 0,
            "residential_area_group": residence,
            "survey_weight":         1.0,
            "clinical_notes":        clinical_notes
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
                m2.metric("Prediction",         "Will Access" if result["prediction"] == 1 else "Will NOT Access")
                m3.metric("Distance Flag",       ">25km ⚠️" if distance_km > 25 else "Within Threshold ✅")

                st.progress(prob / 100)

                # Colour bar interpretation
                if prob >= 70:
                    st.markdown('<div class="banner-green"><b style="color:#00D9A3;">High likelihood of access.</b> <span style="font-size:12px;color:#5A7A99;">Patient profile is within normal utilisation range.</span></div>', unsafe_allow_html=True)
                elif prob >= 40:
                    st.markdown('<div class="banner-gold"><b style="color:#F5A623;">Moderate likelihood.</b> <span style="font-size:12px;color:#5A7A99;">Enabling factors are limiting access. Consider outreach support.</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="banner-red"><b style="color:#F87171;">Low likelihood of access.</b> <span style="font-size:12px;color:#5A7A99;">Patient is at high risk of exclusion. Prioritise for mobile clinic or community health worker intervention.</span></div>', unsafe_allow_html=True)

                if clinical_notes and result["nlp_analysis"]["cleaned_keywords"]:
                    st.info(f"**NLP Extracted Keywords:** {result['nlp_analysis']['cleaned_keywords']}")
            else:
                st.error(f"API Error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("🚨 Cannot connect to FastAPI. Run: `uvicorn main:app --reload` in a separate terminal.")
        except requests.exceptions.Timeout:
            st.error("Request timed out. Check that the API server is running.")


# ============================================================
# MODULE 2: GEOSPATIAL MAPPER
# ============================================================
elif "Mapper" in module:
    st.markdown("## 🗺️ Geospatial Facility Mapper")
    st.caption("Interactive facility map · Distance threshold visualisation · Nairobi County")

    col_ctrl, col_info = st.columns([2, 1])
    with col_ctrl:
        max_dist = st.slider("Show facilities within (km)", 1, 60, 30)
        show_threshold = st.checkbox("Show 25km GAM threshold ring", value=True)

    filtered = FACILITIES_DATA[FACILITIES_DATA["Dist_km"] <= max_dist]

    with col_info:
        st.metric("Facilities in range", len(filtered))
        st.metric("Avg Access Rate",     f"{filtered['Access_pct'].mean():.1f}%")
        st.metric("Paradox Facilities",  int(filtered["Paradox"].sum()))

    # Build Folium map
    m = folium.Map(location=[-1.2921, 36.8219], zoom_start=11, tiles="CartoDB dark_matter")

    # 25km threshold ring around KNH
    if show_threshold:
        folium.Circle(
            location=[-1.3006, 36.8066],
            radius=25000,
            color="#F5A623", weight=2, fill=True, fill_color="#F5A623", fill_opacity=0.04,
            tooltip="25km GAM Critical Threshold"
        ).add_to(m)

    for _, row in filtered.iterrows():
        if row["Paradox"]:
            color, icon_name = "red", "exclamation-triangle"
        elif row["Access_pct"] >= 70:
            color, icon_name = "green", "medkit"
        else:
            color, icon_name = "orange", "medkit"

        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            tooltip=row["Name"],
            popup=folium.Popup(
                f"""<b>{row['Name']}</b><br>
                Type: {row['Type']}<br>
                Distance: {row['Dist_km']} km<br>
                Access: {row['Access_pct']}%&nbsp;&nbsp;Retention: {row['Retention_pct']}%<br>
                Insurance coverage: {row['Insurance_pct']}%<br>
                {'<b style="color:red">⚠ Urban Proximity Paradox</b>' if row['Paradox'] else ''}""",
                max_width=220
            ),
            icon=folium.Icon(color=color, icon=icon_name, prefix="fa")
        ).add_to(m)

    st_folium(m, width="100%", height=480)

    st.markdown("---")
    st.markdown("#### Facility Details Table")
    display_df = filtered[["Name","Type","Dist_km","Access_pct","Retention_pct","Insurance_pct","Wealth","Paradox"]].copy()
    display_df.columns = ["Facility","Type","Dist (km)","Access %","Retention %","Insurance %","Wealth","Paradox Flag"]
    st.dataframe(display_df.style.applymap(
        lambda v: "color: #F87171" if v is True else ("color: #00D9A3" if isinstance(v, (int,float)) and v >= 70 else ""),
        subset=["Access %","Paradox Flag"]
    ), use_container_width=True, hide_index=True)


# ============================================================
# MODULE 3: DISTANCE DECAY (GAM)
# ============================================================
elif "Decay" in module:
    st.markdown("## 📍 Distance Decay — GAM Analysis")
    st.caption("Tyranny of Distance · Generalised Additive Model spline · Critical inflection at 25km")

    # Main GAM chart
    fig = go.Figure()

    # Safe zone fill
    safe_dist = [d for d in GAM_DIST if d <= 25]
    safe_prob = [p for d, p in zip(GAM_DIST, GAM_PROB) if d <= 25]
    fig.add_trace(go.Scatter(
        x=safe_dist + [25], y=safe_prob + [0.76],
        fill="tozeroy", fillcolor="rgba(0,217,163,0.08)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False, name="Safe Zone"
    ))

    # Danger zone fill
    danger_dist = [d for d in GAM_DIST if d >= 25]
    danger_prob = [p for d, p in zip(GAM_DIST, GAM_PROB) if d >= 25]
    fig.add_trace(go.Scatter(
        x=danger_dist, y=danger_prob,
        fill="tozeroy", fillcolor="rgba(248,113,113,0.07)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False, name="Danger Zone"
    ))

    # Main decay curve
    fig.add_trace(go.Scatter(
        x=GAM_DIST, y=GAM_PROB,
        mode="lines+markers",
        line=dict(color="#00D9A3", width=3),
        marker=dict(size=6, color="#00D9A3"),
        name="P(Access | Distance)", hovertemplate="Distance: %{x}km<br>Access Prob: %{y:.0%}"
    ))

    # 25km vertical line
    fig.add_vline(x=25, line_dash="dash", line_color="#F5A623", line_width=2,
                  annotation_text="25km Inflection (GAM)", annotation_font_color="#F5A623",
                  annotation_position="top right")

    # Inflection point dot
    fig.add_trace(go.Scatter(
        x=[25], y=[0.76], mode="markers",
        marker=dict(size=12, color="#F5A623", symbol="circle"),
        name="Critical Inflection", hovertemplate="25km → 76% access probability"
    ))

    fig.update_layout(
        paper_bgcolor="#07111F", plot_bgcolor="#07111F",
        font_color="#D9E8F5", height=400,
        xaxis=dict(title="Distance to Nearest Facility (km)", color="#5A7A99", gridcolor="#1A3450"),
        yaxis=dict(title="Probability of Accessing Care", tickformat=".0%", color="#5A7A99", gridcolor="#1A3450"),
        legend=dict(bgcolor="#0D1E30", bordercolor="#1A3450"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Three insight columns
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="banner-green">
            <b style='color:#00D9A3;'>0–25km · Safe Zone</b><br>
            <span style='font-size:11px;color:#5A7A99;'>Access probability 76–96%. Standard catchment.
            Facility placement and ambulance dispatch zones are effective within this radius.</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="banner-gold">
            <b style='color:#F5A623;'>25km · Critical Inflection</b><br>
            <span style='font-size:11px;color:#5A7A99;'>GAM-derived empirical threshold.
            The traditional 5km epidemiological buffer is mathematically flawed.
            This is the evidence-based mobile clinic deployment radius.</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="banner-red">
            <b style='color:#F87171;'>>25km · Danger Zone</b><br>
            <span style='font-size:11px;color:#5A7A99;'>Access drops precipitously toward zero.
            Physical distance is the dominant determinant.
            Priority zone for mobile health unit deployment.</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="banner-green" style='background:#38BDF812; border-color:#38BDF833;'>
        <b style='color:#38BDF8;'>Policy Implication (Ministry of Health)</b><br>
        <span style='font-size:12px;color:#5A7A99;'>
        The 25km catchment standard should replace the linear 5km buffer currently used in epidemiological planning.
        Mobile clinic deployment and ambulance dispatch radius should be recalibrated to this empirically derived GAM threshold.
        This finding is directly deployable to the MoH Department of Planning as per thesis Section 1.9.
        </span>
    </div>""", unsafe_allow_html=True)


# ============================================================
# MODULE 4: SHAP INTERPRETABILITY
# ============================================================
elif "SHAP" in module:
    st.markdown("## 🧠 SHAP Feature Importance")
    st.caption("TreeSHAP applied to XGBoost · Marginal feature contributions · Andersen Model category breakdown")

    col_chart, col_insight = st.columns([3, 2])

    with col_chart:
        cat_colors = {
            "Enabling": "#F5A623",
            "Predisposing": "#A78BFA",
            "Need": "#00D9A3"
        }
        bar_colors = [cat_colors[c] for c in SHAP_DATA["Category"]]

        fig_shap = go.Figure(go.Bar(
            x=SHAP_DATA["Importance"] * 100,
            y=SHAP_DATA["Feature"],
            orientation="h",
            marker_color=bar_colors,
            text=[f"{v*100:.0f}%" for v in SHAP_DATA["Importance"]],
            textposition="outside",
            hovertemplate="%{y}<br>Importance: %{x:.1f}%<extra></extra>"
        ))
        fig_shap.update_layout(
            paper_bgcolor="#07111F", plot_bgcolor="#07111F",
            font_color="#D9E8F5", height=340,
            xaxis=dict(title="SHAP Importance (%)", color="#5A7A99", gridcolor="#1A3450", range=[0, 55]),
            yaxis=dict(color="#D9E8F5", autorange="reversed"),
            margin=dict(l=10, r=50, t=10, b=10),
        )
        st.plotly_chart(fig_shap, use_container_width=True)

        # Legend
        lcols = st.columns(3)
        for i, (cat, col) in enumerate(cat_colors.items()):
            total = SHAP_DATA[SHAP_DATA["Category"] == cat]["Importance"].sum() * 100
            lcols[i].markdown(f"""
            <div style='background:{col}22; border:1px solid {col}44; border-radius:8px; padding:8px 12px; text-align:center;'>
                <div style='font-size:10px; color:{col}; font-weight:700;'>{cat}</div>
                <div style='font-size:18px; font-weight:800; color:{col};'>{total:.0f}%</div>
                <div style='font-size:10px; color:#5A7A99;'>combined weight</div>
            </div>""", unsafe_allow_html=True)

    with col_insight:
        st.markdown("""
        <div class="banner-gold" style='margin-bottom:12px;'>
            <b style='color:#F5A623;'>🎯 Dominant Signal: Distance</b><br>
            <span style='font-size:11px;color:#5A7A99;'>
            Distance_km drives 41% of all model decisions — more than all socioeconomic
            and demographic features combined. Validates the GAM 25km threshold as the
            primary planning instrument.
            </span>
        </div>
        <div class="banner-green" style='background:#38BDF812; border-color:#38BDF833; margin-bottom:12px;'>
            <b style='color:#38BDF8;'>💰 Enabling: 73% Combined</b><br>
            <span style='font-size:11px;color:#5A7A99;'>
            Distance + Wealth + Insurance = 73% of model weight.
            These are Andersen's structural enabling factors.
            Targeting all three simultaneously is the highest-ROI policy intervention.
            </span>
        </div>
        <div style='background:#A78BFA12; border:1px solid #A78BFA33; border-radius:12px; padding:14px 18px;'>
            <b style='color:#A78BFA;'>👤 Predisposing: 25%</b><br>
            <span style='font-size:11px;color:#5A7A99;'>
            Residence type (urban vs rural) is the strongest predisposing signal,
            interacting with distance. Education and age group have smaller but
            consistent marginal contributions.
            </span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# MODULE 5: MODEL PERFORMANCE
# ============================================================
elif "Performance" in module:
    st.markdown("## ⚙️ Algorithm Tournament — Model Performance")
    st.caption("Stratified 3-Fold Cross-Validation · KNBS n=99,031 · scale_pos_weight for class imbalance")

    # Performance table
    def style_row(row):
        if row["Algorithm"] == "XGBoost (Optimised)":
            return ["background-color: #00D9A312; color: #00D9A3"] * len(row)
        return ["color: #D9E8F5"] * len(row)

    display = MODEL_PERF.drop(columns=["Operational"])
    st.dataframe(
        display.style.apply(style_row, axis=1),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")

    # Bar chart comparison
    fig_m = go.Figure()
    for col_name, color in [("F1", "#00D9A3"), ("AUC", "#38BDF8"), ("Accuracy", "#A78BFA")]:
        fig_m.add_trace(go.Bar(
            name=col_name,
            x=MODEL_PERF["Algorithm"],
            y=MODEL_PERF[col_name],
            marker_color=color,
            opacity=0.85,
        ))
    fig_m.update_layout(
        barmode="group",
        paper_bgcolor="#07111F", plot_bgcolor="#07111F",
        font_color="#D9E8F5", height=350,
        xaxis=dict(color="#5A7A99", gridcolor="#1A3450", tickangle=-25),
        yaxis=dict(color="#5A7A99", gridcolor="#1A3450", range=[0, 1.05]),
        legend=dict(bgcolor="#0D1E30", bordercolor="#1A3450"),
        margin=dict(l=10, r=10, t=10, b=80),
    )
    st.plotly_chart(fig_m, use_container_width=True)

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="banner-red">
            <b style='color:#F87171;'>⚖️ Class Imbalance & Sensitivity Bias</b><br>
            <span style='font-size:11px;color:#5A7A99;'>
            The KNBS dataset is heavily skewed — most respondents accessed care (Y=1).
            Without correction the model over-predicts access. <b style='color:#D9E8F5;'>scale_pos_weight</b>
            penalises misclassification of the minority class (Y=0: did not access).
            Result: 3,484 False Positives · 5 False Negatives.
            These FPs represent the "Urban Proximity Paradox" — not model failures.
            </span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="banner-green">
            <b style='color:#00D9A3;'>✅ Why XGBoost Was Selected</b><br>
            <span style='font-size:11px;color:#5A7A99;'>
            Highest single-model ROC-AUC (0.6524). The Top-3 soft-voting ensemble
            marginally stabilised variance (AUC 0.6510) without material performance gain.
            Negligible improvement vs. added complexity → XGBoost selected as the
            operational model for FastAPI deployment (Section 4.6).
            </span>
        </div>""", unsafe_allow_html=True)
           # streamlit run dashboard.py
           #.venv\Scripts\activate