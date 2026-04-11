<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HealthLink Kenya — SW Operations</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root {
  --bg:       #0A1929;
  --surface:  #0C2340;
  --surface2: #0F2847;
  --teal:     #1D9E75;
  --teal-mid: #5DCAA5;
  --teal-dk:  #0F6E56;
  --navy:     #185FA5;
  --text:     #e2e8f0;
  --muted:    rgba(255,255,255,0.45);
  --border:   rgba(255,255,255,0.08);
  --danger:   #F87171;
  --amber:    #FCD34D;
  --success:  #6EE7B7;
  --radius:   12px;
  --radius-sm:8px;
}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{height:100%;font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);font-size:14px;line-height:1.6;overflow-x:hidden;}

/* ── TOPBAR ── */
.topbar{
  position:sticky;top:0;z-index:1000;
  background:var(--surface);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 28px;height:56px;
}
.topbar-logo{display:flex;align-items:center;gap:10px;}
.topbar-logo-icon{width:30px;height:30px;background:linear-gradient(135deg,var(--teal),var(--navy));border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;}
.topbar-logo-text{font-family:'Sora',sans-serif;font-size:15px;font-weight:700;color:white;}
.topbar-logo-text span{color:var(--teal-mid);}
.topbar-right{display:flex;align-items:center;gap:14px;font-size:12px;}
.badge-pill{background:rgba(29,158,117,0.15);border:1px solid rgba(29,158,117,0.3);color:var(--success);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;}
.badge-pill.warn{background:rgba(245,158,11,0.15);border-color:rgba(245,158,11,0.3);color:var(--amber);}
#api-status{transition:all .3s;}

/* ── NAV TABS ── */
.nav-tabs{
  background:var(--surface);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;
  padding:0 20px;
  overflow-x:auto;
  scrollbar-width:none;
  gap:0;
}
.nav-tabs::-webkit-scrollbar{display:none;}
.nav-tab{
  display:flex;align-items:center;gap:6px;
  padding:14px 16px;
  color:var(--muted);font-size:13px;font-weight:500;
  cursor:pointer;white-space:nowrap;
  border-bottom:3px solid transparent;
  transition:all .15s;
  border-top:none;border-left:none;border-right:none;
  background:transparent;
  font-family:'DM Sans',sans-serif;
}
.nav-tab:hover{color:rgba(255,255,255,0.85);background:rgba(255,255,255,0.04);}
.nav-tab.active{color:var(--teal-mid);border-bottom-color:var(--teal-mid);font-weight:600;}

/* ── MAIN ── */
.main{padding:28px 32px;min-height:calc(100vh - 112px);}
.tab-panel{display:none;}
.tab-panel.active{display:block;animation:fadeIn .2s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px);}to{opacity:1;transform:none;}}

/* ── PAGE HEADER ── */
.page-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;}
.page-title{font-family:'Sora',sans-serif;font-size:22px;font-weight:700;color:white;}
.page-sub{font-size:13px;color:var(--muted);margin-top:2px;}
.county-badge{background:rgba(29,158,117,0.15);border:1px solid rgba(29,158,117,0.3);color:var(--teal-mid);font-size:11px;font-weight:600;padding:5px 12px;border-radius:20px;}

/* ── STAT GRID ── */
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px;}
.stat-val{font-family:'Sora',sans-serif;font-size:26px;font-weight:700;color:white;}
.stat-label{font-size:11px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.05em;}
.stat-change{font-size:11px;margin-top:6px;font-weight:600;color:var(--teal-mid);}
.stat-change.down{color:var(--danger);}

/* ── HUB GRID ── */
.hub-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px;}
.hub-btn{background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius);padding:28px 14px 22px;text-align:center;cursor:pointer;transition:all .2s;}
.hub-btn:hover{background:rgba(29,158,117,0.1);border-color:var(--teal-mid);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3);}
.hub-icon{font-size:30px;margin-bottom:10px;display:block;}
.hub-label{font-size:13px;font-weight:600;color:white;}
.hub-desc{font-size:11px;color:var(--muted);margin-top:4px;}

/* ── CARDS ── */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-bottom:14px;}
.card-title{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:14px;}
.card-danger{background:rgba(226,75,74,0.07);border-left:4px solid var(--danger);border-radius:var(--radius);padding:18px 20px;margin-bottom:12px;}
.card-warning{background:rgba(245,158,11,0.07);border-left:4px solid var(--amber);border-radius:var(--radius);padding:18px 20px;margin-bottom:12px;}
.card-teal{background:rgba(29,158,117,0.07);border:1px solid rgba(29,158,117,0.25);border-radius:var(--radius);padding:16px;margin-bottom:12px;}

/* ── RISK PILLS ── */
.pill{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;display:inline-block;}
.pill-high{background:rgba(248,113,113,0.18);color:var(--danger);}
.pill-med{background:rgba(252,211,77,0.18);color:var(--amber);}
.pill-low{background:rgba(110,231,183,0.18);color:var(--success);}

/* ── MAP CONTAINERS ── */
.map-wrap{background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;}
#geo-map,#mc-map{width:100%;height:460px;border-radius:var(--radius);}
.map-controls{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;}
.map-ctrl-btn{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);color:white;padding:7px 14px;border-radius:6px;font-size:12px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .15s;}
.map-ctrl-btn:hover,.map-ctrl-btn.active{background:rgba(29,158,117,0.2);border-color:var(--teal-mid);color:var(--teal-mid);}

/* ── TRIAGE FORM ── */
.triage-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;}
.form-group{display:flex;flex-direction:column;gap:6px;margin-bottom:14px;}
.form-label{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;}
.form-control{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);color:white;padding:9px 12px;border-radius:var(--radius-sm);font-size:13px;font-family:'DM Sans',sans-serif;width:100%;}
.form-control:focus{outline:none;border-color:var(--teal-mid);}
.form-control option{background:var(--surface);}
input[type=range]{-webkit-appearance:none;width:100%;height:4px;border-radius:2px;background:rgba(255,255,255,0.15);outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:var(--teal);cursor:pointer;}
.range-val{font-size:12px;color:var(--teal-mid);font-weight:600;margin-top:4px;}
.btn{padding:10px 20px;border:none;border-radius:var(--radius-sm);font-size:13px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .15s;}
.btn-teal{background:linear-gradient(135deg,var(--teal),var(--teal-dk));color:white;}
.btn-teal:hover{opacity:.88;}
.btn-outline{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);color:white;}
.btn-outline:hover{background:rgba(255,255,255,0.12);}
.btn-danger{background:rgba(226,75,74,0.15);border:1px solid rgba(226,75,74,0.3);color:var(--danger);}

/* ── RESULT CARDS ── */
.result-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px;}
.result-card{background:var(--surface2);border-radius:var(--radius);padding:22px 12px;text-align:center;}
.result-label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;}
.result-val{font-family:'Sora',sans-serif;font-size:40px;font-weight:700;}
.result-sub{font-size:10px;color:var(--muted);margin-top:4px;}

/* ── TABLE ── */
.tbl-wrap{overflow-x:auto;border-radius:var(--radius);border:1px solid var(--border);}
table{width:100%;border-collapse:collapse;}
thead th{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;padding:11px 14px;text-align:left;border-bottom:1px solid var(--border);background:var(--surface);cursor:pointer;white-space:nowrap;}
thead th:hover{color:white;}
tbody td{padding:12px 14px;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px;color:rgba(255,255,255,0.8);background:var(--surface2);}
tbody tr:hover td{background:rgba(255,255,255,0.03);}
.db-controls{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center;}
.db-controls input,.db-controls select{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);color:white;padding:8px 12px;border-radius:var(--radius-sm);font-size:13px;font-family:'DM Sans',sans-serif;}
.db-controls input{width:240px;}
.db-controls select{min-width:140px;}
.pagination{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-top:1px solid var(--border);background:var(--surface);}
.page-info{font-size:12px;color:var(--muted);}

/* ── ACCORDION ── */
.accordion{border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;margin-bottom:14px;}
.accordion-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;cursor:pointer;font-size:14px;font-weight:600;color:white;background:var(--surface);transition:background .15s;}
.accordion-header:hover{background:rgba(29,158,117,0.08);}
.accordion-header.open{color:var(--teal-mid);border-bottom:1px solid var(--border);}
.accordion-body{display:none;padding:20px;background:var(--surface2);}
.accordion-body.open{display:block;}
.chevron{transition:transform .2s;color:var(--muted);}
.chevron.open{transform:rotate(180deg);}

/* ── ALERT CARDS ── */
.alert-card{border-radius:var(--radius);padding:18px 20px;margin-bottom:12px;display:flex;align-items:flex-start;gap:14px;position:relative;}
.alert-icon{font-size:24px;flex-shrink:0;margin-top:2px;}
.alert-content{flex:1;}
.alert-title{font-size:14px;font-weight:700;color:white;margin-bottom:3px;}
.alert-sub{font-size:12px;color:var(--muted);}
.alert-msg{font-size:13px;color:rgba(255,255,255,0.75);margin-top:6px;line-height:1.5;}
.alert-ec{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.04);border-radius:8px;padding:10px 14px;margin-top:10px;}
.alert-time{font-size:11px;color:rgba(255,255,255,0.25);margin-top:8px;}
.alert-badge{position:absolute;top:16px;right:16px;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:700;}
.alert-actions{display:flex;gap:8px;margin-top:12px;}
.btn-call{background:rgba(226,75,74,0.15);border:1px solid rgba(226,75,74,0.3);color:var(--danger);padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;}
.btn-ack{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.12);color:rgba(255,255,255,0.6);padding:6px 14px;border-radius:6px;font-size:12px;cursor:pointer;font-family:'DM Sans',sans-serif;}
.btn-ack:hover{background:rgba(255,255,255,0.1);}

/* ── SETTINGS ── */
.settings-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
.settings-label{font-size:13px;font-weight:600;color:var(--muted);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border);}
.settings-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);}
.settings-key{font-size:13px;color:rgba(255,255,255,0.7);font-weight:500;}
.settings-input{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);color:white;padding:7px 12px;border-radius:6px;font-size:13px;font-family:'DM Sans',sans-serif;width:180px;}
.toggle{width:38px;height:20px;background:var(--teal);border-radius:10px;position:relative;cursor:pointer;flex-shrink:0;}
.toggle::after{content:'';position:absolute;width:14px;height:14px;background:white;border-radius:50%;top:3px;right:3px;transition:right .2s;}
.toggle.off{background:rgba(255,255,255,0.2);}
.toggle.off::after{right:20px;}

/* ── MOBILE CLINIC LIST ── */
.mc-layout{display:grid;grid-template-columns:280px 1fr;gap:14px;height:530px;}
.hh-list{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column;}
.hh-list-header{padding:12px 14px;border-bottom:1px solid var(--border);flex-shrink:0;}
.hh-list-header input{width:100%;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);color:white;padding:7px 10px;border-radius:6px;font-size:12px;font-family:'DM Sans',sans-serif;}
.hh-list-body{overflow-y:auto;flex:1;}
.hh-item{padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.04);cursor:pointer;transition:background .12s;}
.hh-item:hover{background:rgba(255,255,255,0.04);}
.hh-item.active{background:rgba(29,158,117,0.1);border-left:3px solid var(--teal-mid);}
.hh-id{font-size:12px;font-weight:700;font-family:monospace;}
.hh-name{font-size:11px;color:var(--muted);margin-top:1px;}
.hh-meta{font-size:10px;color:rgba(255,255,255,0.3);}

/* ── DETAIL CARD ── */
.detail-card{margin-top:12px;}
.detail-inner{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:16px;padding:16px 20px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);}
.detail-avatar{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;border:2px solid rgba(255,255,255,0.12);}
.detail-facs{display:flex;gap:8px;padding:12px 20px;background:var(--surface);border:1px solid var(--border);border-top:none;border-radius:0 0 var(--radius) var(--radius);}
.fac-chip{flex:1;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:9px 12px;}
.fac-chip-name{font-size:12px;font-weight:600;color:white;}
.fac-chip-meta{font-size:10px;color:var(--muted);margin-top:2px;}

/* ── CHART CONTAINERS ── */
.chart-container{position:relative;background:var(--surface2);border-radius:var(--radius);padding:20px;margin-bottom:14px;}

/* ── FOOTER ── */
.footer{padding:20px 32px;border-top:1px solid var(--border);font-size:11px;color:rgba(255,255,255,0.25);line-height:1.8;}

/* ── LOADER ── */
.loader{display:flex;align-items:center;justify-content:center;padding:40px;color:var(--muted);font-size:13px;gap:8px;}
.spinner{width:16px;height:16px;border:2px solid rgba(255,255,255,0.1);border-top-color:var(--teal-mid);border-radius:50%;animation:spin .7s linear infinite;}
@keyframes spin{to{transform:rotate(360deg);}}

/* ── LEGEND ── */
.legend{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px;}
.legend-item{display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,0.6);}
.legend-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
.legend-sq{width:10px;height:10px;border-radius:2px;flex-shrink:0;}

/* ── TRIAGE TABLE ── */
.triage-table{width:100%;border-collapse:collapse;}
.triage-table th{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;padding:10px 14px;text-align:left;border-bottom:1px solid var(--border);}
.triage-table td{padding:12px 14px;border-bottom:1px solid rgba(255,255,255,0.05);font-size:13px;color:rgba(255,255,255,0.8);}

/* ── RESPONSIVE ── */
@media(max-width:900px){
  .stat-grid,.hub-grid{grid-template-columns:repeat(2,1fr);}
  .triage-grid,.settings-grid,.mc-layout{grid-template-columns:1fr;}
  .main{padding:16px;}
}
</style>
</head>
<body>

<!-- ── TOPBAR ── -->
<header class="topbar">
  <div class="topbar-logo">
    <div class="topbar-logo-icon">🏥</div>
    <div class="topbar-logo-text">Health<span>Link</span> Kenya</div>
  </div>
  <div class="topbar-right">
    <span id="api-status" class="badge-pill">⟳ Connecting…</span>
    <span style="font-size:12px;color:var(--muted);">Nakuru County SW Console</span>
  </div>
</header>

<!-- ── NAV TABS ── -->
<nav class="nav-tabs" id="nav-tabs">
  <button class="nav-tab active" onclick="switchTab('hub')">⊞&nbsp; Outreach Hub</button>
  <button class="nav-tab" onclick="switchTab('geo')">🗺️&nbsp; Geospatial</button>
  <button class="nav-tab" onclick="switchTab('mobile')">🚐&nbsp; Mobile Clinic</button>
  <button class="nav-tab" onclick="switchTab('triage')">👥&nbsp; Triage</button>
  <button class="nav-tab" onclick="switchTab('patientdb')">🗄️&nbsp; Patient Database</button>
  <button class="nav-tab" onclick="switchTab('reports')">📊&nbsp; Reports</button>
  <button class="nav-tab" onclick="switchTab('alerts')">🔔&nbsp; Alerts</button>
  <button class="nav-tab" onclick="switchTab('settings')">⚙️&nbsp; Settings</button>
</nav>

<main class="main">

<!-- ══════════════════════════════════════════ TAB 1 — OUTREACH HUB ══════════════════════════════════════════ -->
<section class="tab-panel active" id="tab-hub">
  <div class="page-header">
    <div>
      <div class="page-title">Outreach Hub</div>
      <div class="page-sub">Nakuru County — select a module to begin</div>
    </div>
    <span class="county-badge">📍 Nakuru County</span>
  </div>

  <div class="stat-grid">
    <div class="stat-card">
      <div class="stat-val" id="hub-total">—</div>
      <div class="stat-label">Total Registered Patients</div>
      <div class="stat-change">↑ Live from FastAPI</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" id="hub-high" style="color:var(--danger);">—</div>
      <div class="stat-label">High Risk Patients</div>
      <div class="stat-change down" id="hub-high-pct"></div>
    </div>
    <div class="stat-card">
      <div class="stat-val" id="hub-med" style="color:var(--amber);">—</div>
      <div class="stat-label">Medium Risk Patients</div>
      <div class="stat-change"></div>
    </div>
    <div class="stat-card">
      <div class="stat-val" id="hub-cov" style="color:var(--teal-mid);">—</div>
      <div class="stat-label">Coverage Rate</div>
      <div class="stat-change">↑ 2pts vs last month</div>
    </div>
  </div>

  <div class="hub-grid">
    <div class="hub-btn" onclick="switchTab('geo')">
      <span class="hub-icon">🗺️</span>
      <div class="hub-label">Geospatial Mapper</div>
      <div class="hub-desc">Risk zones, facilities & household IDs</div>
    </div>
    <div class="hub-btn" onclick="switchTab('reports')">
      <span class="hub-icon">📊</span>
      <div class="hub-label">Reports</div>
      <div class="hub-desc">Triage, SHAP & distance decay</div>
    </div>
    <div class="hub-btn" onclick="switchTab('triage')">
      <span class="hub-icon">👥</span>
      <div class="hub-label">Patient Triage</div>
      <div class="hub-desc">View patient profiles & risk</div>
    </div>
    <div class="hub-btn" onclick="switchTab('mobile')">
      <span class="hub-icon">🚐</span>
      <div class="hub-label">Mobile Clinic Routing</div>
      <div class="hub-desc">Household IDs on field map</div>
    </div>
    <div class="hub-btn" onclick="switchTab('geo')">
      <span class="hub-icon">📉</span>
      <div class="hub-label">Distance Decay</div>
      <div class="hub-desc">Pin-drop household range analysis</div>
    </div>
    <div class="hub-btn" onclick="switchTab('alerts')">
      <span class="hub-icon">🔔</span>
      <div class="hub-label">Alerts</div>
      <div class="hub-desc">Emergency contacts · High-risk flags</div>
    </div>
    <div class="hub-btn" onclick="exportCSV()">
      <span class="hub-icon">📤</span>
      <div class="hub-label">Export</div>
      <div class="hub-desc">Download county reports CSV</div>
    </div>
    <div class="hub-btn" onclick="switchTab('patientdb')" style="border-color:rgba(29,158,117,0.35);background:rgba(29,158,117,0.07);">
      <span class="hub-icon">🗄️</span>
      <div class="hub-label" style="color:var(--teal-mid);">Patient Database</div>
      <div class="hub-desc">All registered patients — full records</div>
    </div>
  </div>

  <div style="margin-bottom:16px;">
    <div style="font-family:'Sora',sans-serif;font-size:16px;font-weight:600;color:white;margin-bottom:12px;">🔔 Recent Alerts</div>
    <div id="hub-alerts">
      <div class="loader"><div class="spinner"></div>Loading alerts…</div>
    </div>
  </div>
</section>

<!-- ══════════════════════════════════════════ TAB 2 — GEOSPATIAL ══════════════════════════════════════════ -->
<section class="tab-panel" id="tab-geo">
  <div class="page-header">
    <div>
      <div class="page-title">Geospatial Mapper</div>
      <div class="page-sub">Facility coverage, household IDs & distance decay — Nakuru County</div>
    </div>
  </div>
  <div class="map-controls">
    <button class="map-ctrl-btn active" id="ctrl-facilities" onclick="toggleGeoLayer('facilities',this)">Facilities</button>
    <button class="map-ctrl-btn active" id="ctrl-households" onclick="toggleGeoLayer('households',this)">Households</button>
    <button class="map-ctrl-btn active" id="ctrl-risk" onclick="toggleGeoLayer('risk',this)">Risk zones</button>
    <button class="map-ctrl-btn" id="ctrl-decay" onclick="activateDecayMode()">📌 Drop pin — decay ring</button>
    <span style="font-size:12px;color:var(--muted);margin-left:8px;" id="geo-hint">Click map to drop decay pin</span>
  </div>
  <div class="map-wrap">
    <div id="geo-map"></div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px;">
    <div class="stat-card"><div class="stat-val" id="geo-fac-count">—</div><div class="stat-label">Facilities mapped</div></div>
    <div class="stat-card"><div class="stat-val">10</div><div class="stat-label">Households shown</div></div>
    <div class="stat-card"><div class="stat-val">35 km</div><div class="stat-label">Decay threshold</div></div>
    <div class="stat-card"><div class="stat-val">Distance</div><div class="stat-label">Top barrier</div></div>
  </div>
  <div class="card" style="margin-top:12px;">
    <div class="card-title">Legend</div>
    <div class="legend">
      <div class="legend-item"><div class="legend-sq" style="background:#1D9E75;"></div>Hospital</div>
      <div class="legend-item"><div class="legend-sq" style="background:#185FA5;"></div>Health Centre</div>
      <div class="legend-item"><div class="legend-sq" style="background:#8B5CF6;"></div>Dispensary</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--danger);"></div>High risk HH</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--amber);"></div>Medium risk HH</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--success);"></div>Low risk HH</div>
    </div>
  </div>
  <div id="decay-results" style="display:none;" class="card-teal">
    <div style="font-size:12px;font-weight:600;color:var(--amber);margin-bottom:10px;">📌 Distance decay results from dropped pin</div>
    <div id="decay-content"></div>
  </div>
</section>

<!-- ══════════════════════════════════════════ TAB 3 — MOBILE CLINIC ══════════════════════════════════════════ -->
<section class="tab-panel" id="tab-mobile">
  <div class="page-header">
    <div>
      <div class="page-title">Mobile Clinic Routing</div>
      <div class="page-sub">Select a household to locate — nearest facilities shown automatically</div>
    </div>
    <button class="btn btn-outline" onclick="clearMCRoute()">Clear route</button>
  </div>
  <div class="mc-layout">
    <div class="hh-list">
      <div class="hh-list-header">
        <input type="text" placeholder="🔍 Search household…" oninput="filterHH(this.value)" id="hh-search">
        <div style="display:flex;gap:6px;margin-top:8px;flex-wrap:wrap;">
          <button class="map-ctrl-btn active" onclick="setHHFilter('All',this)">All</button>
          <button class="map-ctrl-btn" onclick="setHHFilter('High',this)" style="color:var(--danger);border-color:rgba(248,113,113,0.3);">High</button>
          <button class="map-ctrl-btn" onclick="setHHFilter('Medium',this)" style="color:var(--amber);border-color:rgba(252,211,77,0.3);">Medium</button>
          <button class="map-ctrl-btn" onclick="setHHFilter('Low',this)" style="color:var(--success);border-color:rgba(110,231,183,0.3);">Low</button>
        </div>
        <div id="hh-count" style="font-size:10px;color:var(--muted);margin-top:6px;text-transform:uppercase;letter-spacing:.06em;"></div>
      </div>
      <div class="hh-list-body" id="hh-list-body"></div>
    </div>
    <div class="map-wrap">
      <div id="mc-map"></div>
    </div>
  </div>
  <div class="detail-card" id="mc-detail" style="display:none;">
    <div class="detail-inner" id="mc-detail-inner"></div>
    <div class="detail-facs" id="mc-detail-facs"></div>
  </div>
</section>

<!-- ══════════════════════════════════════════ TAB 4 — TRIAGE ══════════════════════════════════════════ -->
<section class="tab-panel" id="tab-triage">
  <div class="page-header">
    <div>
      <div class="page-title">Predictive Triage</div>
      <div class="page-sub">Enter patient profile → live XGBoost prediction via FastAPI backend</div>
    </div>
  </div>
  <div class="triage-grid">
    <div class="card">
      <div class="card-title">Patient Profile</div>
      <div class="form-group">
        <label class="form-label">Age Group</label>
        <select class="form-control" id="t-age">
          <option>0-4</option><option>5-14</option><option>15-24</option>
          <option selected>25-34</option><option>35-49</option><option>50-64</option><option>65+</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Gender</label>
        <select class="form-control" id="t-gender">
          <option>Female</option><option>Male</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Residence Type</label>
        <select class="form-control" id="t-residence">
          <option>Urban</option><option>Rural</option><option>Peri-Urban</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Wealth Index</label>
        <select class="form-control" id="t-wealth">
          <option>Poorest</option><option>Poorer</option><option selected>Middle</option><option>Richer</option><option>Richest</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Insurance Status</label>
        <select class="form-control" id="t-insurance">
          <option value="1">Insured</option><option value="0">Uninsured</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Distance to Nearest Facility (km)</label>
        <input type="range" id="t-distance" min="0" max="100" value="5" step="0.5" oninput="document.getElementById('t-dist-val').textContent=this.value+' km'">
        <div class="range-val" id="t-dist-val">5 km</div>
      </div>
      <div id="t-dist-warning" style="display:none;" class="card-danger" style="padding:10px 14px;font-size:12px;">
        📍 Beyond 35km GAM threshold — access probability drops sharply.
      </div>
      <button class="btn btn-teal" style="width:100%;margin-top:8px;" onclick="runTriage()">🔍 Run Access Prediction</button>
    </div>
    <div id="triage-result-panel">
      <div class="card" style="text-align:center;padding:60px 20px;">
        <div style="font-size:44px;margin-bottom:14px;">🔍</div>
        <div style="font-size:14px;color:var(--muted);">Fill in the patient profile and click<br>Run Access Prediction</div>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════════════════════════════════ TAB 5 — PATIENT DATABASE ══════════════════════════════════════════ -->
<section class="tab-panel" id="tab-patientdb">
  <div class="page-header">
    <div>
      <div class="page-title">Patient Database</div>
      <div class="page-sub">All registered patients — Nakuru County · <span id="db-count" style="color:var(--teal-mid);font-weight:700;"></span></div>
    </div>
    <button class="btn btn-teal" onclick="exportCSV()">⬇ Export CSV</button>
  </div>

  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px;">
    <div class="stat-card"><div class="stat-val" id="db-total">—</div><div class="stat-label">Total</div></div>
    <div class="stat-card"><div class="stat-val" id="db-high" style="color:var(--danger);">—</div><div class="stat-label">High Risk</div></div>
    <div class="stat-card"><div class="stat-val" id="db-med" style="color:var(--amber);">—</div><div class="stat-label">Medium Risk</div></div>
    <div class="stat-card"><div class="stat-val" id="db-low" style="color:var(--success);">—</div><div class="stat-label">Low Risk</div></div>
    <div class="stat-card"><div class="stat-val" id="db-nhif" style="color:var(--teal-mid);">—</div><div class="stat-label">NHIF Insured</div></div>
  </div>

  <div class="db-controls">
    <input type="text" placeholder="🔍 Search name, ID, sub-county…" id="db-search" oninput="filterDB()">
    <select id="db-risk-filter" onchange="filterDB()">
      <option value="">All Risk Levels</option>
      <option value="High">High</option>
      <option value="Medium">Medium</option>
      <option value="Low">Low</option>
    </select>
    <select id="db-sub-filter" onchange="filterDB()">
      <option value="">All Sub-counties</option>
      <option>Nakuru Town</option><option>Bahati</option><option>Njoro</option><option>Rongai</option>
      <option>Subukia</option><option>Kuresoi</option><option>Molo</option><option>Gilgil</option><option>Naivasha</option>
    </select>
  </div>

  <div class="tbl-wrap">
    <table id="db-table">
      <thead>
        <tr>
          <th onclick="sortDB('id')">Patient ID ↕</th>
          <th onclick="sortDB('name')">Name ↕</th>
          <th>Age</th><th>Gender</th>
          <th onclick="sortDB('sub_county')">Sub-county ↕</th>
          <th>Condition</th>
          <th onclick="sortDB('risk')">Risk ↕</th>
          <th>Dist (km)</th><th>Insurance</th><th>Last Visit</th>
        </tr>
      </thead>
      <tbody id="db-tbody">
        <tr><td colspan="10"><div class="loader"><div class="spinner"></div>Loading patients from API…</div></td></tr>
      </tbody>
    </table>
  </div>
  <div class="pagination">
    <div class="page-info" id="db-page-info"></div>
    <div style="display:flex;gap:8px;">
      <button class="btn btn-outline" id="db-prev" onclick="dbPage(-1)">← Prev</button>
      <button class="btn btn-outline" id="db-next" onclick="dbPage(1)">Next →</button>
    </div>
  </div>
</section>

<!-- ══════════════════════════════════════════ TAB 6 — REPORTS ══════════════════════════════════════════ -->
<section class="tab-panel" id="tab-reports">
  <div class="page-header">
    <div>
      <div class="page-title">Reports</div>
      <div class="page-sub">Predictive triage · SHAP attribution · Distance decay analytics</div>
    </div>
  </div>

  <!-- Accordion 1: Predictive Risk Triage -->
  <div class="accordion">
    <div class="accordion-header open" onclick="toggleAccordion(this)">
      <span>Predictive Risk Triage — Nakuru County</span>
      <span class="chevron open">▼</span>
    </div>
    <div class="accordion-body open">
      <table class="triage-table">
        <thead>
          <tr><th>Household ID</th><th>Sub-county</th><th>Risk Score</th><th>Primary Barrier</th><th>Distance (km)</th><th>Insurance</th></tr>
        </thead>
        <tbody>
          <tr><td style="font-family:monospace;color:var(--amber);">HH-NK-00234</td><td>Bahati</td><td><span class="pill pill-high">High 0.87</span></td><td><span style="background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.6);padding:2px 8px;border-radius:4px;font-size:11px;">Distance</span></td><td style="color:var(--danger);">41.2</td><td>None</td></tr>
          <tr><td style="font-family:monospace;color:var(--amber);">HH-NK-00891</td><td>Njoro</td><td><span class="pill pill-high">High 0.82</span></td><td><span style="background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.6);padding:2px 8px;border-radius:4px;font-size:11px;">Education</span></td><td>28.5</td><td>None</td></tr>
          <tr><td style="font-family:monospace;color:var(--amber);">HH-NK-01102</td><td>Rongai</td><td><span class="pill pill-med">Med 0.65</span></td><td><span style="background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.6);padding:2px 8px;border-radius:4px;font-size:11px;">Wealth</span></td><td>19.3</td><td>NHIF</td></tr>
          <tr><td style="font-family:monospace;color:var(--amber);">HH-NK-00455</td><td>Subukia</td><td><span class="pill pill-med">Med 0.61</span></td><td><span style="background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.6);padding:2px 8px;border-radius:4px;font-size:11px;">Distance</span></td><td>36.7</td><td>None</td></tr>
          <tr><td style="font-family:monospace;color:var(--amber);">HH-NK-00678</td><td>Nakuru Town</td><td><span class="pill pill-low">Low 0.31</span></td><td><span style="background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.6);padding:2px 8px;border-radius:4px;font-size:11px;">Insurance</span></td><td>3.1</td><td>Partial</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Accordion 2: SHAP -->
  <div class="accordion">
    <div class="accordion-header" onclick="toggleAccordion(this)">
      <span>SHAP Feature Importance — Access Model</span>
      <span class="chevron">▼</span>
    </div>
    <div class="accordion-body">
      <div class="chart-container" style="height:280px;">
        <canvas id="shap-chart"></canvas>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px;">
        <div class="card-warning"><b style="color:var(--amber);">Enabling: 26.8%</b><br><span style="font-size:12px;color:var(--muted);">Distance + Wealth + Insurance</span></div>
        <div class="card" style="border-left:3px solid #6366F1;"><b style="color:#A78BFA;">Predisposing: 73.2%</b><br><span style="font-size:12px;color:var(--muted);">Education dominates</span></div>
        <div class="card-teal"><b style="color:var(--teal-mid);">Distance: 12.9%</b><br><span style="font-size:12px;color:var(--muted);">Strongest single feature</span></div>
      </div>
    </div>
  </div>

  <!-- Accordion 3: Distance Decay -->
  <div class="accordion">
    <div class="accordion-header" onclick="toggleAccordion(this)">
      <span>Distance Decay — GAM Analysis</span>
      <span class="chevron">▼</span>
    </div>
    <div class="accordion-body">
      <div class="chart-container" style="height:360px;">
        <canvas id="gam-chart"></canvas>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px;">
        <div class="card-teal"><b style="color:var(--teal-mid);">0–35 km · Stable Zone</b><br><span style="font-size:12px;color:var(--muted);">89–92% access probability</span></div>
        <div class="card-warning"><b style="color:var(--amber);">35 km · Inflection</b><br><span style="font-size:12px;color:var(--muted);">GAM threshold — mobile clinic boundary</span></div>
        <div class="card-danger"><b style="color:var(--danger);">&gt;35 km · Declining</b><br><span style="font-size:12px;color:var(--muted);">Access drops to 84% at 50 km</span></div>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════════════════════════════════ TAB 7 — ALERTS ══════════════════════════════════════════ -->
<section class="tab-panel" id="tab-alerts">
  <div class="page-header">
    <div>
      <div class="page-title">Alerts</div>
      <div class="page-sub">Emergency contacts, high-risk flags and urgent outreach actions</div>
    </div>
    <div style="display:flex;gap:8px;">
      <button class="btn btn-outline" style="font-size:12px;padding:7px 14px;">Mark all read</button>
      <span style="background:rgba(226,75,74,0.2);color:var(--danger);font-size:12px;font-weight:700;padding:7px 14px;border-radius:var(--radius-sm);" id="alerts-crit-badge">3 Critical</span>
    </div>
  </div>
  <div id="alerts-list"></div>
</section>

<!-- ══════════════════════════════════════════ TAB 8 — SETTINGS ══════════════════════════════════════════ -->
<section class="tab-panel" id="tab-settings">
  <div class="page-header">
    <div>
      <div class="page-title">Settings</div>
      <div class="page-sub">Coverage area, alert thresholds and export preferences</div>
    </div>
    <button class="btn btn-teal" onclick="saveSettings()">Save changes</button>
  </div>
  <div class="settings-grid">
    <div class="card">
      <div class="settings-label">Coverage area</div>
      <div class="settings-row"><span class="settings-key">County</span><input class="settings-input" value="Nakuru"></div>
      <div class="settings-row"><span class="settings-key">Sub-counties</span><input class="settings-input" value="All"></div>
      <div class="settings-row"><span class="settings-key">Distance threshold (km)</span><input class="settings-input" type="number" value="35" id="s-decay"></div>
    </div>
    <div class="card">
      <div class="settings-label">Alert thresholds</div>
      <div class="settings-row"><span class="settings-key">High-risk flag (score above)</span><input class="settings-input" value="0.75"></div>
      <div class="settings-row"><span class="settings-key">Export format</span>
        <select class="settings-input" style="padding:7px 10px;cursor:pointer;"><option>CSV</option><option>Excel</option><option>JSON</option></select>
      </div>
      <div class="settings-row"><span class="settings-key">Email alerts</span><div class="toggle" onclick="this.classList.toggle('off')"></div></div>
      <div class="settings-row"><span class="settings-key">SMS emergency alerts</span><div class="toggle" onclick="this.classList.toggle('off')"></div></div>
    </div>
  </div>

  <div class="card-teal" style="margin-top:20px;">
    <div style="font-size:12px;font-weight:700;color:var(--teal-mid);margin-bottom:8px;">HealthLink Kenya — System Information</div>
    <div style="font-size:12px;color:var(--muted);line-height:2.2;">
      <b style="color:rgba(255,255,255,0.7);">FastAPI Backend:</b> https://healthlink-kenya-production.up.railway.app<br>
      <b style="color:rgba(255,255,255,0.7);">Access Model:</b> XGBoost (Tuned) · F1: 0.8091 · AUC: 0.8144<br>
      <b style="color:rgba(255,255,255,0.7);">Retention Model:</b> XGBoost Stage 2 (SMOTE) · AUC: 0.8292 · Recall: 53.4%<br>
      <b style="color:rgba(255,255,255,0.7);">Dataset:</b> KNBS HSB Survey 2022 · n = 99,031
    </div>
  </div>
</section>

</main>

<!-- ── FOOTER ── -->
<footer class="footer">
  HealthLink Kenya — Social Worker Operations Dashboard.<br>
  Author: Rutendo Julia Kandeya · ID: 168332 · Strathmore University · 2026. Supervisor: Dr. Esther Khakata
</footer>

<script>
// ─────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────
const API = 'https://healthlink-kenya-production.up.railway.app';

const FACILITIES = [
  {name:'Nakuru PGH',lat:-0.2929,lng:36.0763,type:'hospital'},
  {name:'Naivasha District Hospital',lat:-0.7145,lng:36.4335,type:'hospital'},
  {name:'Bahati District Hospital',lat:-0.1703,lng:36.1237,type:'hospital'},
  {name:'Molo District Hospital',lat:-0.2500,lng:35.7337,type:'hospital'},
  {name:'Gilgil Sub-District Hospital',lat:-0.4987,lng:36.3225,type:'hospital'},
  {name:'Subukia SDH',lat:-0.0003,lng:36.2283,type:'hospital'},
  {name:'Lanet Health Centre',lat:-0.2699,lng:36.1071,type:'clinic'},
  {name:'Njoro Health Centre',lat:-0.3355,lng:35.9394,type:'clinic'},
  {name:'Rongai Health Centre',lat:-0.2029,lng:35.9612,type:'clinic'},
  {name:'Bahati Dispensary',lat:-0.1540,lng:36.1536,type:'dispensary'},
  {name:'Mbaruk Dispensary',lat:-0.4996,lng:36.3237,type:'dispensary'},
];

const HH_DATA = [
  {id:'HH-NK-00234',name:'Rutendo Nyamari',age:34,cond:'Hypertension',risk:'High',dist:41.2,ins:'None',sub:'Bahati',lat:-0.154,lng:36.140},
  {id:'HH-NK-00891',name:'Joseph Mwangi',age:52,cond:'Diabetes T2',risk:'High',dist:28.5,ins:'None',sub:'Njoro',lat:-0.368,lng:35.970},
  {id:'HH-NK-01102',name:'Aisha Karimi',age:29,cond:'Maternal Care',risk:'Medium',dist:19.3,ins:'NHIF',sub:'Rongai',lat:-0.190,lng:35.980},
  {id:'HH-NK-00455',name:'Samuel Otieno',age:45,cond:'TB Follow-up',risk:'Medium',dist:36.7,ins:'None',sub:'Subukia',lat:0.020,lng:36.220},
  {id:'HH-NK-00678',name:'Fatuma Hassan',age:38,cond:'HIV Care',risk:'Low',dist:3.1,ins:'Partial',sub:'Nakuru Town',lat:-0.303,lng:36.075},
  {id:'HH-NK-00312',name:'Grace Wambui',age:61,cond:'Hypertension',risk:'High',dist:52.3,ins:'None',sub:'Molo',lat:-0.270,lng:35.760},
  {id:'HH-NK-00549',name:'Daniel Kimani',age:44,cond:'Diabetes T2',risk:'Medium',dist:22.1,ins:'NHIF',sub:'Gilgil',lat:-0.480,lng:36.300},
  {id:'HH-NK-00763',name:'Susan Njoki',age:33,cond:'Maternal Care',risk:'Low',dist:7.8,ins:'NHIF',sub:'Bahati',lat:-0.185,lng:36.130},
  {id:'HH-NK-00988',name:'Peter Koech',age:58,cond:'TB Screening',risk:'High',dist:47.0,ins:'None',sub:'Kuresoi',lat:-0.420,lng:35.690},
  {id:'HH-NK-01055',name:'Mary Auma',age:27,cond:'Child Nutrition',risk:'Low',dist:11.2,ins:'NHIF',sub:'Rongai',lat:-0.150,lng:36.020},
];

const ALERTS_DATA = [
  {id:'HH-NK-00234',name:'Rutendo Nyamari',sub:'Bahati',cond:'Hypertension',sev:'critical',
   msg:'Reported chest pain and difficulty breathing. Missed follow-up scheduled 5 Apr 2026.',
   ec:'James Nyamari',rel:'Spouse',phone:'+254 712 445 678',time:'Today at 08:14 AM'},
  {id:'HH-NK-00312',name:'Grace Wambui',sub:'Molo',cond:'Hypertension',sev:'critical',
   msg:'New registration flagged risk score 0.91. Distance 52.3km — beyond decay threshold. No insurance.',
   ec:'Grace Wanjiku',rel:'Mother',phone:'+254 728 990 112',time:'Today at 09:32 AM'},
  {id:'HH-NK-00891',name:'Joseph Mwangi',sub:'Njoro',cond:'Diabetes T2',sev:'critical',
   msg:'Missed 2 consecutive follow-up appointments. Last contact 15 Feb 2026. Dropout risk elevated.',
   ec:'Peter Kamau',rel:'Brother',phone:'+254 700 334 891',time:'Yesterday at 04:45 PM'},
  {id:'HH-NK-00455',name:'Samuel Otieno',sub:'Subukia',cond:'TB Follow-up',sev:'warning',
   msg:'Distance 36.7km exceeds 35km decay threshold. Utilisation probability dropped to 38%.',
   ec:'',rel:'',phone:'',time:'2 days ago'},
];

// ─────────────────────────────────────────────
// TAB SWITCHING
// ─────────────────────────────────────────────
const TAB_MAP = {
  'hub':'hub','geo':'geo','mobile':'mobile','triage':'triage',
  'patientdb':'patientdb','reports':'reports','alerts':'alerts','settings':'settings'
};
let chartsBuilt = false;

function switchTab(id) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  const tabs = document.querySelectorAll('.nav-tab');
  const order = ['hub','geo','mobile','triage','patientdb','reports','alerts','settings'];
  const idx = order.indexOf(id);
  if(idx >= 0) tabs[idx].classList.add('active');

  if(id==='geo' && !window.geoMapInit) initGeoMap();
  if(id==='mobile' && !window.mcMapInit) initMCMap();
  if(id==='reports' && !chartsBuilt){ buildCharts(); chartsBuilt=true; }
  if(id==='alerts') renderAlerts();
}

// ─────────────────────────────────────────────
// API FETCH
// ─────────────────────────────────────────────
async function apiGet(path, params={}) {
  try {
    const url = new URL(API+path);
    Object.entries(params).forEach(([k,v]) => { if(v) url.searchParams.set(k,v); });
    const r = await fetch(url);
    if(r.ok) return await r.json();
  } catch(e) {}
  return null;
}

// ─────────────────────────────────────────────
// HUB — LIVE STATS
// ─────────────────────────────────────────────
async function loadHubStats() {
  const s = await apiGet('/analytics/dashboard/stats');
  const el = document.getElementById('api-status');
  if(s) {
    el.textContent = '✅ API Online';
    el.className = 'badge-pill';
    document.getElementById('hub-total').textContent = s.total ?? '—';
    document.getElementById('hub-high').textContent = s.high_risk ?? '—';
    document.getElementById('hub-med').textContent = s.medium_risk ?? '—';
    document.getElementById('hub-cov').textContent = (s.coverage_rate ?? '—') + '%';
    document.getElementById('hub-high-pct').textContent = s.high_risk ? `${Math.round(s.high_risk/s.total*100)}% of total` : '';
  } else {
    el.textContent = '⚠️ API Offline';
    el.className = 'badge-pill warn';
    ['hub-total','hub-high','hub-med','hub-cov'].forEach(id => document.getElementById(id).textContent = 'N/A');
  }
  renderHubAlerts();
}

function renderHubAlerts() {
  const el = document.getElementById('hub-alerts');
  el.innerHTML = ALERTS_DATA.slice(0,2).map(a => `
    <div class="card-danger">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div style="font-size:14px;font-weight:700;color:white;">🚨 ${a.name} — ${a.id}</div>
        <span style="background:rgba(226,75,74,0.2);color:var(--danger);font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;">CRITICAL</span>
      </div>
      <div style="font-size:12px;color:var(--muted);margin-top:3px;">${a.sub} · ${a.cond}</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.7);margin-top:6px;">${a.msg}</div>
      <div style="font-size:11px;color:rgba(255,255,255,0.25);margin-top:6px;">${a.time}</div>
    </div>`).join('');
}

// ─────────────────────────────────────────────
// GEO MAP
// ─────────────────────────────────────────────
let geoMap, geoLayers = {}, decayMode = false, decayCircle = null;

function initGeoMap() {
  window.geoMapInit = true;
  geoMap = L.map('geo-map', {center:[-0.310,36.080],zoom:9});
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    {attribution:'© OpenStreetMap © CARTO',maxZoom:18}).addTo(geoMap);

  // Facilities
  const facMarkers = FACILITIES.map(f => {
    const c = f.type==='hospital'?'#1D9E75':f.type==='clinic'?'#185FA5':'#8B5CF6';
    const sz = f.type==='hospital'?9:f.type==='clinic'?7:5;
    const icon = L.divIcon({className:'',
      html:`<div style="width:${sz}px;height:${sz}px;background:${c};border-radius:${f.type==='dispensary'?'50%':'3px'};border:2px solid rgba(255,255,255,0.7);box-shadow:0 0 6px ${c}80;"></div>`,
      iconAnchor:[sz/2,sz/2]});
    return L.marker([f.lat,f.lng],{icon}).bindPopup(`<b>${f.name}</b><br>${f.type.charAt(0).toUpperCase()+f.type.slice(1)}`);
  });
  geoLayers.facilities = L.layerGroup(facMarkers).addTo(geoMap);
  document.getElementById('geo-fac-count').textContent = FACILITIES.length;

  // Households
  const hhMarkers = HH_DATA.map(hh => {
    const c = hh.risk==='High'?'#F87171':hh.risk==='Medium'?'#FCD34D':'#6EE7B7';
    const icon = L.divIcon({className:'',
      html:`<div style="width:12px;height:12px;background:${c};border-radius:50%;border:2px solid white;box-shadow:0 0 8px ${c};cursor:pointer;"></div>`,
      iconAnchor:[6,6]});
    return L.marker([hh.lat,hh.lng],{icon})
      .bindPopup(`<b>${hh.id}</b><br>${hh.name}, ${hh.age}yrs<br>${hh.cond}<br><span style="color:${c};font-weight:700;">${hh.risk} Risk</span> · ${hh.dist}km<br>${hh.ins}`);
  });
  geoLayers.households = L.layerGroup(hhMarkers);

  // Risk zones
  const riskZones = [
    {lat:-0.17,lng:36.12,r:8000,c:'#E24B4A',l:'Bahati High-Risk Zone'},
    {lat:-0.42,lng:35.70,r:12000,c:'#E24B4A',l:'Kuresoi High-Risk Zone'},
    {lat:-0.63,lng:35.99,r:9000,c:'#E24B4A',l:'Molo-Narok Risk Zone'},
    {lat:0.04,lng:36.22,r:7000,c:'#F59E0B',l:'Subukia Medium Zone'},
    {lat:-0.20,lng:35.85,r:6000,c:'#F59E0B',l:'Rongai Medium Zone'},
    {lat:-0.50,lng:36.33,r:5000,c:'#10B981',l:'Gilgil Low-Risk Zone'},
    {lat:-0.29,lng:36.07,r:4000,c:'#10B981',l:'Nakuru Town Low-Risk Zone'},
  ].map(z => L.circle([z.lat,z.lng],{color:z.c,fillColor:z.c,fillOpacity:.15,weight:1.5,opacity:.6,radius:z.r}).bindTooltip(z.l,{permanent:false}));
  geoLayers.risk = L.layerGroup(riskZones).addTo(geoMap);

  geoMap.on('click', e => {
    if(!decayMode) return;
    const {lat,lng} = e.latlng;
    if(decayCircle) geoMap.removeLayer(decayCircle);
    decayCircle = L.circle([lat,lng],{radius:35000,color:'#F59E0B',fillColor:'#F59E0B',fillOpacity:.05,weight:2,dashArray:'8 6'})
      .addTo(geoMap).bindTooltip('35km decay threshold',{permanent:true,direction:'top'});
    const results = HH_DATA.map(hh => {
      const d = geoMap.distance([lat,lng],[hh.lat,hh.lng])/1000;
      const score = Math.max(0,1-Math.pow(d/35,1.5)).toFixed(2);
      return {id:hh.id,d:d.toFixed(1),score,label:score>=.6?'Good access':score>=.3?'Moderate':'Poor access'};
    }).sort((a,b)=>b.score-a.score);
    const panel = document.getElementById('decay-results');
    const content = document.getElementById('decay-content');
    panel.style.display='block';
    content.innerHTML = results.map(r => {
      const c = parseFloat(r.score)>=.6?'var(--success)':parseFloat(r.score)>=.3?'var(--amber)':'var(--danger)';
      return `<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px;">
        <span style="font-family:monospace;color:var(--amber);font-weight:600;">${r.id}</span>
        <span style="color:var(--muted);">${r.d} km</span>
        <span style="color:${c};font-weight:700;">${r.label} (${r.score})</span>
      </div>`;
    }).join('');
    document.getElementById('geo-hint').textContent = '📌 Pin dropped · '+results.length+' households analysed';
    decayMode = false;
  });
}

function toggleGeoLayer(layer, btn) {
  btn.classList.toggle('active');
  const on = btn.classList.contains('active');
  if(!geoMap) return;
  if(on) geoLayers[layer].addTo(geoMap);
  else geoMap.removeLayer(geoLayers[layer]);
}

function activateDecayMode() {
  decayMode = true;
  document.getElementById('geo-hint').textContent = '📌 Click anywhere on the map to drop a pin…';
  document.getElementById('ctrl-decay').classList.add('active');
}

// ─────────────────────────────────────────────
// MOBILE CLINIC MAP
// ─────────────────────────────────────────────
let mcMap, mcHHMarkers=[], mcRouteLine=null, mcFilter='All', mcSelHH=null;

function initMCMap() {
  window.mcMapInit = true;
  mcMap = L.map('mc-map',{center:[-0.310,36.080],zoom:9});
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    {attribution:'© OpenStreetMap © CARTO',maxZoom:18}).addTo(mcMap);

  FACILITIES.forEach(f => {
    const c = f.type==='hospital'?'#1D9E75':f.type==='clinic'?'#185FA5':'#8B5CF6';
    const icon = L.divIcon({className:'',
      html:`<div style="width:8px;height:8px;background:${c};border-radius:2px;border:1.5px solid rgba(255,255,255,.6);opacity:.8;"></div>`,
      iconAnchor:[4,4]});
    L.marker([f.lat,f.lng],{icon}).bindTooltip(f.name).addTo(mcMap);
  });

  renderHHList();
}

function haversine(lat1,lng1,lat2,lng2) {
  const R=6371,dlat=(lat2-lat1)*Math.PI/180,dlng=(lng2-lng1)*Math.PI/180;
  const a=Math.sin(dlat/2)**2+Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dlng/2)**2;
  return R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));
}

function renderHHList() {
  const search = document.getElementById('hh-search').value.toLowerCase();
  const filtered = HH_DATA.filter(h => {
    const mR = mcFilter==='All'||h.risk===mcFilter;
    const mS = !search||(h.id.toLowerCase().includes(search)||h.name.toLowerCase().includes(search)||h.sub.toLowerCase().includes(search));
    return mR&&mS;
  });
  document.getElementById('hh-count').textContent = filtered.length+' Household'+(filtered.length!==1?'s':'');
  const el = document.getElementById('hh-list-body');
  el.innerHTML = filtered.map(hh => {
    const c = hh.risk==='High'?'#F87171':hh.risk==='Medium'?'#FCD34D':'#6EE7B7';
    const active = mcSelHH&&mcSelHH.id===hh.id?'active':'';
    return `<div class="hh-item ${active}" onclick='selectHH(${JSON.stringify(hh)})'>
      <div class="hh-id" style="color:${c};">${hh.id}</div>
      <div class="hh-name">${hh.name} · ${hh.sub}</div>
      <div class="hh-meta">${hh.dist} km · ${hh.cond}</div>
    </div>`;
  }).join('');

  // Sync map markers
  mcHHMarkers.forEach(m => mcMap.removeLayer(m.marker));
  mcHHMarkers = [];
  filtered.forEach(hh => {
    const c = hh.risk==='High'?'#F87171':hh.risk==='Medium'?'#FCD34D':'#6EE7B7';
    const isS = mcSelHH&&mcSelHH.id===hh.id;
    const icon = L.divIcon({className:'',
      html:`<div style="width:${isS?18:12}px;height:${isS?18:12}px;background:${c};border-radius:50%;border:${isS?3:2}px solid white;box-shadow:0 0 ${isS?16:8}px ${c};cursor:pointer;"></div>`,
      iconAnchor:[isS?9:6,isS?9:6]});
    const m = L.marker([hh.lat,hh.lng],{icon}).bindTooltip(`${hh.id} · ${hh.risk}`,{direction:'top'})
      .on('click',()=>selectHH(hh));
    m.addTo(mcMap);
    mcHHMarkers.push({marker:m,data:hh});
  });
}

function selectHH(hh) {
  mcSelHH = typeof hh==='string'?JSON.parse(hh):hh;
  renderHHList();
  const nearest = [...FACILITIES].map(f=>({...f,km:haversine(mcSelHH.lat,mcSelHH.lng,f.lat,f.lng)}))
    .sort((a,b)=>a.km-b.km);
  if(mcRouteLine) mcMap.removeLayer(mcRouteLine);
  mcRouteLine = L.polyline([[mcSelHH.lat,mcSelHH.lng],[nearest[0].lat,nearest[0].lng]],
    {color:'#F59E0B',weight:2.5,dashArray:'8 5',opacity:.85}).addTo(mcMap);
  mcMap.fitBounds([[mcSelHH.lat,mcSelHH.lng],[nearest[0].lat,nearest[0].lng]],{padding:[60,60],maxZoom:13});

  const rc = mcSelHH.risk==='High'?'#F87171':mcSelHH.risk==='Medium'?'#FCD34D':'#6EE7B7';
  const ic = mcSelHH.ins==='NHIF'?'#6EE7B7':mcSelHH.ins==='Partial'?'#FCD34D':'#F87171';
  document.getElementById('mc-detail').style.display='block';
  document.getElementById('mc-detail-inner').innerHTML = `
    <div class="detail-avatar" style="background:${rc}22;border-color:${rc}55;">🏠</div>
    <div>
      <div style="font-family:'Sora',sans-serif;font-size:15px;font-weight:700;color:white;">${mcSelHH.id}</div>
      <div style="font-size:12px;color:var(--muted);margin-top:2px;">${mcSelHH.name} · ${mcSelHH.age} yrs · ${mcSelHH.sub}</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:13px;font-weight:700;color:${rc};">${mcSelHH.risk} Risk</div>
      <div style="font-size:12px;font-weight:600;color:${ic};">${mcSelHH.ins}</div>
    </div>`;
  const typIcon = t => t==='hospital'?'🏥':t==='clinic'?'🏨':'💊';
  document.getElementById('mc-detail-facs').innerHTML = nearest.slice(0,3).map((f,i) => `
    <div class="fac-chip" style="${i===0?'border-color:rgba(245,158,11,.4);':''}">
      <div class="fac-chip-name">${typIcon(f.type)} ${f.name}</div>
      <div class="fac-chip-meta">${f.km.toFixed(1)} km · ${f.type}</div>
    </div>`).join('');
}

function filterHH(val) { renderHHList(); }
function setHHFilter(val, el) {
  mcFilter=val;
  document.querySelectorAll('.hh-list-header .map-ctrl-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  renderHHList();
}
function clearMCRoute() {
  if(mcRouteLine){mcMap.removeLayer(mcRouteLine);mcRouteLine=null;}
  mcSelHH=null;
  document.getElementById('mc-detail').style.display='none';
  renderHHList();
  if(mcMap) mcMap.setView([-0.310,36.080],9);
}

// ─────────────────────────────────────────────
// PREDICTIVE TRIAGE — hits FastAPI /predict_access
// ─────────────────────────────────────────────
async function runTriage() {
  const dist = parseFloat(document.getElementById('t-distance').value);
  const age  = document.getElementById('t-age').value;
  const gender = document.getElementById('t-gender').value;
  const wealth = document.getElementById('t-wealth').value;
  const ins  = parseInt(document.getElementById('t-insurance').value);
  const res  = document.getElementById('t-residence').value;

  const panel = document.getElementById('triage-result-panel');
  panel.innerHTML = `<div class="card" style="text-align:center;padding:40px;"><div class="loader" style="justify-content:center;"><div class="spinner"></div>Running prediction…</div></div>`;

  let acc = 72.0, ret = 65.0, source = 'fallback';

  try {
    const body = {
      distance_km: dist,
      age_group: age,
      gender: gender,
      wealth_index: wealth,
      insurance_status: ins,
      residential_area_group: res,
      survey_weight: 1.0
    };
    const r = await fetch(API+'/predict_access', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(body)
    });
    if(r.ok) {
      const data = await r.json();
      acc = data.probability ?? acc;
      source = 'XGBoost · Live';
    }
  } catch(e) {}

  // Simulate retention from access (model not exposed separately)
  ret = Math.max(10, Math.min(95, acc * 0.88 - (dist > 35 ? 8 : 0)));

  const ac = acc>=70?'#6EE7B7':acc>=40?'#FCD34D':'#F87171';
  const rc = ret>=70?'#6EE7B7':ret>=40?'#FCD34D':'#F87171';
  const zoneColor = dist<=35?'#6EE7B7':'#F87171';
  const zoneLabel = dist<=35?'🟢 Safe Zone (≤35km)':'🔴 Beyond 35km Threshold';
  const advice = acc>=70
    ? `<div class="card-teal">✅ <b>High likelihood of access.</b> Standard outreach schedule appropriate.</div>`
    : acc>=40
    ? `<div class="card-warning">⚡ <b>Moderate likelihood.</b> Consider transport support or CHW follow-up.</div>`
    : `<div class="card-danger">🚨 <b>Low likelihood.</b> Prioritise mobile clinic or immediate CHW dispatch.</div>`;

  panel.innerHTML = `
    <div class="card">
      <div class="card-title">Prediction Results · ${source}</div>
      <div class="result-grid">
        <div class="result-card">
          <div class="result-label">Access Probability</div>
          <div class="result-val" style="color:${ac};">${acc.toFixed(1)}%</div>
          <div class="result-sub">XGBoost · FastAPI</div>
        </div>
        <div class="result-card">
          <div class="result-label">Retention Probability</div>
          <div class="result-val" style="color:${rc};">${ret.toFixed(1)}%</div>
          <div class="result-sub">Stage 2 · Estimated</div>
        </div>
      </div>
      <div style="font-size:13px;font-weight:600;color:${zoneColor};margin-bottom:12px;">${zoneLabel} · ${dist} km</div>
      ${advice}
    </div>`;
}

// distance warning
document.getElementById('t-distance').addEventListener('input', function() {
  const w = document.getElementById('t-dist-warning');
  w.style.display = parseFloat(this.value)>35?'block':'none';
});

// ─────────────────────────────────────────────
// PATIENT DATABASE
// ─────────────────────────────────────────────
let allPatients = [], filteredPatients = [], dbPage = 1;
const PAGE_SIZE = 10;
let sortKey = '', sortDir = 1;

async function loadPatients() {
  const data = await apiGet('/patients/', {page:1, page_size:100});
  if(data && data.data) {
    allPatients = data.data;
  } else {
    allPatients = HH_DATA.map(h => ({
      id:h.id,name:h.name,age:h.age,gender:h.risk==='High'?'M':'F',
      sub_county:h.sub,condition:h.cond,risk:h.risk,
      distance_km:h.dist,insurance:h.ins,last_visit:'N/A'
    }));
  }
  filteredPatients = [...allPatients];
  updateDBStats();
  renderDBTable();
}

function updateDBStats() {
  document.getElementById('db-total').textContent = allPatients.length;
  document.getElementById('db-high').textContent  = allPatients.filter(p=>p.risk==='High').length;
  document.getElementById('db-med').textContent   = allPatients.filter(p=>p.risk==='Medium').length;
  document.getElementById('db-low').textContent   = allPatients.filter(p=>p.risk==='Low').length;
  document.getElementById('db-nhif').textContent  = allPatients.filter(p=>p.insurance==='NHIF').length;
  document.getElementById('db-count').textContent = allPatients.length+' records';
}

function filterDB() {
  const q   = (document.getElementById('db-search').value||'').toLowerCase();
  const risk = document.getElementById('db-risk-filter').value;
  const sub  = document.getElementById('db-sub-filter').value;
  filteredPatients = allPatients.filter(p => {
    const mQ = !q||(p.id||'').toLowerCase().includes(q)||(p.name||'').toLowerCase().includes(q)||(p.sub_county||'').toLowerCase().includes(q);
    const mR = !risk||p.risk===risk;
    const mS = !sub||p.sub_county===sub;
    return mQ&&mR&&mS;
  });
  dbPage=1;
  renderDBTable();
}

function sortDB(key) {
  if(sortKey===key) sortDir*=-1; else {sortKey=key;sortDir=1;}
  filteredPatients.sort((a,b)=>{
    const va=a[key]||'',vb=b[key]||'';
    return va<vb?-sortDir:va>vb?sortDir:0;
  });
  renderDBTable();
}

function dbPage(dir) {
  const total = Math.ceil(filteredPatients.length/PAGE_SIZE);
  dbPage = Math.max(1,Math.min(total,dbPage+dir));
  renderDBTable();
}

function renderDBTable() {
  const start = (dbPage-1)*PAGE_SIZE;
  const rows  = filteredPatients.slice(start,start+PAGE_SIZE);
  const total = Math.ceil(filteredPatients.length/PAGE_SIZE);
  document.getElementById('db-page-info').textContent =
    `Showing ${start+1}–${Math.min(start+PAGE_SIZE,filteredPatients.length)} of ${filteredPatients.length} · Page ${dbPage} of ${total}`;
  document.getElementById('db-prev').disabled = dbPage===1;
  document.getElementById('db-next').disabled = dbPage===total||total===0;

  const tbody = document.getElementById('db-tbody');
  if(!rows.length){
    tbody.innerHTML = `<tr><td colspan="10" style="text-align:center;color:var(--muted);padding:32px;">No patients match the current filters</td></tr>`;
    return;
  }
  tbody.innerHTML = rows.map(p => {
    const rc = p.risk==='High'?'pill-high':p.risk==='Medium'?'pill-med':'pill-low';
    const ic = p.insurance==='NHIF'?'color:#6EE7B7;':p.insurance==='Partial'?'color:#FCD34D;':'color:#F87171;';
    return `<tr>
      <td style="font-family:monospace;color:var(--amber);font-size:12px;">${p.id||''}</td>
      <td style="font-weight:600;color:white;">${p.name||''}</td>
      <td>${p.age||''}</td>
      <td>${p.gender||''}</td>
      <td><span style="background:rgba(29,158,117,0.15);color:var(--teal-mid);padding:2px 8px;border-radius:4px;font-size:11px;">${p.sub_county||''}</span></td>
      <td>${p.condition||''}</td>
      <td><span class="pill ${rc}">${p.risk||''}</span></td>
      <td style="color:${(p.distance_km||0)>35?'var(--danger)':'rgba(255,255,255,0.7)'};">${p.distance_km||''}</td>
      <td style="${ic}font-weight:600;">${p.insurance||''}</td>
      <td style="color:var(--muted);font-size:12px;">${p.last_visit||'N/A'}</td>
    </tr>`;
  }).join('');
}

function exportCSV() {
  const data = filteredPatients.length?filteredPatients:allPatients;
  if(!data.length){alert('No patient data loaded yet.');return;}
  const headers = ['ID','Name','Age','Gender','Sub-county','Condition','Risk','Distance(km)','Insurance','Last Visit'];
  const csv = [headers.join(','), ...data.map(p =>
    [p.id,`"${p.name}"`,p.age,p.gender,p.sub_county,`"${p.condition}"`,p.risk,p.distance_km,p.insurance,p.last_visit||'N/A'].join(',')
  )].join('\n');
  const blob = new Blob([csv],{type:'text/csv'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'Nakuru_Patients.csv';
  a.click();
}

// ─────────────────────────────────────────────
// REPORTS — CHARTS
// ─────────────────────────────────────────────
function buildCharts() {
  // SHAP bar chart
  const shCtx = document.getElementById('shap-chart').getContext('2d');
  new Chart(shCtx, {
    type:'bar',
    data:{
      labels:['Education Level','Distance (km)','Wealth Index','Insurance Status'],
      datasets:[{
        label:'SHAP Importance (%)',
        data:[73.2,12.9,8.4,5.5],
        backgroundColor:['#6366F1','#F59E0B','#F59E0B','#F59E0B'],
        borderRadius:6,
      }]
    },
    options:{
      indexAxis:'y',
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{
        x:{ticks:{color:'rgba(255,255,255,0.4)'},grid:{color:'rgba(255,255,255,0.06)'},max:90},
        y:{ticks:{color:'white',font:{size:13}},grid:{display:false}}
      }
    }
  });

  // GAM decay chart
  const gmCtx = document.getElementById('gam-chart').getContext('2d');
  const GAM_D = [0,5,10,15,20,25,30,35,40,50,60];
  const GAM_P = [0.899,0.905,0.910,0.914,0.916,0.918,0.910,0.895,0.875,0.840,0.800];
  new Chart(gmCtx, {
    type:'line',
    data:{
      labels:GAM_D,
      datasets:[
        {label:'P(Access | Distance)',data:GAM_P,
         borderColor:'#1D9E75',backgroundColor:'rgba(29,158,117,0.08)',
         borderWidth:3,pointBackgroundColor:'#5DCAA5',pointRadius:6,fill:true,tension:.3},
      ]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{
        legend:{labels:{color:'white',font:{size:12}}},
        annotation:{annotations:{line1:{type:'line',xMin:35,xMax:35,borderColor:'#F59E0B',borderWidth:2,borderDash:[6,4],label:{content:'35km threshold',enabled:true,color:'#F59E0B',backgroundColor:'transparent'}}}},
      },
      scales:{
        x:{title:{display:true,text:'Distance to Facility (km)',color:'rgba(255,255,255,0.5)'},
           ticks:{color:'rgba(255,255,255,0.4)'},grid:{color:'rgba(255,255,255,0.06)'}},
        y:{title:{display:true,text:'Access Probability',color:'rgba(255,255,255,0.5)'},
           ticks:{color:'rgba(255,255,255,0.4)',callback:v=>(v*100).toFixed(0)+'%'},
           grid:{color:'rgba(255,255,255,0.06)'},min:.78,max:.93}
      }
    }
  });
}

// ─────────────────────────────────────────────
// ACCORDION
// ─────────────────────────────────────────────
function toggleAccordion(header) {
  const body = header.nextElementSibling;
  const chevron = header.querySelector('.chevron');
  const isOpen = body.classList.contains('open');
  body.classList.toggle('open',!isOpen);
  header.classList.toggle('open',!isOpen);
  chevron.classList.toggle('open',!isOpen);
  if(!chartsBuilt && !isOpen){ buildCharts(); chartsBuilt=true; }
}

// ─────────────────────────────────────────────
// ALERTS
// ─────────────────────────────────────────────
function renderAlerts() {
  const el = document.getElementById('alerts-list');
  const crit = ALERTS_DATA.filter(a=>a.sev==='critical').length;
  document.getElementById('alerts-crit-badge').textContent = crit+' Critical';

  el.innerHTML = ALERTS_DATA.map(a => {
    const isCrit = a.sev==='critical';
    const cardClass = isCrit?'card-danger':'card-warning';
    const icon = isCrit?'🚨':'⚠️';
    const badge = isCrit?'CRITICAL':'WARNING';
    const bc = isCrit?'var(--danger)':'var(--amber)';
    const bbg = isCrit?'rgba(226,75,74,0.2)':'rgba(245,158,11,0.2)';
    const ecHtml = a.phone?`
      <div class="alert-ec">
        <span style="font-size:20px;">📞</span>
        <div>
          <div style="font-size:11px;color:var(--muted);">Emergency Contact</div>
          <div style="font-size:13px;font-weight:600;color:white;">${a.ec} · ${a.rel}</div>
        </div>
        <div style="margin-left:auto;font-size:14px;font-weight:700;color:var(--danger);">${a.phone}</div>
      </div>`:'';
    return `
      <div class="${cardClass}">
        <div style="position:absolute;top:16px;right:16px;background:${bbg};color:${bc};font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;">${badge}</div>
        <div style="display:flex;align-items:flex-start;gap:14px;">
          <div style="font-size:24px;flex-shrink:0;">${icon}</div>
          <div style="flex:1;">
            <div class="alert-title">Emergency: ${a.name} — ${a.id}</div>
            <div class="alert-sub">${a.sub} · ${a.cond}</div>
            <div class="alert-msg">${a.msg}</div>
            ${ecHtml}
            <div class="alert-time">${a.time}</div>
            ${a.phone?`<div class="alert-actions">
              <button class="btn-call" onclick="callContact('${a.phone}')">📞 Call Emergency Contact</button>
              <button class="btn-ack">Dispatch Mobile Clinic</button>
              <button class="btn-ack" onclick="this.closest('.${cardClass}').style.opacity='.5';">Acknowledge</button>
            </div>`:'<div class="alert-actions"><button class="btn-ack">Route Mobile Clinic</button><button class="btn-ack" onclick="this.closest(\'.${cardClass}\').style.opacity=\'.5\';">Acknowledge</button></div>'}
          </div>
        </div>
      </div>`;
  }).join('');
}

function callContact(phone) {
  alert(`📞 Initiating call to ${phone}\n\nIn a live deployment this would dial via your registered telephony system.`);
}

// ─────────────────────────────────────────────
// SETTINGS
// ─────────────────────────────────────────────
function saveSettings() {
  alert('✅ Settings saved successfully.');
}

// ─────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  loadHubStats();
  loadPatients();
  renderAlerts();
});
</script>
</body>
</html>
