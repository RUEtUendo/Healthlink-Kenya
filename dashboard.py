"""
HealthLink Kenya — Streamlit Entry Point
Starts FastAPI in background, fetches live data, injects into index.html
"""
import streamlit as st
import streamlit.components.v1 as components
import requests, json, time, os

st.set_page_config(
    page_title="HealthLink Kenya",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Hide Streamlit chrome ──────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
.block-container { padding: 0 !important; }
iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Start FastAPI in background thread (once per session) ──────
if "api_started" not in st.session_state:
    try:
        from run_api import launch
        launch()
        st.session_state.api_started = True
    except Exception as e:
        st.session_state.api_started = False
        st.session_state.api_error = str(e)

API = "http://localhost:8000"

# ── Wait for API to be ready ───────────────────────────────────
def wait_for_api(max_wait=10):
    for _ in range(max_wait):
        try:
            r = requests.get(f"{API}/analytics/dashboard/stats", timeout=1)
            if r.status_code == 200:
                return True
        except: pass
        time.sleep(1)
    return False

api_ready = wait_for_api()

# ── Fetch all data server-side ─────────────────────────────────
@st.cache_data(ttl=60)
def fetch_stats():
    try:
        r = requests.get(f"{API}/analytics/dashboard/stats", timeout=5)
        if r.status_code == 200: return r.json()
    except: pass
    return {"total": 25, "high_risk": 8, "medium_risk": 10, "low_risk": 7, "coverage_rate": 72.0}

@st.cache_data(ttl=60)
def fetch_patients():
    try:
        r = requests.get(f"{API}/patients/", params={"page": 1, "page_size": 100}, timeout=5)
        if r.status_code == 200: return r.json().get("data", [])
    except: pass
    return []

@st.cache_data(ttl=60)
def fetch_workers():
    try:
        r = requests.get(f"{API}/users/", timeout=5)
        if r.status_code == 200: return r.json()
    except: pass
    return []

stats    = fetch_stats()
patients = fetch_patients()

# ── Load and inject into HTML ──────────────────────────────────
html_file = "index.html"
if not os.path.exists(html_file):
    st.error("index.html not found in repo root. Please ensure it is committed to GitHub.")
    st.stop()

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# Inject live data as JS globals — browser reads these instead of calling localhost
injection = f"""
<script>
  window.PRELOADED_STATS    = {json.dumps(stats)};
  window.PRELOADED_PATIENTS = {json.dumps(patients)};
  window.API_BASE           = "{API}";
  window.API_READY          = {"true" if api_ready else "false"};
</script>"""

html = html.replace("</head>", injection + "\n</head>", 1)

components.html(html, height=960, scrolling=True)
