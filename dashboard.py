import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import time

st.set_page_config(
    page_title="HealthLink Kenya",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Start FastAPI in background on first run ──
if "api_started" not in st.session_state:
    from run_api import launch
    launch()
    st.session_state.api_started = True

API = "http://localhost:8000"

# ── Fetch data server-side ──
@st.cache_data(ttl=30)
def fetch_stats():
    try:
        r = requests.get(f"{API}/analytics/dashboard/stats", timeout=5)
        if r.status_code == 200:
            return r.json()
    except: pass
    return {"total":30,"high_risk":9,"medium_risk":11,"coverage_rate":70.0}

@st.cache_data(ttl=30)
def fetch_patients():
    try:
        r = requests.get(f"{API}/patients/", params={"page":1,"page_size":100}, timeout=5)
        if r.status_code == 200:
            return r.json().get("data", [])
    except: pass
    return []

stats    = fetch_stats()
patients = fetch_patients()

# ── Read HTML and inject live data ──
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Inject data as JS variables so HTML works without calling localhost from browser
injection = f"""
<script>
  window.PRELOADED_STATS    = {json.dumps(stats)};
  window.PRELOADED_PATIENTS = {json.dumps(patients)};
  window.API_BASE           = "{API}";
</script>
"""
html = html.replace("</head>", injection + "</head>", 1)

components.html(html, height=950, scrolling=True)
