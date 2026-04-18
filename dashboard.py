<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HealthLink Kenya</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
:root{
  --bg:#0A1929;--sur:#0C2340;--sur2:#0F2847;
  --teal:#1D9E75;--tm:#5DCAA5;--td:#0F6E56;
  --navy:#185FA5;--tx:#e2e8f0;--mu:rgba(255,255,255,.45);
  --bd:rgba(255,255,255,.08);--dan:#F87171;--amb:#FCD34D;--suc:#6EE7B7;
  --r:12px;--rs:8px;
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:var(--bg);color:var(--tx);font-family:'Segoe UI',Arial,sans-serif;font-size:14px;min-height:100vh}
/* TOPBAR */
.topbar{position:sticky;top:0;z-index:1000;background:var(--sur);border-bottom:1px solid var(--bd);
  display:flex;align-items:center;justify-content:space-between;padding:0 20px;height:52px;gap:10px}
.logo{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:700;color:#fff}
.logo-dot{width:26px;height:26px;background:linear-gradient(135deg,var(--teal),var(--navy));border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:13px}
.tbar-r{display:flex;align-items:center;gap:10px;font-size:12px}
.pill{padding:3px 9px;border-radius:20px;font-size:11px;font-weight:600}
.p-api{background:rgba(29,158,117,.15);border:1px solid rgba(29,158,117,.3);color:var(--suc)}
.p-hi{background:rgba(248,113,113,.18);color:var(--dan)}
.p-me{background:rgba(252,211,77,.18);color:var(--amb)}
.p-lo{background:rgba(110,231,183,.18);color:var(--suc)}
.p-pa{background:rgba(255,255,255,.1);color:var(--mu)}
/* NAV */
.nav{background:var(--sur);border-bottom:1px solid var(--bd);display:flex;padding:0 14px;overflow-x:auto;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
.nb{background:transparent;border:none;border-bottom:3px solid transparent;color:var(--mu);
  padding:12px 13px;font-size:13px;font-weight:500;cursor:pointer;white-space:nowrap;transition:all .15s}
.nb:hover{color:rgba(255,255,255,.85);background:rgba(255,255,255,.04)}
.nb.active{color:var(--tm);border-bottom-color:var(--tm);font-weight:600}
/* MAIN */
.main{padding:22px 24px}
.page{display:none}.page.active{display:block;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
/* HEADERS */
.ph{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:18px;flex-wrap:wrap;gap:10px}
.pt{font-size:20px;font-weight:700;color:#fff}
.ps{font-size:12px;color:var(--mu);margin-top:2px}
/* STAT GRID */
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:18px}
.sc{background:var(--sur);border:1px solid var(--bd);border-radius:var(--rs);padding:13px 15px}
.sv{font-size:24px;font-weight:700;color:#fff;margin-bottom:2px}
.sl{font-size:11px;color:var(--mu);text-transform:uppercase;letter-spacing:.05em}
.sd{font-size:11px;font-weight:600;color:var(--tm);margin-top:3px}
/* HUB GRID */
.hg{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}
.hb{background:var(--sur2);border:1px solid var(--bd);border-radius:var(--r);padding:20px 10px 16px;text-align:center;cursor:pointer;transition:all .2s}
.hb:hover{background:rgba(29,158,117,.12);border-color:var(--tm);transform:translateY(-2px)}
.hi{font-size:26px;margin-bottom:7px;display:block}
.hl{font-size:13px;font-weight:600;color:#fff}
.hd{font-size:11px;color:var(--mu);margin-top:2px}
/* CARD */
.card{background:var(--sur);border:1px solid var(--bd);border-radius:var(--r);padding:16px;margin-bottom:12px}
.ct{font-size:11px;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px}
/* ALERT CARDS */
.ac{border-radius:var(--r);padding:14px 16px;margin-bottom:10px;position:relative}
.ac-c{background:rgba(248,113,113,.08);border-left:4px solid var(--dan)}
.ac-w{background:rgba(252,211,77,.08);border-left:4px solid var(--amb)}
.ac-g{background:rgba(29,158,117,.08);border:1px solid rgba(29,158,117,.25)}
.ac-head{display:flex;align-items:flex-start;gap:8px;margin-bottom:6px}
.ac-badge{font-size:10px;font-weight:700;padding:2px 7px;border-radius:3px;letter-spacing:.05em}
.ac-badge-c{background:rgba(248,113,113,.25);color:var(--dan)}
.ac-badge-w{background:rgba(252,211,77,.25);color:var(--amb)}
.ac-badge-g{background:rgba(29,158,117,.25);color:var(--suc)}
.ac-title{font-size:13px;font-weight:600;color:#fff}
.ac-body{font-size:12px;color:rgba(255,255,255,.65);margin-bottom:10px;line-height:1.5}
.ac-contact{background:rgba(255,255,255,.04);border-radius:var(--rs);padding:8px 10px;margin-bottom:10px;font-size:12px}
.ac-actions{display:flex;flex-wrap:wrap;gap:7px}
.ac-ts{font-size:11px;color:var(--mu);margin-top:8px}
/* BUTTONS */
.btn{padding:7px 13px;border-radius:var(--rs);font-size:12px;font-weight:600;cursor:pointer;border:none;transition:all .15s;font-family:inherit}
.btn-d{background:rgba(248,113,113,.15);border:1px solid rgba(248,113,113,.35);color:var(--dan)}
.btn-d:hover{background:rgba(248,113,113,.25)}
.btn-t{background:rgba(29,158,117,.15);border:1px solid rgba(29,158,117,.35);color:var(--suc)}
.btn-t:hover{background:rgba(29,158,117,.25)}
.btn-n{background:rgba(24,95,165,.15);border:1px solid rgba(24,95,165,.35);color:#7eb8f7}
.btn-n:hover{background:rgba(24,95,165,.25)}
.btn-g{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);color:var(--tx)}
.btn-g:hover{background:rgba(255,255,255,.12)}
.btn-pri{background:var(--teal);color:#fff;border:none;padding:8px 16px}
.btn-pri:hover{background:var(--td)}
/* TABLE */
.tw{overflow-x:auto;border-radius:var(--r);border:1px solid var(--bd)}
table{width:100%;border-collapse:collapse}
thead th{font-size:11px;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.05em;
  padding:10px 12px;text-align:left;border-bottom:1px solid var(--bd);background:var(--sur);cursor:pointer}
thead th:hover{color:#fff}
tbody td{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.04);font-size:12px;color:rgba(255,255,255,.8);background:var(--sur2)}
tbody tr:hover td{background:rgba(255,255,255,.03);cursor:pointer}
/* MAP */
.map-wrap{border-radius:var(--r);overflow:hidden;border:1px solid var(--bd)}
#geo-map,#mc-map{width:100%;height:420px}
/* TOOLBAR */
.tb{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;align-items:center}
.fc{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:#fff;
  padding:7px 10px;border-radius:var(--rs);font-size:12px;font-family:inherit;width:auto}
.fc:focus{outline:none;border-color:var(--tm)}
.fc option{background:var(--sur)}
.fi{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:#fff;
  padding:7px 10px;border-radius:var(--rs);font-size:12px;font-family:inherit;flex:1;min-width:200px}
.fi:focus{outline:none;border-color:var(--tm)}
.fi::placeholder{color:var(--mu)}
/* FORM */
.fg{display:flex;flex-direction:column;gap:5px;margin-bottom:12px}
.fl{font-size:11px;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.05em}
.fci{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:#fff;
  padding:8px 11px;border-radius:var(--rs);font-size:13px;font-family:inherit;width:100%}
.fci:focus{outline:none;border-color:var(--tm)}
input[type=range]{-webkit-appearance:none;width:100%;height:4px;border-radius:2px;background:rgba(255,255,255,.15);outline:none}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:var(--teal);cursor:pointer}
.toggle-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--bd)}
.toggle-sw{position:relative;width:38px;height:22px;cursor:pointer}
.toggle-sw input{opacity:0;width:0;height:0;position:absolute}
.toggle-track{display:block;width:38px;height:22px;background:rgba(255,255,255,.15);border-radius:11px;transition:.2s}
.toggle-sw input:checked + .toggle-track{background:var(--teal)}
.toggle-track::after{content:'';position:absolute;left:3px;top:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:.2s}
.toggle-sw input:checked + .toggle-track::after{transform:translateX(16px)}
/* MODAL */
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:9000;align-items:center;justify-content:center;padding:16px}
.modal-bg.show{display:flex}
.modal{background:var(--sur);border:1px solid var(--bd);border-radius:var(--r);width:100%;max-width:640px;max-height:90vh;overflow-y:auto;padding:22px}
.modal-close{float:right;background:rgba(255,255,255,.1);border:none;color:#fff;width:26px;height:26px;border-radius:50%;cursor:pointer;font-size:14px;line-height:1;display:flex;align-items:center;justify-content:center}
.profile-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.pf{background:rgba(255,255,255,.04);border-radius:var(--rs);padding:10px 12px}
.pf-l{font-size:10px;color:var(--mu);text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px}
.pf-v{font-size:13px;color:#fff;font-weight:500}
/* RISK BAR */
.risk-bar{height:6px;border-radius:3px;background:rgba(255,255,255,.1);margin-top:4px;overflow:hidden}
.risk-fill{height:100%;border-radius:3px}
/* MAP LEGEND */
.map-leg{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;font-size:12px;color:var(--mu)}
.leg-dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:4px;vertical-align:middle}
/* DISTANCE DECAY */
.decay-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px}
.dz{border-radius:var(--rs);padding:12px 14px;text-align:center}
.dz-safe{background:rgba(29,158,117,.1);border:1px solid rgba(29,158,117,.25)}
.dz-tr{background:rgba(252,211,77,.1);border:1px solid rgba(252,211,77,.25)}
.dz-ex{background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.25)}
.dz-val{font-size:22px;font-weight:700;color:#fff}
.dz-lab{font-size:11px;color:var(--mu);margin-top:2px}
/* MC household card */
.hh-card{background:var(--sur2);border:1px solid var(--bd);border-radius:var(--rs);padding:12px 14px;margin-bottom:8px;cursor:pointer;display:flex;align-items:center;gap:12px;transition:border-color .15s}
.hh-card:hover{border-color:var(--tm)}
.hh-card.selected{border-color:var(--teal);background:rgba(29,158,117,.08)}
.hh-icon{width:38px;height:38px;border-radius:var(--rs);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.hh-info{flex:1;min-width:0}
.hh-name{font-size:13px;font-weight:600;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hh-sub{font-size:11px;color:var(--mu);margin-top:1px}
/* Settings */
.set-section{margin-bottom:22px;padding-bottom:18px;border-bottom:1px solid var(--bd)}
.set-section:last-child{border-bottom:none}
.set-title{font-size:14px;font-weight:600;color:#fff;margin-bottom:12px}
/* Summary bar for DB */
.sum-bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;padding:10px 14px;background:var(--sur);border-radius:var(--rs);border:1px solid var(--bd);align-items:center;font-size:12px}
.sum-item{display:flex;align-items:center;gap:5px;color:var(--mu)}
.sum-val{font-weight:700;color:#fff}
/* scrollable list */
.hh-list{max-height:370px;overflow-y:auto;padding-right:4px}
.hh-list::-webkit-scrollbar{width:4px}
.hh-list::-webkit-scrollbar-track{background:transparent}
.hh-list::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:2px}
/* layout helpers */
.row{display:flex;gap:14px;align-items:flex-start}
.col-l{flex:0 0 300px;min-width:0}
.col-r{flex:1;min-width:0}
@media(max-width:700px){.row{flex-direction:column}.col-l{flex:unset;width:100%}.decay-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<!-- DATA -->
<script>
const PATIENTS = [{"id":"HH-NK-01100","name":"Mary Wanjiku","age":34,"gender":"F","sub_county":"Nakuru Town","condition":"Hypertension","risk":"High","distance":2.3,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.27805,"lng":36.06978,"contact_name":"James Wanjiku (Spouse)","contact_phone":"+254 712 445 678","dropout_score":0.72,"access_score":0.85,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Long-term hypertension patient. On medication since 2023."},{"id":"HH-NK-01101","name":"John Kamau","age":61,"gender":"M","sub_county":"Rongai","condition":"Diabetes T2","risk":"Low","distance":38.0,"insurance":"None","last_visit":"2026-03-12","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.15202,"lng":35.83443,"contact_name":"Thomas (Brother)","contact_phone":"+254 720 564 103","dropout_score":0.91,"access_score":0.88,"nearest_facility":"Rongai Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01102","name":"Grace Achieng","age":50,"gender":"F","sub_county":"Subukia","condition":"Maternal Care","risk":"Low","distance":48.1,"insurance":"NHIF","last_visit":"NaN","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":0.05123,"lng":36.16683,"contact_name":"Mary (Aunt)","contact_phone":"+254 769 897 643","dropout_score":0.88,"access_score":0.67,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Stable condition."},{"id":"HH-NK-01103","name":"Peter Mwangi","age":41,"gender":"M","sub_county":"Molo","condition":"TB Follow-up","risk":"Low","distance":46.0,"insurance":"NHIF","last_visit":"2026-01-15","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.29646,"lng":35.74578,"contact_name":"Peter (Mother)","contact_phone":"+254 793 597 935","dropout_score":0.16,"access_score":0.79,"nearest_facility":"Molo District Hospital","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01104","name":"Fatuma Hassan","age":60,"gender":"F","sub_county":"Naivasha","condition":"HIV Care","risk":"Medium","distance":30.9,"insurance":"NHIF","last_visit":"2026-04-10","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.7323,"lng":36.38889,"contact_name":"Francis (Son)","contact_phone":"+254 791 419 508","dropout_score":0.95,"access_score":0.71,"nearest_facility":"Naivasha District Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01105","name":"James Omondi","age":25,"gender":"M","sub_county":"Gilgil","condition":"Malaria","risk":"High","distance":4.9,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.54318,"lng":36.28023,"contact_name":"Grace (Mother)","contact_phone":"+254 729 169 132","dropout_score":0.83,"access_score":0.26,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01106","name":"Aisha Karimi","age":31,"gender":"F","sub_county":"Bahati","condition":"Asthma","risk":"Medium","distance":40.2,"insurance":"Partial","last_visit":"2026-04-10","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.16937,"lng":36.24054,"contact_name":"Francis (Uncle)","contact_phone":"+254 712 199 774","dropout_score":0.47,"access_score":0.53,"nearest_facility":"Bahati Health Centre","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01107","name":"Alex Maina","age":61,"gender":"M","sub_county":"Njoro","condition":"Mental Health","risk":"Medium","distance":36.1,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.29191,"lng":35.95748,"contact_name":"Francis (Sister)","contact_phone":"+254 768 559 243","dropout_score":0.46,"access_score":0.42,"nearest_facility":"Njoro Health Centre","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01108","name":"Purity Njeri","age":46,"gender":"F","sub_county":"Nakuru Town","condition":"Renal Disease","risk":"Low","distance":47.3,"insurance":"NHIF","last_visit":"NaN","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.20311,"lng":36.12176,"contact_name":"Agnes (Mother)","contact_phone":"+254 721 516 597","dropout_score":0.51,"access_score":0.87,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01109","name":"Samuel Koech","age":42,"gender":"M","sub_county":"Rongai","condition":"Cancer Screening","risk":"High","distance":22.4,"insurance":"Partial","last_visit":"2026-04-01","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.22936,"lng":35.89145,"contact_name":"Moses (Son)","contact_phone":"+254 719 294 403","dropout_score":0.29,"access_score":0.25,"nearest_facility":"Rongai Health Centre","visit_type":"Urgent","notes":"Patient enrolled Jan 2026. Requires follow-up."},{"id":"HH-NK-01110","name":"Jane Muthoni","age":65,"gender":"F","sub_county":"Subukia","condition":"Post-surgery","risk":"Medium","distance":4.2,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.00481,"lng":36.28872,"contact_name":"Mary (Mother)","contact_phone":"+254 708 709 169","dropout_score":0.67,"access_score":0.38,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01111","name":"Francis Kariuki","age":55,"gender":"M","sub_county":"Molo","condition":"Malnutrition","risk":"Medium","distance":34.6,"insurance":"NHIF","last_visit":"2026-04-10","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.24456,"lng":35.70562,"contact_name":"Francis (Brother)","contact_phone":"+254 785 833 421","dropout_score":0.3,"access_score":0.51,"nearest_facility":"Molo District Hospital","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01112","name":"Sarah Odhiambo","age":47,"gender":"F","sub_county":"Naivasha","condition":"Arthritis","risk":"Medium","distance":41.7,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.70061,"lng":36.44508,"contact_name":"Peter (Mother)","contact_phone":"+254 768 318 618","dropout_score":0.33,"access_score":0.93,"nearest_facility":"Naivasha District Hospital","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01113","name":"David Otieno","age":41,"gender":"M","sub_county":"Gilgil","condition":"Epilepsy","risk":"High","distance":24.9,"insurance":"None","last_visit":"2026-03-12","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.48213,"lng":36.40296,"contact_name":"James (Son)","contact_phone":"+254 785 936 667","dropout_score":0.35,"access_score":0.72,"nearest_facility":"Gilgil District Hospital","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01114","name":"Agnes Kimotho","age":34,"gender":"F","sub_county":"Bahati","condition":"Typhoid","risk":"High","distance":7.2,"insurance":"None","last_visit":"2026-03-12","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.19992,"lng":36.1487,"contact_name":"Francis (Aunt)","contact_phone":"+254 787 749 973","dropout_score":0.32,"access_score":0.58,"nearest_facility":"Bahati Health Centre","visit_type":"Resolved","notes":"Patient enrolled Jan 2026. Requires follow-up."},{"id":"HH-NK-01115","name":"Robert Mugo","age":23,"gender":"M","sub_county":"Njoro","condition":"Hypertension","risk":"Medium","distance":45.9,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.29662,"lng":36.04194,"contact_name":"Mary (Brother)","contact_phone":"+254 794 552 664","dropout_score":0.7,"access_score":0.64,"nearest_facility":"Njoro Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01116","name":"Winnie Otieno","age":52,"gender":"F","sub_county":"Nakuru Town","condition":"Diabetes T2","risk":"High","distance":21.3,"insurance":"None","last_visit":"2026-03-22","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.34261,"lng":36.03732,"contact_name":"Charles (Spouse)","contact_phone":"+254 726 798 355","dropout_score":0.67,"access_score":0.48,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01117","name":"Joseph Kipchoge","age":57,"gender":"M","sub_county":"Rongai","condition":"Maternal Care","risk":"Low","distance":51.0,"insurance":"NHIF","last_visit":"2026-02-20","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.11881,"lng":35.90972,"contact_name":"James (Uncle)","contact_phone":"+254 722 854 440","dropout_score":0.77,"access_score":0.52,"nearest_facility":"Rongai Health Centre","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01118","name":"Esther Njoki","age":35,"gender":"F","sub_county":"Subukia","condition":"TB Follow-up","risk":"High","distance":39.0,"insurance":"NHIF","last_visit":"2026-01-15","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":0.10737,"lng":36.17059,"contact_name":"Charles (Neighbour)","contact_phone":"+254 739 940 914","dropout_score":0.84,"access_score":0.37,"nearest_facility":"Subukia Health Centre","visit_type":"Urgent","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01119","name":"Moses Waweru","age":39,"gender":"M","sub_county":"Molo","condition":"HIV Care","risk":"High","distance":5.2,"insurance":"None","last_visit":"2026-03-18","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.23236,"lng":35.71895,"contact_name":"Joyce (Son)","contact_phone":"+254 703 218 998","dropout_score":0.92,"access_score":0.34,"nearest_facility":"Molo District Hospital","visit_type":"Resolved","notes":"Patient enrolled Mar 2026. Requires follow-up."},{"id":"HH-NK-01120","name":"Hawa Ibrahim","age":20,"gender":"F","sub_county":"Naivasha","condition":"Malaria","risk":"High","distance":24.7,"insurance":"None","last_visit":"2026-03-18","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.73018,"lng":36.51248,"contact_name":"Esther (Mother)","contact_phone":"+254 773 294 360","dropout_score":0.14,"access_score":0.54,"nearest_facility":"Naivasha District Hospital","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01121","name":"Henry Njenga","age":41,"gender":"M","sub_county":"Gilgil","condition":"Asthma","risk":"Medium","distance":52.3,"insurance":"Partial","last_visit":"2026-04-10","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.52977,"lng":36.38068,"contact_name":"Jane (Brother)","contact_phone":"+254 739 782 518","dropout_score":0.38,"access_score":0.74,"nearest_facility":"Gilgil District Hospital","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01122","name":"Miriam Chepkemoi","age":44,"gender":"F","sub_county":"Bahati","condition":"Mental Health","risk":"Medium","distance":21.8,"insurance":"None","last_visit":"2026-02-20","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.14652,"lng":36.16315,"contact_name":"James (Son)","contact_phone":"+254 738 393 315","dropout_score":0.47,"access_score":0.65,"nearest_facility":"Bahati Health Centre","visit_type":"Urgent","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01123","name":"Charles Mutua","age":46,"gender":"M","sub_county":"Njoro","condition":"Renal Disease","risk":"Medium","distance":12.9,"insurance":"NHIF","last_visit":"2026-02-20","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.31458,"lng":35.98541,"contact_name":"Joyce (Daughter)","contact_phone":"+254 711 938 869","dropout_score":0.3,"access_score":0.44,"nearest_facility":"Njoro Health Centre","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01124","name":"Joyce Mwangi","age":19,"gender":"F","sub_county":"Nakuru Town","condition":"Cancer Screening","risk":"High","distance":54.1,"insurance":"None","last_visit":"2026-02-03","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.29013,"lng":36.12978,"contact_name":"Francis (Daughter)","contact_phone":"+254 791 813 493","dropout_score":0.52,"access_score":0.39,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled Jan 2026. Requires follow-up."},{"id":"HH-NK-01125","name":"Patrick Njoroge","age":66,"gender":"M","sub_county":"Rongai","condition":"Post-surgery","risk":"Low","distance":48.9,"insurance":"None","last_visit":"2026-03-01","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.24686,"lng":35.93327,"contact_name":"Ann (Son)","contact_phone":"+254 706 670 355","dropout_score":0.88,"access_score":0.29,"nearest_facility":"Rongai Health Centre","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01126","name":"Ruth Wambui","age":60,"gender":"F","sub_county":"Subukia","condition":"Malnutrition","risk":"Medium","distance":31.4,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":0.06802,"lng":36.25008,"contact_name":"Thomas (Son)","contact_phone":"+254 770 556 262","dropout_score":0.73,"access_score":0.57,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01127","name":"Thomas Onyango","age":71,"gender":"M","sub_county":"Molo","condition":"Arthritis","risk":"Medium","distance":42.5,"insurance":"None","last_visit":"NaN","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.29672,"lng":35.72538,"contact_name":"Agnes (Brother)","contact_phone":"+254 734 443 427","dropout_score":0.86,"access_score":0.26,"nearest_facility":"Molo District Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01128","name":"Lydia Chebet","age":62,"gender":"F","sub_county":"Naivasha","condition":"Epilepsy","risk":"High","distance":12.9,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.71318,"lng":36.42152,"contact_name":"Thomas (Sister)","contact_phone":"+254 749 888 698","dropout_score":0.9,"access_score":0.22,"nearest_facility":"Naivasha District Hospital","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01129","name":"Michael Ochieng","age":48,"gender":"M","sub_county":"Gilgil","condition":"Typhoid","risk":"High","distance":20.3,"insurance":"None","last_visit":"2026-03-22","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.49388,"lng":36.36254,"contact_name":"Agnes (Daughter)","contact_phone":"+254 762 324 379","dropout_score":0.47,"access_score":0.22,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01130","name":"Gladys Mutua","age":64,"gender":"F","sub_county":"Bahati","condition":"Hypertension","risk":"High","distance":26.5,"insurance":"NHIF","last_visit":"2026-04-10","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.15954,"lng":36.26011,"contact_name":"Lydia (Daughter)","contact_phone":"+254 784 127 185","dropout_score":0.65,"access_score":0.31,"nearest_facility":"Bahati Health Centre","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Requires follow-up."},{"id":"HH-NK-01131","name":"Philip Korir","age":34,"gender":"M","sub_county":"Njoro","condition":"Diabetes T2","risk":"Medium","distance":12.8,"insurance":"NHIF","last_visit":"2026-03-22","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.37548,"lng":36.09219,"contact_name":"David (Uncle)","contact_phone":"+254 710 581 119","dropout_score":0.74,"access_score":0.24,"nearest_facility":"Njoro Health Centre","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01132","name":"Eunice Kerubo","age":59,"gender":"F","sub_county":"Nakuru Town","condition":"Maternal Care","risk":"High","distance":52.7,"insurance":"NHIF","last_visit":"2026-01-15","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.21106,"lng":36.0199,"contact_name":"John (Spouse)","contact_phone":"+254 719 344 229","dropout_score":0.5,"access_score":0.29,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01133","name":"George Kimani","age":62,"gender":"M","sub_county":"Rongai","condition":"TB Follow-up","risk":"High","distance":21.2,"insurance":"None","last_visit":"2026-02-03","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.15055,"lng":35.8062,"contact_name":"Wanjiru (Brother)","contact_phone":"+254 774 126 419","dropout_score":0.59,"access_score":0.91,"nearest_facility":"Rongai Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01134","name":"Christine Mugo","age":22,"gender":"F","sub_county":"Subukia","condition":"HIV Care","risk":"Medium","distance":45.9,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":0.10605,"lng":36.23107,"contact_name":"Lydia (Mother)","contact_phone":"+254 705 455 645","dropout_score":0.46,"access_score":0.49,"nearest_facility":"Subukia Health Centre","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01135","name":"Nicholas Weru","age":18,"gender":"M","sub_county":"Molo","condition":"Malaria","risk":"Low","distance":45.5,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.23331,"lng":35.78759,"contact_name":"Thomas (Father)","contact_phone":"+254 722 851 634","dropout_score":0.92,"access_score":0.41,"nearest_facility":"Molo District Hospital","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01136","name":"Doris Anyango","age":47,"gender":"F","sub_county":"Naivasha","condition":"Asthma","risk":"Medium","distance":40.6,"insurance":"NHIF","last_visit":"2026-03-01","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.66708,"lng":36.36887,"contact_name":"Agnes (Neighbour)","contact_phone":"+254 796 575 683","dropout_score":0.62,"access_score":0.5,"nearest_facility":"Naivasha District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01137","name":"Anthony Mbugua","age":29,"gender":"M","sub_county":"Gilgil","condition":"Mental Health","risk":"Medium","distance":20.5,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.43915,"lng":36.35719,"contact_name":"Paul (Brother)","contact_phone":"+254 701 629 295","dropout_score":0.17,"access_score":0.76,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01138","name":"Lucy Kamau","age":62,"gender":"F","sub_county":"Bahati","condition":"Renal Disease","risk":"Medium","distance":39.6,"insurance":"NHIF","last_visit":"2026-01-15","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.23011,"lng":36.15046,"contact_name":"Ruth (Sister)","contact_phone":"+254 784 695 477","dropout_score":0.5,"access_score":0.61,"nearest_facility":"Bahati Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01139","name":"Daniel Mwangi","age":40,"gender":"M","sub_county":"Njoro","condition":"Cancer Screening","risk":"Low","distance":16.0,"insurance":"NHIF","last_visit":"2026-02-03","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.30459,"lng":35.99049,"contact_name":"Mary (Son)","contact_phone":"+254 724 321 856","dropout_score":0.51,"access_score":0.77,"nearest_facility":"Njoro Health Centre","visit_type":"Resolved","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01140","name":"Mary Wanjiku","age":24,"gender":"F","sub_county":"Nakuru Town","condition":"Post-surgery","risk":"Low","distance":17.3,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.36074,"lng":36.07346,"contact_name":"Grace (Brother)","contact_phone":"+254 706 666 399","dropout_score":0.69,"access_score":0.3,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01141","name":"John Kamau","age":24,"gender":"M","sub_county":"Rongai","condition":"Malnutrition","risk":"Low","distance":32.2,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.22049,"lng":35.93448,"contact_name":"Moses (Brother)","contact_phone":"+254 714 941 166","dropout_score":0.44,"access_score":0.26,"nearest_facility":"Rongai Health Centre","visit_type":"Urgent","notes":"Patient enrolled Jan 2026. Stable condition."},{"id":"HH-NK-01142","name":"Grace Achieng","age":27,"gender":"F","sub_county":"Subukia","condition":"Arthritis","risk":"High","distance":31.6,"insurance":"NHIF","last_visit":"2026-03-01","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.01105,"lng":36.25731,"contact_name":"John (Daughter)","contact_phone":"+254 779 331 894","dropout_score":0.54,"access_score":0.55,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01143","name":"Peter Mwangi","age":37,"gender":"M","sub_county":"Molo","condition":"Epilepsy","risk":"Medium","distance":4.7,"insurance":"Partial","last_visit":"2026-02-03","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.18339,"lng":35.68825,"contact_name":"David (Sister)","contact_phone":"+254 784 183 260","dropout_score":0.3,"access_score":0.63,"nearest_facility":"Molo District Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01144","name":"Fatuma Hassan","age":46,"gender":"F","sub_county":"Naivasha","condition":"Typhoid","risk":"Medium","distance":26.6,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.68689,"lng":36.46748,"contact_name":"Peter (Neighbour)","contact_phone":"+254 787 339 370","dropout_score":0.77,"access_score":0.69,"nearest_facility":"Naivasha District Hospital","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01145","name":"James Omondi","age":45,"gender":"M","sub_county":"Gilgil","condition":"Hypertension","risk":"High","distance":13.5,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.44774,"lng":36.25643,"contact_name":"Ruth (Father)","contact_phone":"+254 776 866 944","dropout_score":0.58,"access_score":0.43,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Requires follow-up."},{"id":"HH-NK-01146","name":"Aisha Karimi","age":62,"gender":"F","sub_county":"Bahati","condition":"Diabetes T2","risk":"Medium","distance":16.1,"insurance":"None","last_visit":"2026-04-01","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.23213,"lng":36.12138,"contact_name":"Joyce (Uncle)","contact_phone":"+254 777 356 126","dropout_score":0.18,"access_score":0.95,"nearest_facility":"Bahati Health Centre","visit_type":"Resolved","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01147","name":"Alex Maina","age":66,"gender":"M","sub_county":"Njoro","condition":"Maternal Care","risk":"Medium","distance":15.9,"insurance":"NHIF","last_visit":"2026-02-20","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.34472,"lng":36.04424,"contact_name":"Mary (Brother)","contact_phone":"+254 774 546 750","dropout_score":0.79,"access_score":0.96,"nearest_facility":"Njoro Health Centre","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01148","name":"Purity Njeri","age":39,"gender":"F","sub_county":"Nakuru Town","condition":"TB Follow-up","risk":"Medium","distance":7.1,"insurance":"NHIF","last_visit":"2026-03-22","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.25201,"lng":36.03411,"contact_name":"Paul (Uncle)","contact_phone":"+254 704 565 190","dropout_score":0.37,"access_score":0.45,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01149","name":"Samuel Koech","age":50,"gender":"M","sub_county":"Rongai","condition":"HIV Care","risk":"Low","distance":1.6,"insurance":"Partial","last_visit":"2026-04-01","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.20888,"lng":35.81001,"contact_name":"John (Aunt)","contact_phone":"+254 796 610 740","dropout_score":0.48,"access_score":0.24,"nearest_facility":"Rongai Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01150","name":"Jane Muthoni","age":36,"gender":"F","sub_county":"Subukia","condition":"Malaria","risk":"Medium","distance":38.9,"insurance":"NHIF","last_visit":"NaN","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":0.06742,"lng":36.17329,"contact_name":"Ruth (Father)","contact_phone":"+254 770 114 665","dropout_score":0.45,"access_score":0.38,"nearest_facility":"Subukia Health Centre","visit_type":"Resolved","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01151","name":"Francis Kariuki","age":47,"gender":"M","sub_county":"Molo","condition":"Asthma","risk":"Low","distance":36.2,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.25358,"lng":35.69875,"contact_name":"Moses (Neighbour)","contact_phone":"+254 731 567 664","dropout_score":0.22,"access_score":0.35,"nearest_facility":"Molo District Hospital","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01152","name":"Sarah Odhiambo","age":22,"gender":"F","sub_county":"Naivasha","condition":"Mental Health","risk":"High","distance":43.8,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.75725,"lng":36.35541,"contact_name":"Lydia (Brother)","contact_phone":"+254 774 775 601","dropout_score":0.84,"access_score":0.55,"nearest_facility":"Naivasha District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Requires follow-up."},{"id":"HH-NK-01153","name":"David Otieno","age":53,"gender":"M","sub_county":"Gilgil","condition":"Renal Disease","risk":"Low","distance":21.7,"insurance":"Partial","last_visit":"2026-03-01","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.42308,"lng":36.28321,"contact_name":"Agnes (Uncle)","contact_phone":"+254 799 520 144","dropout_score":0.37,"access_score":0.57,"nearest_facility":"Gilgil District Hospital","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01154","name":"Agnes Kimotho","age":42,"gender":"F","sub_county":"Bahati","condition":"Cancer Screening","risk":"Low","distance":43.9,"insurance":"None","last_visit":"2026-02-20","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.16575,"lng":36.12092,"contact_name":"Lydia (Son)","contact_phone":"+254 742 990 202","dropout_score":0.84,"access_score":0.54,"nearest_facility":"Bahati Health Centre","visit_type":"Urgent","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01155","name":"Robert Mugo","age":18,"gender":"M","sub_county":"Njoro","condition":"Post-surgery","risk":"Low","distance":23.4,"insurance":"None","last_visit":"2026-02-20","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.40803,"lng":36.06504,"contact_name":"Joyce (Brother)","contact_phone":"+254 779 809 507","dropout_score":0.65,"access_score":0.86,"nearest_facility":"Njoro Health Centre","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01156","name":"Winnie Otieno","age":38,"gender":"F","sub_county":"Nakuru Town","condition":"Malnutrition","risk":"Medium","distance":49.0,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.35726,"lng":35.99895,"contact_name":"Agnes (Brother)","contact_phone":"+254 795 192 544","dropout_score":0.93,"access_score":0.79,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01157","name":"Joseph Kipchoge","age":46,"gender":"M","sub_county":"Rongai","condition":"Arthritis","risk":"High","distance":17.5,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.14762,"lng":35.82694,"contact_name":"Thomas (Aunt)","contact_phone":"+254 718 350 643","dropout_score":0.45,"access_score":0.73,"nearest_facility":"Rongai Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01158","name":"Esther Njoki","age":23,"gender":"F","sub_county":"Subukia","condition":"Epilepsy","risk":"Medium","distance":22.0,"insurance":"None","last_visit":"2026-04-01","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":0.11605,"lng":36.1579,"contact_name":"David (Neighbour)","contact_phone":"+254 758 361 782","dropout_score":0.11,"access_score":0.83,"nearest_facility":"Subukia Health Centre","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01159","name":"Moses Waweru","age":22,"gender":"M","sub_county":"Molo","condition":"Typhoid","risk":"Medium","distance":20.0,"insurance":"None","last_visit":"NaN","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.18108,"lng":35.76545,"contact_name":"Ruth (Neighbour)","contact_phone":"+254 725 493 973","dropout_score":0.51,"access_score":0.39,"nearest_facility":"Molo District Hospital","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01160","name":"Hawa Ibrahim","age":62,"gender":"F","sub_county":"Naivasha","condition":"Hypertension","risk":"High","distance":53.8,"insurance":"None","last_visit":"2026-03-12","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.7987,"lng":36.49341,"contact_name":"John (Spouse)","contact_phone":"+254 795 608 952","dropout_score":0.87,"access_score":0.42,"nearest_facility":"Naivasha District Hospital","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Requires follow-up."},{"id":"HH-NK-01161","name":"Henry Njenga","age":32,"gender":"M","sub_county":"Gilgil","condition":"Diabetes T2","risk":"Medium","distance":34.7,"insurance":"None","last_visit":"NaN","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.47106,"lng":36.26688,"contact_name":"Grace (Mother)","contact_phone":"+254 739 907 551","dropout_score":0.13,"access_score":0.48,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01162","name":"Miriam Chepkemoi","age":38,"gender":"F","sub_county":"Bahati","condition":"Maternal Care","risk":"Low","distance":10.9,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.10477,"lng":36.17354,"contact_name":"David (Son)","contact_phone":"+254 721 363 944","dropout_score":0.9,"access_score":0.95,"nearest_facility":"Bahati Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01163","name":"Charles Mutua","age":69,"gender":"M","sub_county":"Njoro","condition":"TB Follow-up","risk":"High","distance":53.0,"insurance":"NHIF","last_visit":"2026-03-01","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.28238,"lng":36.05587,"contact_name":"Paul (Uncle)","contact_phone":"+254 746 192 909","dropout_score":0.44,"access_score":0.41,"nearest_facility":"Njoro Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Requires follow-up."},{"id":"HH-NK-01164","name":"Joyce Mwangi","age":61,"gender":"F","sub_county":"Nakuru Town","condition":"HIV Care","risk":"Low","distance":15.5,"insurance":"NHIF","last_visit":"NaN","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.21255,"lng":36.00534,"contact_name":"Moses (Sister)","contact_phone":"+254 703 734 674","dropout_score":0.38,"access_score":0.68,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01165","name":"Patrick Njoroge","age":62,"gender":"M","sub_county":"Rongai","condition":"Malaria","risk":"Medium","distance":23.3,"insurance":"NHIF","last_visit":"2026-01-15","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.2263,"lng":35.85882,"contact_name":"Agnes (Mother)","contact_phone":"+254 768 238 497","dropout_score":0.49,"access_score":0.72,"nearest_facility":"Rongai Health Centre","visit_type":"Urgent","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01166","name":"Ruth Wambui","age":55,"gender":"F","sub_county":"Subukia","condition":"Asthma","risk":"Low","distance":9.8,"insurance":"NHIF","last_visit":"2026-02-03","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":0.10339,"lng":36.2335,"contact_name":"Grace (Brother)","contact_phone":"+254 788 479 322","dropout_score":0.48,"access_score":0.94,"nearest_facility":"Subukia Health Centre","visit_type":"Resolved","notes":"Patient enrolled Jan 2026. Stable condition."},{"id":"HH-NK-01167","name":"Thomas Onyango","age":61,"gender":"M","sub_county":"Molo","condition":"Mental Health","risk":"Medium","distance":49.7,"insurance":"None","last_visit":"2026-01-15","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.2713,"lng":35.68537,"contact_name":"Ann (Mother)","contact_phone":"+254 711 778 317","dropout_score":0.65,"access_score":0.67,"nearest_facility":"Molo District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01168","name":"Lydia Chebet","age":33,"gender":"F","sub_county":"Naivasha","condition":"Renal Disease","risk":"Low","distance":43.6,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.76685,"lng":36.38955,"contact_name":"Joyce (Sister)","contact_phone":"+254 799 251 907","dropout_score":0.87,"access_score":0.2,"nearest_facility":"Naivasha District Hospital","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01169","name":"Michael Ochieng","age":26,"gender":"M","sub_county":"Gilgil","condition":"Cancer Screening","risk":"Medium","distance":44.2,"insurance":"NHIF","last_visit":"2026-01-15","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.55891,"lng":36.30232,"contact_name":"Lydia (Sister)","contact_phone":"+254 741 116 278","dropout_score":0.33,"access_score":0.3,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01170","name":"Gladys Mutua","age":65,"gender":"F","sub_county":"Bahati","condition":"Post-surgery","risk":"High","distance":25.5,"insurance":"NHIF","last_visit":"2026-04-10","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.22755,"lng":36.19561,"contact_name":"Grace (Daughter)","contact_phone":"+254 793 902 987","dropout_score":0.66,"access_score":0.44,"nearest_facility":"Bahati Health Centre","visit_type":"Urgent","notes":"Patient enrolled Jan 2026. Requires follow-up."},{"id":"HH-NK-01171","name":"Philip Korir","age":21,"gender":"M","sub_county":"Njoro","condition":"Malnutrition","risk":"Low","distance":46.8,"insurance":"NHIF","last_visit":"2026-02-03","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.34156,"lng":36.08555,"contact_name":"Peter (Mother)","contact_phone":"+254 741 722 251","dropout_score":0.16,"access_score":0.41,"nearest_facility":"Njoro Health Centre","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01172","name":"Eunice Kerubo","age":42,"gender":"F","sub_county":"Nakuru Town","condition":"Arthritis","risk":"Low","distance":29.9,"insurance":"NHIF","last_visit":"2026-04-10","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.29417,"lng":36.1149,"contact_name":"Paul (Mother)","contact_phone":"+254 792 986 320","dropout_score":0.47,"access_score":0.89,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01173","name":"George Kimani","age":43,"gender":"M","sub_county":"Rongai","condition":"Epilepsy","risk":"Medium","distance":6.6,"insurance":"NHIF","last_visit":"NaN","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.23422,"lng":35.93257,"contact_name":"Peter (Neighbour)","contact_phone":"+254 711 951 187","dropout_score":0.18,"access_score":0.28,"nearest_facility":"Rongai Health Centre","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01174","name":"Christine Mugo","age":53,"gender":"F","sub_county":"Subukia","condition":"Typhoid","risk":"High","distance":52.7,"insurance":"None","last_visit":"NaN","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.01044,"lng":36.19158,"contact_name":"Grace (Uncle)","contact_phone":"+254 736 714 419","dropout_score":0.4,"access_score":0.65,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01175","name":"Nicholas Weru","age":32,"gender":"M","sub_county":"Molo","condition":"Hypertension","risk":"Low","distance":20.2,"insurance":"None","last_visit":"2026-02-03","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.21298,"lng":35.74686,"contact_name":"Paul (Uncle)","contact_phone":"+254 798 938 736","dropout_score":0.62,"access_score":0.7,"nearest_facility":"Molo District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01176","name":"Doris Anyango","age":19,"gender":"F","sub_county":"Naivasha","condition":"Diabetes T2","risk":"High","distance":39.1,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.74384,"lng":36.38402,"contact_name":"Lydia (Father)","contact_phone":"+254 784 510 171","dropout_score":0.22,"access_score":0.69,"nearest_facility":"Naivasha District Hospital","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01177","name":"Anthony Mbugua","age":42,"gender":"M","sub_county":"Gilgil","condition":"Maternal Care","risk":"Medium","distance":19.7,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.45571,"lng":36.33581,"contact_name":"Grace (Mother)","contact_phone":"+254 719 261 872","dropout_score":0.63,"access_score":0.73,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01178","name":"Lucy Kamau","age":49,"gender":"F","sub_county":"Bahati","condition":"TB Follow-up","risk":"Medium","distance":23.7,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.22679,"lng":36.18379,"contact_name":"Lydia (Brother)","contact_phone":"+254 762 639 783","dropout_score":0.36,"access_score":0.37,"nearest_facility":"Bahati Health Centre","visit_type":"Resolved","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01179","name":"Daniel Mwangi","age":18,"gender":"M","sub_county":"Njoro","condition":"HIV Care","risk":"High","distance":52.1,"insurance":"None","last_visit":"2026-03-12","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.37369,"lng":35.9592,"contact_name":"Thomas (Neighbour)","contact_phone":"+254 722 232 489","dropout_score":0.55,"access_score":0.38,"nearest_facility":"Njoro Health Centre","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Requires follow-up."},{"id":"HH-NK-01180","name":"Mary Wanjiku","age":22,"gender":"F","sub_county":"Nakuru Town","condition":"Malaria","risk":"Medium","distance":41.2,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.21561,"lng":36.12594,"contact_name":"Thomas (Daughter)","contact_phone":"+254 773 514 826","dropout_score":0.64,"access_score":0.43,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01181","name":"John Kamau","age":28,"gender":"M","sub_county":"Rongai","condition":"Asthma","risk":"Low","distance":34.6,"insurance":"None","last_visit":"2026-03-18","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.2609,"lng":35.91512,"contact_name":"Thomas (Sister)","contact_phone":"+254 775 510 636","dropout_score":0.17,"access_score":0.88,"nearest_facility":"Rongai Health Centre","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01182","name":"Grace Achieng","age":39,"gender":"F","sub_county":"Subukia","condition":"Mental Health","risk":"Low","distance":5.6,"insurance":"None","last_visit":"2026-04-05","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":0.05159,"lng":36.27995,"contact_name":"Charles (Aunt)","contact_phone":"+254 793 938 760","dropout_score":0.79,"access_score":0.38,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01183","name":"Peter Mwangi","age":29,"gender":"M","sub_county":"Molo","condition":"Renal Disease","risk":"Medium","distance":42.2,"insurance":"None","last_visit":"2026-02-20","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.18279,"lng":35.75547,"contact_name":"Lydia (Neighbour)","contact_phone":"+254 797 693 559","dropout_score":0.68,"access_score":0.89,"nearest_facility":"Molo District Hospital","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01184","name":"Fatuma Hassan","age":58,"gender":"F","sub_county":"Naivasha","condition":"Cancer Screening","risk":"Medium","distance":25.0,"insurance":"NHIF","last_visit":"NaN","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.75155,"lng":36.39895,"contact_name":"Charles (Spouse)","contact_phone":"+254 764 175 417","dropout_score":0.49,"access_score":0.23,"nearest_facility":"Naivasha District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01185","name":"James Omondi","age":22,"gender":"M","sub_county":"Gilgil","condition":"Post-surgery","risk":"Medium","distance":53.8,"insurance":"NHIF","last_visit":"2026-04-10","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.49887,"lng":36.31903,"contact_name":"Grace (Son)","contact_phone":"+254 757 929 685","dropout_score":0.65,"access_score":0.45,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01186","name":"Aisha Karimi","age":21,"gender":"F","sub_county":"Bahati","condition":"Malnutrition","risk":"Medium","distance":44.9,"insurance":"None","last_visit":"2026-02-03","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.16427,"lng":36.14261,"contact_name":"Ann (Sister)","contact_phone":"+254 756 636 635","dropout_score":0.62,"access_score":0.48,"nearest_facility":"Bahati Health Centre","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01187","name":"Alex Maina","age":44,"gender":"M","sub_county":"Njoro","condition":"Arthritis","risk":"Low","distance":37.8,"insurance":"NHIF","last_visit":"NaN","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.31643,"lng":35.95055,"contact_name":"Paul (Mother)","contact_phone":"+254 786 495 390","dropout_score":0.31,"access_score":0.86,"nearest_facility":"Njoro Health Centre","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01188","name":"Purity Njeri","age":39,"gender":"F","sub_county":"Nakuru Town","condition":"Epilepsy","risk":"High","distance":37.0,"insurance":"Partial","last_visit":"2026-03-12","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.20817,"lng":36.09976,"contact_name":"Samuel (Uncle)","contact_phone":"+254 776 825 186","dropout_score":0.36,"access_score":0.49,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01189","name":"Samuel Koech","age":60,"gender":"M","sub_county":"Rongai","condition":"Typhoid","risk":"Low","distance":52.2,"insurance":"Partial","last_visit":"2026-04-05","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.26005,"lng":35.88727,"contact_name":"Charles (Son)","contact_phone":"+254 702 471 416","dropout_score":0.25,"access_score":0.37,"nearest_facility":"Rongai Health Centre","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01190","name":"Jane Muthoni","age":30,"gender":"F","sub_county":"Subukia","condition":"Hypertension","risk":"High","distance":8.9,"insurance":"NHIF","last_visit":"2026-02-03","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":0.05123,"lng":36.22136,"contact_name":"Grace (Son)","contact_phone":"+254 784 444 997","dropout_score":0.75,"access_score":0.3,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01191","name":"Francis Kariuki","age":29,"gender":"M","sub_county":"Molo","condition":"Diabetes T2","risk":"Low","distance":42.8,"insurance":"None","last_visit":"2026-02-20","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.21961,"lng":35.66199,"contact_name":"Agnes (Aunt)","contact_phone":"+254 756 725 391","dropout_score":0.74,"access_score":0.81,"nearest_facility":"Molo District Hospital","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01192","name":"Sarah Odhiambo","age":37,"gender":"F","sub_county":"Naivasha","condition":"Maternal Care","risk":"Low","distance":43.5,"insurance":"Partial","last_visit":"2026-03-01","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.74115,"lng":36.50654,"contact_name":"Ann (Neighbour)","contact_phone":"+254 798 388 896","dropout_score":0.42,"access_score":0.61,"nearest_facility":"Naivasha District Hospital","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Stable condition."},{"id":"HH-NK-01193","name":"David Otieno","age":69,"gender":"M","sub_county":"Gilgil","condition":"TB Follow-up","risk":"Medium","distance":48.2,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.44014,"lng":36.33373,"contact_name":"Jane (Mother)","contact_phone":"+254 715 391 185","dropout_score":0.75,"access_score":0.41,"nearest_facility":"Gilgil District Hospital","visit_type":"Resolved","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01194","name":"Agnes Kimotho","age":71,"gender":"F","sub_county":"Bahati","condition":"HIV Care","risk":"Medium","distance":52.1,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.10346,"lng":36.26388,"contact_name":"Grace (Uncle)","contact_phone":"+254 750 614 482","dropout_score":0.3,"access_score":0.98,"nearest_facility":"Bahati Health Centre","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01195","name":"Robert Mugo","age":38,"gender":"M","sub_county":"Njoro","condition":"Malaria","risk":"Low","distance":46.4,"insurance":"None","last_visit":"2026-02-20","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.39798,"lng":35.9859,"contact_name":"Samuel (Neighbour)","contact_phone":"+254 797 822 580","dropout_score":0.48,"access_score":0.2,"nearest_facility":"Njoro Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01196","name":"Winnie Otieno","age":31,"gender":"F","sub_county":"Nakuru Town","condition":"Asthma","risk":"Low","distance":30.9,"insurance":"None","last_visit":"2026-04-05","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.29528,"lng":36.11219,"contact_name":"Ruth (Sister)","contact_phone":"+254 715 148 344","dropout_score":0.46,"access_score":0.82,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Stable condition."},{"id":"HH-NK-01197","name":"Joseph Kipchoge","age":71,"gender":"M","sub_county":"Rongai","condition":"Mental Health","risk":"Low","distance":33.4,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.18299,"lng":35.89497,"contact_name":"Thomas (Brother)","contact_phone":"+254 700 729 461","dropout_score":0.3,"access_score":0.52,"nearest_facility":"Rongai Health Centre","visit_type":"Urgent","notes":"Patient enrolled Jan 2026. Stable condition."},{"id":"HH-NK-01198","name":"Esther Njoki","age":51,"gender":"F","sub_county":"Subukia","condition":"Renal Disease","risk":"Low","distance":5.1,"insurance":"None","last_visit":"2026-04-05","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":0.09583,"lng":36.21622,"contact_name":"Esther (Spouse)","contact_phone":"+254 760 144 750","dropout_score":0.43,"access_score":0.49,"nearest_facility":"Subukia Health Centre","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01199","name":"Moses Waweru","age":68,"gender":"M","sub_county":"Molo","condition":"Cancer Screening","risk":"High","distance":14.4,"insurance":"None","last_visit":"2026-02-03","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.21156,"lng":35.77263,"contact_name":"Samuel (Aunt)","contact_phone":"+254 705 460 659","dropout_score":0.39,"access_score":0.7,"nearest_facility":"Molo District Hospital","visit_type":"Resolved","notes":"Patient enrolled Apr 2026. Requires follow-up."},{"id":"HH-NK-01200","name":"Hawa Ibrahim","age":62,"gender":"F","sub_county":"Naivasha","condition":"Post-surgery","risk":"Medium","distance":11.3,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.79408,"lng":36.38725,"contact_name":"Grace (Sister)","contact_phone":"+254 740 417 627","dropout_score":0.44,"access_score":0.84,"nearest_facility":"Naivasha District Hospital","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01201","name":"Henry Njenga","age":66,"gender":"M","sub_county":"Gilgil","condition":"Malnutrition","risk":"Medium","distance":16.8,"insurance":"Partial","last_visit":"2026-01-15","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.44147,"lng":36.29811,"contact_name":"Charles (Mother)","contact_phone":"+254 755 509 861","dropout_score":0.47,"access_score":0.95,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01202","name":"Miriam Chepkemoi","age":49,"gender":"F","sub_county":"Bahati","condition":"Arthritis","risk":"Medium","distance":21.2,"insurance":"None","last_visit":"2026-03-12","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.11682,"lng":36.23133,"contact_name":"Thomas (Mother)","contact_phone":"+254 777 942 284","dropout_score":0.56,"access_score":0.45,"nearest_facility":"Bahati Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01203","name":"Charles Mutua","age":37,"gender":"M","sub_county":"Njoro","condition":"Epilepsy","risk":"Medium","distance":39.9,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.36375,"lng":35.94678,"contact_name":"John (Aunt)","contact_phone":"+254 755 381 754","dropout_score":0.93,"access_score":0.94,"nearest_facility":"Njoro Health Centre","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01204","name":"Joyce Mwangi","age":41,"gender":"F","sub_county":"Nakuru Town","condition":"Typhoid","risk":"Medium","distance":41.6,"insurance":"NHIF","last_visit":"2026-01-15","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.34016,"lng":36.08521,"contact_name":"Grace (Neighbour)","contact_phone":"+254 716 168 341","dropout_score":0.76,"access_score":0.49,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01205","name":"Patrick Njoroge","age":56,"gender":"M","sub_county":"Rongai","condition":"Hypertension","risk":"High","distance":25.6,"insurance":"NHIF","last_visit":"2026-04-01","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.15291,"lng":35.87183,"contact_name":"Charles (Son)","contact_phone":"+254 750 421 765","dropout_score":0.34,"access_score":0.95,"nearest_facility":"Rongai Health Centre","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Requires follow-up."},{"id":"HH-NK-01206","name":"Ruth Wambui","age":49,"gender":"F","sub_county":"Subukia","condition":"Diabetes T2","risk":"Medium","distance":50.4,"insurance":"NHIF","last_visit":"2026-03-12","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":0.08265,"lng":36.16933,"contact_name":"Ruth (Daughter)","contact_phone":"+254 788 602 304","dropout_score":0.2,"access_score":0.87,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01207","name":"Thomas Onyango","age":23,"gender":"M","sub_county":"Molo","condition":"Maternal Care","risk":"Low","distance":53.3,"insurance":"Partial","last_visit":"NaN","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.27941,"lng":35.66539,"contact_name":"Ruth (Son)","contact_phone":"+254 738 971 261","dropout_score":0.71,"access_score":0.92,"nearest_facility":"Molo District Hospital","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01208","name":"Lydia Chebet","age":50,"gender":"F","sub_county":"Naivasha","condition":"TB Follow-up","risk":"High","distance":54.2,"insurance":"None","last_visit":"2026-03-01","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.67354,"lng":36.35921,"contact_name":"Lydia (Son)","contact_phone":"+254 747 578 922","dropout_score":0.94,"access_score":0.3,"nearest_facility":"Naivasha District Hospital","visit_type":"Resolved","notes":"Patient enrolled Jan 2026. Requires follow-up."},{"id":"HH-NK-01209","name":"Michael Ochieng","age":37,"gender":"M","sub_county":"Gilgil","condition":"HIV Care","risk":"Medium","distance":39.9,"insurance":"NHIF","last_visit":"2026-03-22","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.45693,"lng":36.37673,"contact_name":"Samuel (Mother)","contact_phone":"+254 740 757 175","dropout_score":0.48,"access_score":0.73,"nearest_facility":"Gilgil District Hospital","visit_type":"Regular","notes":"Patient enrolled Feb 2026. Monitoring in progress."},{"id":"HH-NK-01210","name":"Gladys Mutua","age":67,"gender":"F","sub_county":"Bahati","condition":"Malaria","risk":"Low","distance":24.6,"insurance":"Partial","last_visit":"2026-01-15","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.11198,"lng":36.1979,"contact_name":"Mary (Brother)","contact_phone":"+254 720 430 826","dropout_score":0.29,"access_score":0.94,"nearest_facility":"Bahati Health Centre","visit_type":"Urgent","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01211","name":"Philip Korir","age":72,"gender":"M","sub_county":"Njoro","condition":"Asthma","risk":"High","distance":12.0,"insurance":"Partial","last_visit":"2026-03-12","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.39997,"lng":35.98845,"contact_name":"Peter (Son)","contact_phone":"+254 764 756 272","dropout_score":0.6,"access_score":0.65,"nearest_facility":"Njoro Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Requires follow-up."},{"id":"HH-NK-01212","name":"Eunice Kerubo","age":71,"gender":"F","sub_county":"Nakuru Town","condition":"Mental Health","risk":"Low","distance":3.7,"insurance":"Partial","last_visit":"2026-02-03","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.35573,"lng":36.09063,"contact_name":"David (Daughter)","contact_phone":"+254 783 315 885","dropout_score":0.59,"access_score":0.68,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01213","name":"George Kimani","age":59,"gender":"M","sub_county":"Rongai","condition":"Renal Disease","risk":"Low","distance":27.3,"insurance":"None","last_visit":"NaN","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.21003,"lng":35.85257,"contact_name":"Mary (Spouse)","contact_phone":"+254 756 525 595","dropout_score":0.49,"access_score":0.47,"nearest_facility":"Rongai Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01214","name":"Christine Mugo","age":64,"gender":"F","sub_county":"Subukia","condition":"Cancer Screening","risk":"Low","distance":20.0,"insurance":"NHIF","last_visit":"2026-03-18","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":0.0524,"lng":36.15199,"contact_name":"Ann (Sister)","contact_phone":"+254 715 373 560","dropout_score":0.31,"access_score":0.28,"nearest_facility":"Subukia Health Centre","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Stable condition."},{"id":"HH-NK-01215","name":"Nicholas Weru","age":57,"gender":"M","sub_county":"Molo","condition":"Post-surgery","risk":"Medium","distance":53.0,"insurance":"Partial","last_visit":"2026-03-18","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.1856,"lng":35.77038,"contact_name":"Mary (Sister)","contact_phone":"+254 763 627 578","dropout_score":0.52,"access_score":0.44,"nearest_facility":"Molo District Hospital","visit_type":"Regular","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01216","name":"Doris Anyango","age":50,"gender":"F","sub_county":"Naivasha","condition":"Malnutrition","risk":"Medium","distance":14.4,"insurance":"None","last_visit":"2026-01-15","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.79191,"lng":36.43418,"contact_name":"Ruth (Neighbour)","contact_phone":"+254 768 108 967","dropout_score":0.19,"access_score":0.3,"nearest_facility":"Naivasha District Hospital","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Monitoring in progress."},{"id":"HH-NK-01217","name":"Anthony Mbugua","age":66,"gender":"M","sub_county":"Gilgil","condition":"Arthritis","risk":"Medium","distance":3.9,"insurance":"NHIF","last_visit":"2026-04-05","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.54886,"lng":36.33352,"contact_name":"Esther (Mother)","contact_phone":"+254 764 561 882","dropout_score":0.57,"access_score":0.84,"nearest_facility":"Gilgil District Hospital","visit_type":"Urgent","notes":"Patient enrolled Jan 2026. Monitoring in progress."},{"id":"HH-NK-01218","name":"Lucy Kamau","age":26,"gender":"F","sub_county":"Bahati","condition":"Epilepsy","risk":"Low","distance":22.6,"insurance":"None","last_visit":"2026-03-18","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.15575,"lng":36.1735,"contact_name":"Francis (Father)","contact_phone":"+254 777 621 511","dropout_score":0.53,"access_score":0.24,"nearest_facility":"Bahati Health Centre","visit_type":"Regular","notes":"Patient enrolled Mar 2026. Stable condition."},{"id":"HH-NK-01219","name":"Daniel Mwangi","age":69,"gender":"M","sub_county":"Njoro","condition":"Typhoid","risk":"Medium","distance":25.9,"insurance":"None","last_visit":"2026-04-05","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.39764,"lng":36.08902,"contact_name":"Mary (Aunt)","contact_phone":"+254 750 731 857","dropout_score":0.82,"access_score":0.66,"nearest_facility":"Njoro Health Centre","visit_type":"Urgent","notes":"Patient enrolled Apr 2026. Monitoring in progress."},{"id":"HH-NK-01220","name":"Doris Chebet","age":43,"gender":"F","sub_county":"Nakuru Town","condition":"Hypertension","risk":"Medium","distance":11.6,"insurance":"NHIF","last_visit":"2026-03-15","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.31537,"lng":36.02399,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 721 357 846","dropout_score":0.43,"access_score":0.73,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Resolved","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01221","name":"Oscar Kimani","age":23,"gender":"M","sub_county":"Rongai","condition":"Diabetes T2","risk":"Low","distance":25.5,"insurance":"None","last_visit":"2026-03-15","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.16833,"lng":35.87061,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 757 942 497","dropout_score":0.83,"access_score":0.37,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01222","name":"Anita Mwende","age":60,"gender":"F","sub_county":"Subukia","condition":"Maternal Care","risk":"High","distance":42.8,"insurance":"None","last_visit":"2026-03-15","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-4e-05,"lng":36.241,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 796 893 189","dropout_score":0.5,"access_score":0.51,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01223","name":"Benson Karuri","age":53,"gender":"M","sub_county":"Molo","condition":"TB Follow-up","risk":"High","distance":22.4,"insurance":"None","last_visit":"2026-03-15","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.19625,"lng":35.73912,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 769 631 302","dropout_score":0.61,"access_score":0.96,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01224","name":"Beatrice Otieno","age":26,"gender":"F","sub_county":"Naivasha","condition":"HIV Care","risk":"High","distance":47.7,"insurance":"Partial","last_visit":"2026-03-15","sw_id":"SW-NK-05","sw_name":"Rose Kimani","sw_phone":"+254 745 678 901","lat":-0.7607,"lng":36.47002,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 786 281 615","dropout_score":0.66,"access_score":0.23,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01225","name":"Calvin Odhiambo","age":28,"gender":"M","sub_county":"Gilgil","condition":"Malaria","risk":"Medium","distance":34.8,"insurance":"None","last_visit":"2026-03-15","sw_id":"SW-NK-06","sw_name":"Joyce Mutua","sw_phone":"+254 756 789 012","lat":-0.55026,"lng":36.31605,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 721 246 417","dropout_score":0.62,"access_score":0.5,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01226","name":"Celine Njoki","age":51,"gender":"F","sub_county":"Bahati","condition":"Asthma","risk":"Medium","distance":11.6,"insurance":"NHIF","last_visit":"2026-03-15","sw_id":"SW-NK-01","sw_name":"Amara Ochieng","sw_phone":"+254 701 234 567","lat":-0.14815,"lng":36.18816,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 779 513 944","dropout_score":0.75,"access_score":0.48,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Resolved","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01227","name":"Dennis Koech","age":48,"gender":"M","sub_county":"Njoro","condition":"Mental Health","risk":"High","distance":8.3,"insurance":"Partial","last_visit":"2026-03-15","sw_id":"SW-NK-02","sw_name":"James Kipkemboi","sw_phone":"+254 712 345 678","lat":-0.32804,"lng":36.04967,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 787 518 227","dropout_score":0.18,"access_score":0.31,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Regular","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01228","name":"Diana Kamau","age":29,"gender":"F","sub_county":"Nakuru Town","condition":"Hypertension","risk":"Medium","distance":9.0,"insurance":"NHIF","last_visit":"2026-03-15","sw_id":"SW-NK-03","sw_name":"Faith Wanjiku","sw_phone":"+254 723 456 789","lat":-0.23735,"lng":36.04629,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 773 917 339","dropout_score":0.82,"access_score":0.29,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled 2026. Under monitoring."},{"id":"HH-NK-01229","name":"Edwin Mwangi","age":29,"gender":"M","sub_county":"Rongai","condition":"Diabetes T2","risk":"Low","distance":5.5,"insurance":"None","last_visit":"2026-03-15","sw_id":"SW-NK-04","sw_name":"David Muriithi","sw_phone":"+254 734 567 890","lat":-0.25366,"lng":35.89991,"contact_name":"Family Member (Next of Kin)","contact_phone":"+254 753 321 486","dropout_score":0.44,"access_score":0.84,"nearest_facility":"Nakuru Level 5 Hospital","visit_type":"Urgent","notes":"Patient enrolled 2026. Under monitoring."}];
const FACILITIES = [{"name":"AAR Nakuru Clinic","type":"Dispensary","sub_county":"Nakuru","lat":-0.23285,"lng":36.04388,"speciality":"Dispensary"},{"name":"Advent Med & Dentist Care Centre","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28631,"lng":36.06565,"speciality":"Medical Clinic"},{"name":"Afraha Maternity and Nursing Home","type":"Nursing Home","sub_county":"Nakuru","lat":-0.29746,"lng":36.07421,"speciality":"Nursing Home"},{"name":"Afya Bora Medical Clinic","type":"Medical Clinic","sub_county":"Njoro","lat":-0.34365,"lng":36.05765,"speciality":"Medical Clinic"},{"name":"Afya Medical Clinic (Gilgil)","type":"Medical Clinic","sub_county":"Gilgil","lat":-0.49987,"lng":36.32373,"speciality":"Medical Clinic"},{"name":"Afya Medical Clinic (Mbaruk)","type":"Medical Clinic","sub_county":"Gilgil","lat":-0.35429,"lng":36.21398,"speciality":"Medical Clinic"},{"name":"Afya Medical Clinic (Nakuru)","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.29448,"lng":36.09211,"speciality":"Medical Clinic"},{"name":"Afya Njema Medical Clinic","type":"Medical Clinic","sub_county":"Rongai","lat":-0.20643,"lng":35.84816,"speciality":"Medical Clinic"},{"name":"Aga Khan University Hospital Clinic (Naivasha)","type":"Medical Clinic","sub_county":"Naivasha","lat":-0.71459,"lng":36.43354,"speciality":"Medical Clinic"},{"name":"Agakhan Medical Centre","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28651,"lng":36.06348,"speciality":"Medical Clinic"},{"name":"Agc Baby Health Centre","type":"Health Centre","sub_county":"Rongai","lat":-0.25955,"lng":35.9785,"speciality":"Health Centre"},{"name":"AIC Parkview Dispensary","type":"Dispensary","sub_county":"Nakuru","lat":-0.31257,"lng":36.05826,"speciality":"Dispensary"},{"name":"Ainamoi Dispensary","type":"Dispensary","sub_county":"Kuresoi","lat":-0.55684,"lng":35.60215,"speciality":"Dispensary"},{"name":"Algadir Medical Clinic","type":"Dispensary","sub_county":"Nakuru","lat":-0.29912,"lng":36.06766,"speciality":"Dispensary"},{"name":"AMEC Laboratories","type":"Laboratory (Stand-alone)","sub_county":"Nakuru","lat":-0.28489,"lng":36.071,"speciality":"Laboratory (Stand-alone)"},{"name":"Annex Hospital (Nakuru)","type":"Other Hospital","sub_county":"Nakuru","lat":-0.16938,"lng":36.04868,"speciality":"Other Hospital"},{"name":"Aphiaplus Drop-In Centre (Naivasha)","type":"Medical Clinic","sub_county":"Naivasha","lat":-0.71238,"lng":36.42947,"speciality":"Medical Clinic"},{"name":"Aquilla Farm Medical Clinic","type":"Medical Clinic","sub_county":"Naivasha","lat":-0.74543,"lng":36.25053,"speciality":"Medical Clinic"},{"name":"Arimi Dispensary","type":"Dispensary","sub_county":"Molo","lat":-0.28251,"lng":35.85133,"speciality":"Dispensary"},{"name":"ASN Upendo Village Dispensary","type":"Dispensary","sub_county":"Naivasha","lat":-0.75748,"lng":36.47571,"speciality":"Dispensary"},{"name":"Avenue Health Care Nakuru","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28633,"lng":36.06528,"speciality":"Medical Clinic"},{"name":"B & L Healthcare(Naivasha)","type":"Medical Centre","sub_county":"Naivasha","lat":-0.71456,"lng":36.4335,"speciality":"Medical Centre"},{"name":"Bagaria Dispensary","type":"Dispensary","sub_county":"Njoro","lat":-0.48542,"lng":36.03998,"speciality":"Dispensary"},{"name":"Bahati Dispensary","type":"Dispensary","sub_county":"Nakuru North","lat":-0.15402,"lng":36.15361,"speciality":"Dispensary"},{"name":"Bahati District Hospital","type":"District Hospital","sub_county":"Nakuru North","lat":-0.17031,"lng":36.12368,"speciality":"District Hospital"},{"name":"Bangii Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.27787,"lng":36.00408,"speciality":"Medical Clinic"},{"name":"Banita Dispensary","type":"Dispensary","sub_county":"Rongai","lat":-0.07525,"lng":36.07665,"speciality":"Dispensary"},{"name":"Baraka Maternity Home","type":"Maternity Home","sub_county":"Nakuru","lat":-0.28909,"lng":36.07628,"speciality":"Maternity Home"},{"name":"Bararget Dispensary","type":"Dispensary","sub_county":"Kuresoi","lat":-0.41505,"lng":35.73243,"speciality":"Dispensary"},{"name":"Bargain Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.2795,"lng":36.12783,"speciality":"Medical Clinic"},{"name":"Barut Dispensary","type":"Dispensary","sub_county":"Nakuru","lat":-0.19625,"lng":36.03383,"speciality":"Dispensary"},{"name":"Barut Medical clinic","type":"Dispensary","sub_county":"Nakuru","lat":0.19625,"lng":36.03383,"speciality":"Dispensary"},{"name":"Benmac Clinic","type":"Medical Clinic","sub_county":"Njoro","lat":-0.37458,"lng":35.9445,"speciality":"Medical Clinic"},{"name":"Bethania Clinic","type":"Nursing Home","sub_county":"Gilgil","lat":-0.56696,"lng":36.11691,"speciality":"Nursing Home"},{"name":"Bethania Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru North","lat":0.25742,"lng":36.10862,"speciality":"Medical Clinic"},{"name":"Bethsaida (AIC) Clinic (Nakuru)","type":"Dispensary","sub_county":"Nakuru","lat":-0.17608,"lng":36.03875,"speciality":"Dispensary"},{"name":"Better Health Services","type":"Medical Clinic","sub_county":"Naivasha","lat":-0.82184,"lng":36.20376,"speciality":"Medical Clinic"},{"name":"Bigot Medical Clinic","type":"Medical Clinic","sub_county":"Naivasha","lat":-0.67489,"lng":36.4328,"speciality":"Medical Clinic"},{"name":"Binyo Medical Clinic","type":"Medical Clinic","sub_county":"Subukia","lat":0.140937,"lng":36.2427,"speciality":"Medical Clinic"},{"name":"Blue Cross Medical Clicnic","type":"Medical Clinic","sub_county":"Gilgil","lat":-0.4984,"lng":36.32246,"speciality":"Medical Clinic"},{"name":"Bondeni Dispensary (Nakuru Central)","type":"Dispensary","sub_county":"Nakuru","lat":-0.29061,"lng":36.08127,"speciality":"Dispensary"},{"name":"Bondeni Maternity","type":"Maternity Home","sub_county":"Nakuru","lat":-0.29575,"lng":36.07952,"speciality":"Maternity Home"},{"name":"Calvary Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru North","lat":-0.28505,"lng":36.15003,"speciality":"Medical Clinic"},{"name":"Camp Brethren Medical Clinic","type":"Medical Clinic","sub_county":"Gilgil","lat":-0.563306,"lng":36.2726,"speciality":"Medical Clinic"},{"name":"Canaan (ACK) Medical Clinic","type":"Medical Clinic","sub_county":"Naivasha","lat":-1.00432,"lng":36.5525,"speciality":"Medical Clinic"},{"name":"Cdn VCT","type":"VCT Centre (Stand-Alone)","sub_county":"Nakuru","lat":-0.29113,"lng":36.07229,"speciality":"VCT Centre (Stand-Alone)"},{"name":"Centre medical clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":0.29649,"lng":36.03157,"speciality":"Medical Clinic"},{"name":"Chebaraa Dispensary","type":"Dispensary","sub_county":"Kuresoi","lat":-0.47748,"lng":35.67997,"speciality":"Dispensary"},{"name":"Chemaner Dispensary (Kuresoi)","type":"Dispensary","sub_county":"Kuresoi","lat":-0.43614,"lng":35.60652,"speciality":"Dispensary"},{"name":"Chemasis Maternity Home","type":"Maternity Home","sub_county":"Subukia","lat":0.00135,"lng":36.23152,"speciality":"Maternity Home"},{"name":"Chepakundi Dispensary","type":"Dispensary","sub_county":"Kuresoi","lat":-0.67766,"lng":35.65591,"speciality":"Dispensary"},{"name":"Cheppemma (AIC) Dispensary","type":"Dispensary","sub_county":"Rongai","lat":-0.06215,"lng":35.86396,"speciality":"Dispensary"},{"name":"Cheptuech Dispensary","type":"Dispensary","sub_county":"Kuresoi","lat":-0.59136,"lng":35.64678,"speciality":"Dispensary"},{"name":"Civil Servants Clinic (Nakuru)","type":"Dispensary","sub_county":"Nakuru","lat":-0.17259,"lng":36.04281,"speciality":"Dispensary"},{"name":"Comfort The Chidren International (Ctc) Naivasha","type":"Health Project","sub_county":"Naivasha","lat":-0.97945,"lng":36.58256,"speciality":"Health Project"},{"name":"Consolata Clinic","type":"Dispensary","sub_county":"Njoro","lat":-0.63417,"lng":35.99525,"speciality":"Dispensary"},{"name":"Copeman Health Care Centre","type":"Medical Clinic","sub_county":"Kuresoi","lat":-0.632,"lng":35.6702,"speciality":"Medical Clinic"},{"name":"Coping Centre","type":"VCT Centre (Stand-Alone)","sub_county":"Nakuru","lat":-0.30248,"lng":36.06426,"speciality":"VCT Centre (Stand-Alone)"},{"name":"Crater Medical Centre","type":"Nursing Home","sub_county":"Nakuru","lat":-0.28449,"lng":36.09737,"speciality":"Nursing Home"},{"name":"Delamere Clinic","type":"Medical Clinic","sub_county":"Gilgil","lat":-0.46866,"lng":36.1948,"speciality":"Medical Clinic"},{"name":"Denticheck Clinical Services","type":"Medical Clinic","sub_county":"Gilgil","lat":-0.71185,"lng":36.29532,"speciality":"Medical Clinic"},{"name":"Dentomed Clinic","type":"Medical Clinic","sub_county":"Molo","lat":-0.25003,"lng":35.73365,"speciality":"Medical Clinic"},{"name":"Dr Aluvaala Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28489,"lng":36.07247,"speciality":"Medical Clinic"},{"name":"Dr Arthur (PCEA) Dispensary","type":"Dispensary","sub_county":"Nakuru","lat":-0.29933,"lng":36.07827,"speciality":"Dispensary"},{"name":"Dr B.K.Kariuki","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28453,"lng":36.06665,"speciality":"Medical Clinic"},{"name":"Dr Babu Bora clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28322,"lng":36.07513,"speciality":"Medical Clinic"},{"name":"Dr Kalyas Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28316,"lng":36.07442,"speciality":"Medical Clinic"},{"name":"Dr Karania Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28534,"lng":36.07491,"speciality":"Medical Clinic"},{"name":"Dr Manyara Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.30228,"lng":36.07493,"speciality":"Medical Clinic"},{"name":"Dr Mugo Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.16964,"lng":36.0447,"speciality":"Medical Clinic"},{"name":"Dr Mwangi","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.028353,"lng":36.07529,"speciality":"Medical Clinic"},{"name":"Dr Ngotho Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.16937,"lng":36.04868,"speciality":"Medical Clinic"},{"name":"Dr Ogindo's Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":0.28276,"lng":36.07401,"speciality":"Medical Clinic"},{"name":"Dr Osore's Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28331,"lng":36.07526,"speciality":"Medical Clinic"},{"name":"Dr Shanti Haria","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.2997,"lng":36.07737,"speciality":"Medical Clinic"},{"name":"Dr Walumbe Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.23467,"lng":36.06643,"speciality":"Medical Clinic"},{"name":"Dr Wenyaa Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.28352,"lng":36.07376,"speciality":"Medical Clinic"},{"name":"Dr.Finn consultants","type":"Medical Clinic","sub_county":"Nakuru","lat":0.30629,"lng":36.13843,"speciality":"Medical Clinic"},{"name":"DRIC (Naivasha)","type":"Health Project","sub_county":"Naivasha","lat":-0.71852,"lng":36.43706,"speciality":"Health Project"},{"name":"Dubai Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru North","lat":-0.27528,"lng":36.1702,"speciality":"Medical Clinic"},{"name":"Dundori Health Centre","type":"Health Centre","sub_county":"Nakuru North","lat":-0.25061,"lng":36.23326,"speciality":"Health Centre"},{"name":"Eburru Dispensary","type":"Dispensary","sub_county":"Gilgil","lat":-0.64815,"lng":36.27082,"speciality":"Dispensary"},{"name":"Egerton University","type":"Other Hospital","sub_county":"Njoro","lat":-0.37295,"lng":35.93072,"speciality":"Other Hospital"},{"name":"Elburgon (PCEA) Dispensary","type":"Dispensary","sub_county":"Molo","lat":-0.3059,"lng":35.80974,"speciality":"Dispensary"},{"name":"Elburgon Nursing Home","type":"Nursing Home","sub_county":"Molo","lat":-0.28593,"lng":35.75811,"speciality":"Nursing Home"},{"name":"Elburgon Sub-District Hospital","type":"Sub-District Hospital","sub_county":"Molo","lat":-0.30606,"lng":35.80782,"speciality":"Sub-District Hospital"},{"name":"Elementeita Dispensary","type":"Dispensary","sub_county":"Gilgil","lat":-0.518257,"lng":36.1091,"speciality":"Dispensary"},{"name":"Emitik Dispensary","type":"Dispensary","sub_county":"Kuresoi","lat":-0.62334,"lng":35.60361,"speciality":"Dispensary"},{"name":"Emmaus Clinic","type":"Medical Clinic","sub_county":"Kuresoi","lat":-0.58026,"lng":35.69344,"speciality":"Medical Clinic"},{"name":"Engashura Health Centre","type":"Health Centre","sub_county":"Nakuru North","lat":-0.25958,"lng":36.13405,"speciality":"Health Centre"},{"name":"Esther Memorial Nursing Home","type":"Health Centre","sub_county":"Nakuru North","lat":-0.23076,"lng":36.11773,"speciality":"Health Centre"},{"name":"Euvan Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru North","lat":-0.15042,"lng":36.14682,"speciality":"Medical Clinic"},{"name":"Faith Medical Clinic Karate","type":"Medical Clinic","sub_county":"Naivasha","lat":-0.636028,"lng":36.4108,"speciality":"Medical Clinic"},{"name":"Family Healthoptions Kenya (Nakuru)","type":"Health Centre","sub_county":"Nakuru","lat":-0.28742,"lng":36.07682,"speciality":"Health Centre"},{"name":"Family Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.30209,"lng":36.07761,"speciality":"Medical Clinic"},{"name":"FGC of Kenya Medical Centre","type":"Dispensary","sub_county":"Molo","lat":-0.24807,"lng":35.7349,"speciality":"Dispensary"},{"name":"Finlays Hospital","type":"Other Hospital","sub_county":"Naivasha","lat":-0.67459,"lng":36.43277,"speciality":"Other Hospital"},{"name":"Fitc Dispensary","type":"Dispensary","sub_county":"Nakuru","lat":-0.16941,"lng":36.03225,"speciality":"Dispensary"},{"name":"Florensis Kenya LTD Medical Clinic(Naivasha)","type":"Medical Clinic","sub_county":"Naivasha","lat":-0.82559,"lng":36.37277,"speciality":"Medical Clinic"},{"name":"Florex Medical Clinic","type":"Medical Clinic","sub_county":"Nakuru","lat":-0.33942,"lng":36.14698,"speciality":"Medical Clinic"}];
const WORKERS = [{"id":"SW-NK-01","name":"Amara Ochieng","role":"Social Worker","sub_county":"Nakuru Town","lat":-0.27805,"lng":36.06978,"phone":"+254 701 234 567","email":"amara.ochieng@nakuru.go.ke"},{"id":"SW-NK-02","name":"James Kipkemboi","role":"Social Worker","sub_county":"Rongai","lat":-0.1802,"lng":35.8521,"phone":"+254 712 345 678","email":"james.kipkemboi@nakuru.go.ke"},{"id":"SW-NK-03","name":"Faith Wanjiku","role":"Social Worker","sub_county":"Subukia","lat":0.0412,"lng":36.2215,"phone":"+254 723 456 789","email":"faith.wanjiku@nakuru.go.ke"},{"id":"SW-NK-04","name":"David Muriithi","role":"Social Worker","sub_county":"Molo","lat":-0.2501,"lng":35.7335,"phone":"+254 734 567 890","email":"david.muriithi@nakuru.go.ke"},{"id":"SW-NK-05","name":"Rose Kimani","role":"Social Worker","sub_county":"Naivasha","lat":-0.7145,"lng":36.4335,"phone":"+254 745 678 901","email":"rose.kimani@nakuru.go.ke"},{"id":"SW-NK-06","name":"Joyce Mutua","role":"Social Worker","sub_county":"Gilgil","lat":-0.4987,"lng":36.3225,"phone":"+254 756 789 012","email":"joyce.mutua@nakuru.go.ke"}];
</script>

<!-- TOPBAR -->
<div class="topbar">
  <div class="logo"><div class="logo-dot">🏥</div> HealthLink <span style="color:var(--tm);margin-left:4px">Kenya</span></div>
  <div class="tbar-r">
    <span id="api-pill" class="pill p-api">⬤ API Live</span>
    <span class="pill p-hi" id="kpi-hi-top">— High Risk</span>
    <span style="font-size:12px;color:var(--mu)" id="sw-name-top">Amara Ochieng · SW-NK-01</span>
    <button class="btn btn-g" style="font-size:11px;padding:5px 10px" onclick="doLogout()">Logout</button>
  </div>
</div>

<!-- NAV -->
<div class="nav">
  <button class="nb active" onclick="go('hub',this)">📊 Outreach Hub</button>
  <button class="nb" onclick="go('geo',this)">🗺 Geospatial Mapper</button>
  <button class="nb" onclick="go('triage',this)">🩺 Patient Triage</button>
  <button class="nb" onclick="go('mc',this)">🚑 Mobile Clinic</button>
  <button class="nb" onclick="go('db',this)">📋 Patient Database</button>
  <button class="nb" onclick="go('decay',this)">📉 Distance Decay</button>
  <button class="nb" onclick="go('alerts',this)">🔔 Alerts <span id="alert-badge" class="pill p-hi" style="font-size:10px;padding:1px 5px">3</span></button>
  <button class="nb" onclick="go('settings',this)">⚙️ Settings</button>
</div>

<div class="main">

<!-- ── HUB ─────────────────────────────────────────────────── -->
<div id="hub" class="page active">
  <div class="ph"><div><div class="pt">Social Worker Outreach Hub</div><div class="ps">Nakuru County · Live triage intelligence dashboard</div></div></div>
  <div class="sg" id="hub-kpis"></div>
  <div class="hg">
    <div class="hb" onclick="go('geo',document.querySelectorAll('.nb')[1])"><span class="hi">🗺</span><div class="hl">Geospatial Mapper</div><div class="hd">Risk zones & facilities</div></div>
    <div class="hb" onclick="go('triage',document.querySelectorAll('.nb')[2])"><span class="hi">🩺</span><div class="hl">Patient Triage</div><div class="hd">Risk-ranked profiles</div></div>
    <div class="hb" onclick="go('mc',document.querySelectorAll('.nb')[3])"><span class="hi">🚑</span><div class="hl">Mobile Clinic</div><div class="hd">Route planning</div></div>
    <div class="hb" onclick="go('db',document.querySelectorAll('.nb')[4])"><span class="hi">📋</span><div class="hl">Patient Database</div><div class="hd">Full registry</div></div>
    <div class="hb" onclick="go('decay',document.querySelectorAll('.nb')[5])"><span class="hi">📉</span><div class="hl">Distance Decay</div><div class="hd">GAM analysis</div></div>
    <div class="hb" onclick="go('alerts',document.querySelectorAll('.nb')[6])"><span class="hi">🔔</span><div class="hl">Alerts</div><div class="hd">3 critical flags</div></div>
  </div>
  <div class="row">
    <div style="flex:1">
      <div class="card"><div class="ct">High-Risk Patients — Immediate Action</div>
        <div id="hub-alert-list"></div>
      </div>
    </div>
    <div style="flex:1">
      <div class="card"><div class="ct">Social Worker Coverage</div>
        <div id="sw-coverage-list"></div>
      </div>
    </div>
  </div>
</div>

<!-- ── GEO ─────────────────────────────────────────────────── -->
<div id="geo" class="page">
  <div class="ph"><div><div class="pt">Geospatial Mapper</div><div class="ps">Nakuru County · Facilities, households, risk zones & decay ring</div></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn btn-t" onclick="geoToggle('facilities')" id="btn-fac">🏥 Facilities ON</button>
      <button class="btn btn-t" onclick="geoToggle('households')" id="btn-hh">🏠 Households ON</button>
      <button class="btn btn-n" onclick="geoToggle('decay')" id="btn-decay">⭕ Decay Ring OFF</button>
    </div>
  </div>
  <div class="sg" id="geo-stats"></div>
  <div class="row">
    <div style="flex:1">
      <div class="map-wrap"><div id="geo-map"></div></div>
      <div class="map-leg">
        <span><span class="leg-dot" style="background:#F87171"></span>High risk</span>
        <span><span class="leg-dot" style="background:#FCD34D"></span>Medium risk</span>
        <span><span class="leg-dot" style="background:#6EE7B7"></span>Low risk</span>
        <span><span class="leg-dot" style="background:#7eb8f7"></span>Health facility</span>
        <span><span class="leg-dot" style="background:#c084fc"></span>Dropped pin</span>
      </div>
    </div>
    <div style="flex:0 0 280px;min-width:0">
      <div class="card" style="height:480px;overflow-y:auto">
        <div class="ct">📌 Distance Decay Results — Dropped Pin</div>
        <div style="font-size:11px;color:var(--mu);margin-bottom:10px">Click map to drop pin and find nearest locations</div>
        <div id="geo-decay-results"><div style="color:var(--mu);font-size:12px;text-align:center;padding:20px 0">Click anywhere on the map to begin</div></div>
      </div>
    </div>
  </div>
</div>

<!-- ── TRIAGE ───────────────────────────────────────────────── -->
<div id="triage" class="page">
  <div class="ph"><div><div class="pt">Patient Triage</div><div class="ps">Risk-ranked patient profiles · Click any row for full profile</div></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <select class="fc" id="tr-risk" onchange="renderTriage()"><option value="">All risk</option><option>High</option><option>Medium</option><option>Low</option></select>
      <select class="fc" id="tr-sw" onchange="renderTriage()"><option value="">All SWs</option></select>
      <select class="fc" id="tr-cond" onchange="renderTriage()"><option value="">All conditions</option></select>
      <input class="fi" id="tr-search" placeholder="Search patient..." oninput="renderTriage()" style="min-width:160px">
    </div>
  </div>
  <div class="tw"><table>
    <thead><tr><th>ID</th><th>Name</th><th>Age</th><th>Sub-county</th><th>Condition</th><th>Risk</th><th>Distance</th><th>Insurance</th><th>Dropout Score</th><th>Social Worker</th><th>Last Visit</th></tr></thead>
    <tbody id="triage-body"></tbody>
  </table></div>
  <div id="triage-count" style="font-size:11px;color:var(--mu);margin-top:8px"></div>
</div>

<!-- ── MOBILE CLINIC ────────────────────────────────────────── -->
<div id="mc" class="page">
  <div class="ph"><div><div class="pt">Mobile Clinic Routing</div><div class="ps">Find households · nearest facility auto-match</div></div></div>
  <div class="tb">
    <input class="fi" id="mc-search" placeholder="Search household or patient name..." oninput="renderMC()" style="max-width:260px">
    <select class="fc" id="mc-risk" onchange="renderMC()"><option value="">All risk levels</option><option>High</option><option>Medium</option><option>Low</option></select>
    <select class="fc" id="mc-vtype" onchange="renderMC()"><option value="">All visit types</option><option value="Urgent">Urgent</option><option value="Regular">Regular</option><option value="Resolved">Resolved</option></select>
    <select class="fc" id="mc-ftype" onchange="renderMC()"><option value="">All facility types</option><option>Hospital</option><option>Health Centre</option><option>Dispensary</option><option>Medical Clinic</option><option>Nursing Home</option></select>
  </div>
  <div class="row">
    <div class="col-l">
      <div class="card" style="padding:10px">
        <div class="ct">Households <span id="mc-count" style="font-weight:400;color:var(--mu)"></span></div>
        <div class="hh-list" id="mc-list"></div>
      </div>
    </div>
    <div class="col-r">
      <div class="map-wrap"><div id="mc-map"></div></div>
      <div id="mc-detail" style="margin-top:10px"></div>
    </div>
  </div>
</div>

<!-- ── PATIENT DB ───────────────────────────────────────────── -->
<div id="db" class="page">
  <div class="ph"><div><div class="pt">Patient Database</div><div class="ps">All 130 registered patients · Nakuru County</div></div>
    <button class="btn btn-t" onclick="exportCSV()">⬇ Export CSV</button>
  </div>
  <div class="tb">
    <input class="fi" id="db-search" placeholder="Search name, ID or condition..." oninput="renderDB()" style="max-width:240px">
    <select class="fc" id="db-risk" onchange="renderDB()"><option value="">All risk</option><option>High</option><option>Medium</option><option>Low</option></select>
    <select class="fc" id="db-ins" onchange="renderDB()"><option value="">All insurance</option><option value="NHIF">NHIF</option><option value="None">Uninsured</option><option value="Partial">Partial</option></select>
    <select class="fc" id="db-sc" onchange="renderDB()"><option value="">All sub-counties</option></select>
    <select class="fc" id="db-sw" onchange="renderDB()"><option value="">All social workers</option></select>
  </div>
  <div class="sum-bar" id="db-summary"></div>
  <div class="tw"><table>
    <thead><tr><th>ID</th><th>Name</th><th>Age/Sex</th><th>Sub-county</th><th>Condition</th><th>Risk</th><th>Distance</th><th>Insurance</th><th>Social Worker</th><th>Last Visit</th></tr></thead>
    <tbody id="db-body"></tbody>
  </table></div>
  <div id="db-count" style="font-size:11px;color:var(--mu);margin-top:8px"></div>
</div>

<!-- ── DECAY ────────────────────────────────────────────────── -->
<div id="decay" class="page">
  <div class="ph"><div><div class="pt">Distance Decay Analysis</div><div class="ps">GAM-derived 35 km threshold · Nakuru County pilot</div></div></div>
  <div class="decay-grid">
    <div class="dz dz-safe"><div class="dz-val" id="dz-safe">—</div><div class="dz-lab">✅ Safe Zone (&lt; 15 km)</div></div>
    <div class="dz dz-tr"><div class="dz-val" id="dz-tr">—</div><div class="dz-lab">⚠️ Transition Zone (15–35 km)</div></div>
    <div class="dz dz-ex"><div class="dz-val" id="dz-ex">—</div><div class="dz-lab">🚫 Exclusion Zone (&gt; 35 km)</div></div>
  </div>
  <div class="row">
    <div style="flex:1"><div class="card"><div class="ct">Patients by Distance Zone</div>
      <canvas id="decay-chart" height="200"></canvas>
    </div></div>
    <div style="flex:0 0 300px">
      <div class="card"><div class="ct">Zone Detail</div>
        <div id="decay-detail"></div>
      </div>
    </div>
  </div>
  <div class="card" style="margin-top:12px"><div class="ct">Exclusion Zone Patients — Immediate Mobile Clinic Priority</div>
    <div id="decay-exclusion-list"></div>
  </div>
</div>

<!-- ── ALERTS ───────────────────────────────────────────────── -->
<div id="alerts" class="page">
  <div class="ph"><div><div class="pt">Alerts</div><div class="ps">Emergency contacts, high-risk flags and urgent outreach actions</div></div>
    <button class="btn btn-g" onclick="markAllRead()">Mark all read</button>
  </div>
  <div id="alerts-list"></div>
</div>

<!-- ── SETTINGS ─────────────────────────────────────────────── -->
<div id="settings" class="page">
  <div class="ph"><div><div class="pt">Settings</div><div class="ps">Coverage area, alert thresholds and export preferences</div></div></div>
  <div class="set-section"><div class="set-title">Coverage Area</div>
    <div class="fg"><label class="fl">County</label><input class="fci" value="Nakuru" readonly></div>
    <div class="fg"><label class="fl">Sub-counties (active)</label>
      <input class="fci" value="Nakuru Town, Rongai, Subukia, Molo, Naivasha, Gilgil, Bahati, Njoro"></div>
    <div class="fg"><label class="fl">Distance threshold (km) — <span id="thresh-val">35</span> km</label>
      <input type="range" min="10" max="100" value="35" id="thresh-range" oninput="document.getElementById('thresh-val').textContent=this.value"></div>
  </div>
  <div class="set-section"><div class="set-title">Alert Thresholds</div>
    <div class="fg"><label class="fl">High-risk flag (dropout score above) — <span id="hr-val">0.70</span></label>
      <input type="range" min="0.1" max="1" step="0.05" value="0.70" id="hr-range" oninput="document.getElementById('hr-val').textContent=parseFloat(this.value).toFixed(2)"></div>
    <div class="fg"><label class="fl">Export format</label>
      <select class="fci"><option>CSV</option><option>JSON</option><option>Excel</option></select></div>
  </div>
  <div class="set-section"><div class="set-title">Notifications</div>
    <label class="toggle-row"><span>Email alerts</span><label class="toggle-sw"><input type="checkbox" checked><span class="toggle-track"></span></label></label>
    <label class="toggle-row"><span>SMS emergency contact alerts</span><label class="toggle-sw"><input type="checkbox" checked><span class="toggle-track"></span></label></label>
    <label class="toggle-row"><span>Daily digest report</span><label class="toggle-sw"><input type="checkbox"><span class="toggle-track"></span></label></label>
  </div>
  <div class="set-section"><div class="set-title">Account</div>
    <div style="background:rgba(255,255,255,.04);border-radius:var(--rs);padding:12px 14px;margin-bottom:12px;font-size:13px">
      <div style="font-weight:600;color:#fff;margin-bottom:6px" id="set-sw-name">Amara Ochieng</div>
      <div style="color:var(--mu)" id="set-sw-role">Social Worker · Nakuru Town</div>
      <div style="color:var(--mu);margin-top:3px" id="set-sw-id">SW-NK-01</div>
    </div>
    <button class="btn btn-pri" onclick="saveSettings()">💾 Save Changes</button>
    <button class="btn btn-d" style="margin-left:8px" onclick="doLogout()">🚪 Logout</button>
  </div>
</div>

</div><!-- /main -->

<!-- PATIENT MODAL -->
<div class="modal-bg" id="patient-modal" onclick="closeModal(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <button class="modal-close" onclick="closeModal()">✕</button>
    <div id="modal-content"></div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
// ── Navigation ───────────────────────────────────────────────
let geoMapInited=false, mcMapInited=false, geoMap, mcMap;
let geoFacLayer, geoHHLayer, geoDecayCircle;
let geoFacOn=true, geoHHOn=true, geoDecayOn=false;
let mcMapObj, mcSelectedHH=null;
let alertStates={};
let decayChartObj=null;

function go(id, btn) {
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nb').forEach(b=>b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  if(btn) btn.classList.add('active');
  if(id==='geo' && !geoMapInited){setTimeout(initGeoMap,80);geoMapInited=true}
  if(id==='mc' && !mcMapInited){setTimeout(initMCMap,80);mcMapInited=true}
  if(id==='decay') renderDecay();
  if(id==='triage') renderTriage();
  if(id==='db') renderDB();
  if(id==='alerts') renderAlerts();
  if(id==='hub') renderHub();
  if(id==='mc') renderMC();
  if(id==='geo') renderGeoStats();
}

// ── Risk helpers ─────────────────────────────────────────────
const RC={High:'var(--dan)',Medium:'var(--amb)',Low:'var(--suc)'};
const RB={High:'p-hi',Medium:'p-med',Low:'p-lo'};
function rPill(r){return `<span class="pill ${RB[r]||'p-pa'}">${r}</span>`}
function rColor(r){return RC[r]||'#aaa'}
function rIcon(r){return r==='High'?'🔴':r==='Medium'?'🟡':'🟢'}

// ── Haversine distance ───────────────────────────────────────
function haversine(la1,lo1,la2,lo2){
  const R=6371,dLat=(la2-la1)*Math.PI/180,dLon=(lo2-lo1)*Math.PI/180;
  const a=Math.sin(dLat/2)**2+Math.cos(la1*Math.PI/180)*Math.cos(la2*Math.PI/180)*Math.sin(dLon/2)**2;
  return R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));
}
function nearestFac(lat,lng){
  let best=null,bd=9999;
  FACILITIES.forEach(f=>{const d=haversine(lat,lng,f.lat,f.lng);if(d<bd){bd=d;best={...f,dist:d}}});
  return best;
}

// ── KPIs ─────────────────────────────────────────────────────
function renderHub(){
  const hi=PATIENTS.filter(p=>p.risk==='High').length;
  const me=PATIENTS.filter(p=>p.risk==='Medium').length;
  const lo=PATIENTS.filter(p=>p.risk==='Low').length;
  const ins=PATIENTS.filter(p=>p.insurance==='NHIF').length;
  const ex=PATIENTS.filter(p=>p.distance>35).length;
  document.getElementById('hub-kpis').innerHTML=`
    <div class="sc"><div class="sv">${PATIENTS.length}</div><div class="sl">Total patients</div></div>
    <div class="sc"><div class="sv" style="color:var(--dan)">${hi}</div><div class="sl">High risk</div><div class="sd">⬆ Immediate action</div></div>
    <div class="sc"><div class="sv" style="color:var(--amb)">${me}</div><div class="sl">Medium risk</div></div>
    <div class="sc"><div class="sv" style="color:var(--suc)">${lo}</div><div class="sl">Low risk</div></div>
    <div class="sc"><div class="sv">${ins}</div><div class="sl">NHIF insured</div></div>
    <div class="sc"><div class="sv" style="color:var(--dan)">${ex}</div><div class="sl">&gt;35 km exclusion zone</div></div>`;
  document.getElementById('kpi-hi-top').textContent=hi+' High Risk';
  // high risk alerts
  const hiP=PATIENTS.filter(p=>p.risk==='High').slice(0,5);
  document.getElementById('hub-alert-list').innerHTML=hiP.map(p=>`
    <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bd);cursor:pointer" onclick="openModal('${p.id}')">
      <div><div style="font-size:13px;font-weight:600;color:#fff">${p.name}</div><div style="font-size:11px;color:var(--mu)">${p.sub_county} · ${p.condition}</div></div>
      <div style="text-align:right"><div>${rPill(p.risk)}</div><div style="font-size:11px;color:var(--mu);margin-top:3px">${p.distance} km · Dropout: ${p.dropout_score}</div></div>
    </div>`).join('');
  // SW coverage
  document.getElementById('sw-coverage-list').innerHTML=WORKERS.map(w=>{
    const cnt=PATIENTS.filter(p=>p.sw_id===w.id).length;
    const hiCnt=PATIENTS.filter(p=>p.sw_id===w.id&&p.risk==='High').length;
    return `<div style="display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--bd)">
      <div><div style="font-size:13px;font-weight:600;color:#fff">${w.name}</div><div style="font-size:11px;color:var(--mu)">${w.sub_county} · ${w.id}</div></div>
      <div style="text-align:right;font-size:12px"><span style="color:#fff">${cnt} patients</span> &nbsp;<span style="color:var(--dan)">${hiCnt} high</span></div>
    </div>`;}).join('');
}
renderHub();

// ── GEO MAP ──────────────────────────────────────────────────
function renderGeoStats(){
  const hi=PATIENTS.filter(p=>p.risk==='High').length;
  document.getElementById('geo-stats').innerHTML=`
    <div class="sc"><div class="sv">${FACILITIES.length}</div><div class="sl">Facilities mapped</div></div>
    <div class="sc"><div class="sv">${PATIENTS.length}</div><div class="sl">Households</div></div>
    <div class="sc"><div class="sv" style="color:var(--dan)">${hi}</div><div class="sl">High-risk households</div></div>
    <div class="sc"><div class="sv" style="color:var(--amb)">${PATIENTS.filter(p=>p.distance>35).length}</div><div class="sl">Beyond 35 km threshold</div></div>`;
}

function initGeoMap(){
  renderGeoStats();
  geoMap=L.map('geo-map').setView([-0.35,36.08],10);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap'}).addTo(geoMap);
  geoFacLayer=L.layerGroup();
  FACILITIES.forEach(f=>{
    L.circleMarker([f.lat,f.lng],{radius:6,fillColor:'#7eb8f7',color:'#fff',weight:1,fillOpacity:.8})
      .addTo(geoFacLayer).bindPopup(`<b>${f.name}</b><br>${f.type}<br>${f.sub_county}`);
  });
  geoHHLayer=L.layerGroup();
  PATIENTS.forEach(p=>{
    L.circleMarker([p.lat,p.lng],{radius:7,fillColor:rColor(p.risk),color:'#fff',weight:1,fillOpacity:.85})
      .addTo(geoHHLayer).bindPopup(`<b>${p.name}</b><br>${p.id}<br>${p.condition} · ${p.risk} risk<br>Distance: ${p.distance} km<br>SW: ${p.sw_name}`);
  });
  geoFacLayer.addTo(geoMap);
  geoHHLayer.addTo(geoMap);
  // click to drop pin
  geoMap.on('click',function(e){
    const lat=e.latlng.lat,lng=e.latlng.lng;
    if(window._pinMarker) geoMap.removeLayer(window._pinMarker);
    window._pinMarker=L.marker([lat,lng],{icon:L.divIcon({html:'📌',iconSize:[20,20],iconAnchor:[10,20],className:''})}).addTo(geoMap);
    const near=[...PATIENTS].map(p=>({...p,d:haversine(lat,lng,p.lat,p.lng)})).sort((a,b)=>a.d-b.d).slice(0,10);
    const nearFac=nearestFac(lat,lng);
    let html=`<div style="font-size:11px;font-weight:600;color:var(--tm);margin-bottom:8px">Pin: ${lat.toFixed(4)}, ${lng.toFixed(4)}</div>`;
    if(nearFac) html+=`<div style="background:rgba(29,158,117,.1);border-radius:var(--rs);padding:7px 9px;margin-bottom:8px;font-size:11px"><b style="color:#fff">Nearest facility:</b><br>${nearFac.name} — ${nearFac.dist.toFixed(1)} km<br><span style="color:var(--mu)">${nearFac.type}</span></div>`;
    html+=`<div style="font-size:11px;font-weight:600;color:var(--mu);margin-bottom:6px">10 nearest households:</div>`;
    near.forEach((p,i)=>{
      const note=p.d>35?'⚠️ Beyond decay threshold':p.d>15?'🟡 Transition zone':'✅ Safe zone';
      html+=`<div style="padding:6px 0;border-bottom:1px solid var(--bd);font-size:11px;cursor:pointer" onclick="openModal('${p.id}')">
        <b style="color:#fff">${i+1}. ${p.name}</b> <span style="color:var(--mu)">${p.id}</span><br>
        ${p.condition} · ${rIcon(p.risk)} ${p.risk} · ${p.d.toFixed(1)} km<br>
        <span style="color:var(--mu)">${note}</span>
      </div>`;
    });
    document.getElementById('geo-decay-results').innerHTML=html;
  });
}
function geoToggle(layer){
  if(layer==='facilities'){
    geoFacOn=!geoFacOn;
    geoFacOn?geoFacLayer.addTo(geoMap):geoMap.removeLayer(geoFacLayer);
    document.getElementById('btn-fac').textContent='🏥 Facilities '+(geoFacOn?'ON':'OFF');
    document.getElementById('btn-fac').className='btn '+(geoFacOn?'btn-t':'btn-g');
  } else if(layer==='households'){
    geoHHOn=!geoHHOn;
    geoHHOn?geoHHLayer.addTo(geoMap):geoMap.removeLayer(geoHHLayer);
    document.getElementById('btn-hh').textContent='🏠 Households '+(geoHHOn?'ON':'OFF');
    document.getElementById('btn-hh').className='btn '+(geoHHOn?'btn-t':'btn-g');
  } else if(layer==='decay'){
    geoDecayOn=!geoDecayOn;
    if(geoDecayOn){
      geoDecayCircle=L.circle([-0.3031,36.0800],{radius:35000,color:'#FCD34D',fillColor:'#FCD34D',fillOpacity:.05,dashArray:'8 4'}).addTo(geoMap);
    } else if(geoDecayCircle){
      geoMap.removeLayer(geoDecayCircle);
    }
    document.getElementById('btn-decay').textContent='⭕ Decay Ring '+(geoDecayOn?'ON':'OFF');
    document.getElementById('btn-decay').className='btn '+(geoDecayOn?'btn-t':'btn-g');
  }
}

// ── TRIAGE ───────────────────────────────────────────────────
function renderTriage(){
  const risk=document.getElementById('tr-risk').value;
  const sw=document.getElementById('tr-sw').value;
  const cond=document.getElementById('tr-cond').value;
  const q=document.getElementById('tr-search').value.toLowerCase();
  let data=[...PATIENTS].filter(p=>{
    return (!risk||p.risk===risk)&&(!sw||p.sw_id===sw)&&(!cond||p.condition===cond)&&
      (!q||p.name.toLowerCase().includes(q)||p.id.toLowerCase().includes(q)||p.condition.toLowerCase().includes(q));
  }).sort((a,b)=>{const o={High:0,Medium:1,Low:2};return o[a.risk]-o[b.risk]||(b.dropout_score-a.dropout_score)});
  document.getElementById('triage-body').innerHTML=data.map(p=>`
    <tr class="clickable" onclick="openModal('${p.id}')">
      <td style="font-family:monospace;font-size:11px;color:var(--mu)">${p.id}</td>
      <td style="font-weight:600;color:#fff">${p.name}</td>
      <td>${p.age}/${p.gender}</td>
      <td>${p.sub_county}</td>
      <td>${p.condition}</td>
      <td>${rPill(p.risk)}</td>
      <td>${p.distance} km</td>
      <td>${p.insurance}</td>
      <td><div style="display:flex;align-items:center;gap:6px"><span>${p.dropout_score}</span>
        <div class="risk-bar" style="width:50px"><div class="risk-fill" style="width:${p.dropout_score*100}%;background:${rColor(p.risk)}"></div></div></div></td>
      <td>${p.sw_name}</td>
      <td style="color:var(--mu)">${p.last_visit==='NaN'?'No record':p.last_visit}</td>
    </tr>`).join('');
  document.getElementById('triage-count').textContent=`Showing ${data.length} of ${PATIENTS.length} patients`;
}
// populate triage filters
(function(){
  const sw=document.getElementById('tr-sw');
  WORKERS.forEach(w=>{const o=document.createElement('option');o.value=w.id;o.textContent=w.name;sw.appendChild(o)});
  const conds=[...new Set(PATIENTS.map(p=>p.condition))].sort();
  const cc=document.getElementById('tr-cond');
  conds.forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;cc.appendChild(o)});
})();

// ── MOBILE CLINIC ────────────────────────────────────────────
let mcData=[];
function renderMC(){
  const q=document.getElementById('mc-search').value.toLowerCase();
  const risk=document.getElementById('mc-risk').value;
  const vtype=document.getElementById('mc-vtype').value;
  mcData=[...PATIENTS].filter(p=>
    (!q||p.name.toLowerCase().includes(q)||p.id.toLowerCase().includes(q))&&
    (!risk||p.risk===risk)&&(!vtype||p.visit_type===vtype)
  ).sort((a,b)=>{const o={High:0,Medium:1,Low:2};return o[a.risk]-o[b.risk]});
  document.getElementById('mc-count').textContent=`(${mcData.length})`;
  document.getElementById('mc-list').innerHTML=mcData.map(p=>`
    <div class="hh-card${mcSelectedHH===p.id?' selected':''}" id="hh-${p.id}" onclick="selectHH('${p.id}')">
      <div class="hh-icon" style="background:${rColor(p.risk)}22">${rIcon(p.risk)}</div>
      <div class="hh-info">
        <div class="hh-name">${p.name} · ${p.id}</div>
        <div class="hh-sub">${p.sub_county} · ${p.condition} · ${p.distance} km</div>
      </div>
      <span class="pill ${RB[p.visit_type]||'p-pa'}" style="font-size:10px">${p.visit_type||'—'}</span>
    </div>`).join('');
}
function initMCMap(){
  mcMapObj=L.map('mc-map').setView([-0.35,36.08],10);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap'}).addTo(mcMapObj);
  FACILITIES.forEach(f=>{
    L.circleMarker([f.lat,f.lng],{radius:5,fillColor:'#7eb8f7',color:'#fff',weight:1,fillOpacity:.7})
      .addTo(mcMapObj).bindPopup(`<b>${f.name}</b><br>${f.type}`);
  });
}
function selectHH(id){
  mcSelectedHH=id;
  document.querySelectorAll('.hh-card').forEach(c=>c.classList.remove('selected'));
  const el=document.getElementById('hh-'+id);
  if(el){el.classList.add('selected');el.scrollIntoView({block:'nearest',behavior:'smooth'})}
  const p=PATIENTS.find(x=>x.id===id);
  if(!p) return;
  const nf=nearestFac(p.lat,p.lng);
  // move map
  if(mcMapObj){
    mcMapObj.setView([p.lat,p.lng],14);
    if(window._mcPin) mcMapObj.removeLayer(window._mcPin);
    window._mcPin=L.circleMarker([p.lat,p.lng],{radius:10,fillColor:rColor(p.risk),color:'#fff',weight:2,fillOpacity:.9}).addTo(mcMapObj)
      .bindPopup(`<b>${p.name}</b><br>${p.condition}`).openPopup();
    if(nf && window._mcFacPin) mcMapObj.removeLayer(window._mcFacPin);
    if(nf) window._mcFacPin=L.circleMarker([nf.lat,nf.lng],{radius:8,fillColor:'#7eb8f7',color:'#fff',weight:2,fillOpacity:.9})
      .addTo(mcMapObj).bindPopup(`<b>${nf.name}</b><br>${nf.type}`).openPopup();
  }
  const sw=WORKERS.find(w=>w.id===p.sw_id)||{};
  document.getElementById('mc-detail').innerHTML=`
    <div class="card">
      <div class="ct">🏠 ${p.id} — Patient Detail</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px">
        <div class="pf"><div class="pf-l">Name</div><div class="pf-v">${p.name} · ${p.age} yrs</div></div>
        <div class="pf"><div class="pf-l">Sub-county</div><div class="pf-v">${p.sub_county}</div></div>
        <div class="pf"><div class="pf-l">Condition</div><div class="pf-v">${p.condition}</div></div>
        <div class="pf"><div class="pf-l">Nearest facility</div><div class="pf-v">${nf?nf.name:'—'}</div></div>
        <div class="pf"><div class="pf-l">Distance</div><div class="pf-v">${nf?nf.dist.toFixed(1)+' km':p.distance+' km'}</div></div>
        <div class="pf"><div class="pf-l">Risk level</div><div class="pf-v">${rIcon(p.risk)} ${p.risk}</div></div>
        <div class="pf"><div class="pf-l">Insurance</div><div class="pf-v">${p.insurance}</div></div>
        <div class="pf"><div class="pf-l">Visit type</div><div class="pf-v">${p.visit_type}</div></div>
        <div class="pf"><div class="pf-l">Social Worker</div><div class="pf-v">${p.sw_name}</div></div>
      </div>
      <div style="background:rgba(255,255,255,.04);border-radius:var(--rs);padding:8px 10px;font-size:12px;margin-bottom:10px">
        <b>Person of contact in system:</b><br>${p.contact_name} · ${p.contact_phone}<br>
        <b style="color:var(--mu)">SW contact:</b> ${sw.phone||'—'}
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-t" onclick="openModal('${p.id}')">👤 Full Profile</button>
        <button class="btn btn-n">📍 Route to Facility</button>
        <button class="btn btn-d">🚨 Flag Emergency</button>
      </div>
    </div>`;
}

// ── PATIENT DB ───────────────────────────────────────────────
(function(){
  const scs=[...new Set(PATIENTS.map(p=>p.sub_county))].sort();
  const el=document.getElementById('db-sc');
  scs.forEach(s=>{const o=document.createElement('option');o.value=s;o.textContent=s;el.appendChild(o)});
  const swEl=document.getElementById('db-sw');
  WORKERS.forEach(w=>{const o=document.createElement('option');o.value=w.id;o.textContent=w.name;swEl.appendChild(o)});
})();
function renderDB(){
  const q=document.getElementById('db-search').value.toLowerCase();
  const risk=document.getElementById('db-risk').value;
  const ins=document.getElementById('db-ins').value;
  const sc=document.getElementById('db-sc').value;
  const sw=document.getElementById('db-sw').value;
  const data=PATIENTS.filter(p=>
    (!q||p.name.toLowerCase().includes(q)||p.id.toLowerCase().includes(q)||p.condition.toLowerCase().includes(q))&&
    (!risk||p.risk===risk)&&(!ins||p.insurance===ins)&&(!sc||p.sub_county===sc)&&(!sw||p.sw_id===sw));
  const hiCnt=data.filter(p=>p.risk==='High').length;
  const nhif=data.filter(p=>p.insurance==='NHIF').length;
  const unins=data.filter(p=>p.insurance==='None').length;
  document.getElementById('db-summary').innerHTML=`
    <span class="sum-item"><span class="sum-val">${data.length}</span> total</span>
    <span class="sum-item" style="color:var(--dan)"><span class="sum-val">${hiCnt}</span> high risk</span>
    <span class="sum-item" style="color:var(--suc)"><span class="sum-val">${nhif}</span> NHIF</span>
    <span class="sum-item" style="color:var(--mu)"><span class="sum-val">${unins}</span> uninsured</span>
    <span class="sum-item" style="color:var(--amb)"><span class="sum-val">${data.filter(p=>p.distance>35).length}</span> exclusion zone</span>`;
  document.getElementById('db-body').innerHTML=data.map(p=>`
    <tr onclick="openModal('${p.id}')">
      <td style="font-family:monospace;font-size:11px;color:var(--mu)">${p.id}</td>
      <td style="font-weight:600;color:#fff">${p.name}</td>
      <td>${p.age}/${p.gender}</td>
      <td>${p.sub_county}</td>
      <td>${p.condition}</td>
      <td>${rPill(p.risk)}</td>
      <td>${p.distance} km</td>
      <td>${p.insurance}</td>
      <td style="color:var(--mu);font-size:11px">${p.sw_name}</td>
      <td style="color:var(--mu)">${p.last_visit==='NaN'?'—':p.last_visit}</td>
    </tr>`).join('');
  document.getElementById('db-count').textContent=`Showing ${data.length} of ${PATIENTS.length} patients`;
}
function exportCSV(){
  const rows=[['ID','Name','Age','Gender','Sub-county','Condition','Risk','Distance','Insurance','Social Worker','Last Visit','Dropout Score']];
  PATIENTS.forEach(p=>rows.push([p.id,p.name,p.age,p.gender,p.sub_county,p.condition,p.risk,p.distance,p.insurance,p.sw_name,p.last_visit,p.dropout_score]));
  const csv=rows.map(r=>r.join(',')).join('\n');
  const a=document.createElement('a');a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(csv);
  a.download='HealthLink_Patients_Export.csv';a.click();
}

// ── DISTANCE DECAY ───────────────────────────────────────────
function renderDecay(){
  const safe=PATIENTS.filter(p=>p.distance<=15);
  const tr=PATIENTS.filter(p=>p.distance>15&&p.distance<=35);
  const ex=PATIENTS.filter(p=>p.distance>35);
  document.getElementById('dz-safe').textContent=safe.length;
  document.getElementById('dz-tr').textContent=tr.length;
  document.getElementById('dz-ex').textContent=ex.length;
  document.getElementById('decay-detail').innerHTML=`
    <div style="font-size:12px;line-height:1.7;color:rgba(255,255,255,.7)">
      <p>The <b style="color:#fff">35 km GAM threshold</b> is the empirically derived point at which healthcare utilisation probability declines sharply.</p>
      <p style="margin-top:8px"><b style="color:var(--suc)">Safe zone</b> (&lt;15 km): ${safe.length} patients — ${Math.round(safe.filter(p=>p.risk==='High').length/safe.length*100)||0}% high risk</p>
      <p><b style="color:var(--amb)">Transition</b> (15–35 km): ${tr.length} patients — ${Math.round(tr.filter(p=>p.risk==='High').length/tr.length*100)||0}% high risk</p>
      <p><b style="color:var(--dan)">Exclusion</b> (&gt;35 km): ${ex.length} patients — ${Math.round(ex.filter(p=>p.risk==='High').length/ex.length*100)||0}% high risk</p>
      <p style="margin-top:8px;font-size:11px;color:var(--mu)">Note: Based on self-reported perceived distance (r=-0.040 vs geodesic). Treat as behavioural heuristic.</p>
    </div>`;
  document.getElementById('decay-exclusion-list').innerHTML=ex.slice(0,10).map(p=>`
    <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bd);cursor:pointer" onclick="openModal('${p.id}')">
      <div><div style="font-size:13px;font-weight:600;color:#fff">${p.name} <span style="font-size:11px;color:var(--mu)">${p.id}</span></div>
      <div style="font-size:11px;color:var(--mu)">${p.sub_county} · ${p.condition} · SW: ${p.sw_name}</div></div>
      <div style="text-align:right">${rPill(p.risk)}<div style="font-size:11px;color:var(--dan);margin-top:2px">${p.distance} km</div></div>
    </div>`).join('')+(ex.length>10?`<div style="font-size:11px;color:var(--mu);padding:8px 0">+${ex.length-10} more patients in exclusion zone</div>`:'');
  if(decayChartObj) decayChartObj.destroy();
  const ctx=document.getElementById('decay-chart').getContext('2d');
  decayChartObj=new Chart(ctx,{type:'bar',data:{labels:['Safe (<15km)','Transition (15-35km)','Exclusion (>35km)'],datasets:[{data:[safe.length,tr.length,ex.length],backgroundColor:['rgba(110,231,183,.6)','rgba(252,211,77,.6)','rgba(248,113,113,.6)'],borderColor:['#6EE7B7','#FCD34D','#F87171'],borderWidth:1}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{ticks:{color:'rgba(255,255,255,.5)'},grid:{color:'rgba(255,255,255,.05)'}},x:{ticks:{color:'rgba(255,255,255,.5)'},grid:{display:false}}}}});
}

// ── ALERTS ───────────────────────────────────────────────────
const ALERT_DEFS=[
  {id:'a1',level:'CRITICAL',icon:'🚨',title:'Emergency: Mary Wanjiku — HH-NK-01100',body:'Reported chest pain and difficulty breathing. Last clinic visit: 12 Mar 2026. Missed follow-up scheduled 5 Apr 2026. Hypertension — High dropout risk flagged.',contact:'James Wanjiku (Spouse)',phone:'+254 712 445 678',actions:['📞 Call Emergency Contact','🚑 Dispatch Mobile Clinic','✅ Acknowledge'],ts:'Today at 08:14 AM · Nakuru Town',resolved:false},
  {id:'a2',level:'CRITICAL',icon:'🚨',title:'High-risk new profile — HH-NK-00312 (Molo)',body:'New registration flagged risk score 0.91. Distance 52.3 km — beyond decay threshold. No insurance. Never attended any facility.',contact:'Grace Wanjiku (Mother)',phone:'+254 728 990 112',actions:['📞 Call Emergency Contact','📅 Schedule Home Visit','✅ Acknowledge'],ts:'Today at 09:32 AM · Molo Sub-county',resolved:false},
  {id:'a3',level:'CRITICAL',icon:'⚠️',title:'Missed follow-up — HH-NK-00891 (Njoro)',body:'Patient missed 2 consecutive follow-up appointments. Last contact: 15 Feb 2026. Dropout risk score elevated to 0.82. Education barrier noted.',contact:'Peter Kamau (Brother)',phone:'+254 700 334 891',actions:['📞 Call Emergency Contact','💬 Send SMS Reminder','✅ Acknowledge'],ts:'Yesterday at 04:45 PM · Njoro Sub-county',resolved:false},
  {id:'a4',level:'WARNING',icon:'🔔',title:'Distance threshold exceeded — HH-NK-00455 (Subukia)',body:'Household distance 36.7 km exceeds 35 km decay threshold. Utilisation probability dropped to 38%. Recommend mobile clinic deployment.',contact:null,phone:null,actions:['🗺 Route Mobile Clinic','✅ Acknowledge'],ts:'2 days ago · Subukia Sub-county',resolved:false},
  {id:'a5',level:'RESOLVED',icon:'✅',title:'Follow-up completed — HH-NK-00678 (Nakuru Town)',body:'Patient attended scheduled follow-up. Retention score improved to 78%. No further immediate action required.',contact:null,phone:null,actions:[],ts:'Resolved 12 Mar 2026 · Nakuru Town',resolved:true},
];
function renderAlerts(){
  const list=document.getElementById('alerts-list');
  const crit=ALERT_DEFS.filter(a=>!alertStates[a.id+'_done']&&!a.resolved&&a.level==='CRITICAL').length;
  document.getElementById('alert-badge').textContent=crit;
  list.innerHTML=ALERT_DEFS.map(a=>{
    const done=alertStates[a.id+'_done'];
    const cls=a.resolved||done?'ac ac-g':a.level==='CRITICAL'?'ac ac-c':'ac ac-w';
    const bcls=a.resolved||done?'ac-badge ac-badge-g':a.level==='CRITICAL'?'ac-badge ac-badge-c':'ac-badge ac-badge-w';
    const contactHtml=a.contact?`<div class="ac-contact">
      <div style="font-size:11px;color:var(--mu);margin-bottom:3px">📞 Emergency Contact</div>
      <div style="font-weight:600;color:#fff;font-size:12px">${a.contact}</div>
      <div style="font-size:12px;color:var(--mu)">Phone: ${a.phone}</div>
    </div>`:'';
    const actionsHtml=done?`<span style="color:var(--suc);font-size:12px">✅ Handled</span>`:
      a.actions.map((act,i)=>{
        let cls2='btn-g';
        if(act.includes('Call')) cls2='btn-d';
        else if(act.includes('Dispatch')||act.includes('Route')||act.includes('Schedule')) cls2='btn-n';
        else if(act.includes('Acknowledge')||act.includes('SMS')) cls2='btn-t';
        return `<button class="btn ${cls2}" onclick="handleAlert('${a.id}','${act}')">${act}</button>`;
      }).join('');
    return `<div class="${cls}" id="alert-card-${a.id}" style="${done?'opacity:.5':''}">
      <div class="ac-head"><span class="${bcls}">${a.level}</span><span style="font-size:18px">${a.icon}</span></div>
      <div class="ac-title">${a.title}</div>
      <div class="ac-body" style="margin-top:6px">${a.body}</div>
      ${contactHtml}
      <div class="ac-actions">${actionsHtml}</div>
      <div class="ac-ts">${a.ts}</div>
    </div>`;
  }).join('');
}
function handleAlert(id,action){
  if(action.includes('Acknowledge')||action.includes('SMS')){
    alertStates[id+'_done']=true;
    renderAlerts();
    return;
  }
  if(action.includes('Call')){
    const a=ALERT_DEFS.find(x=>x.id===id);
    alert(`📞 Calling ${a.contact}\n${a.phone}\n\nIn a real deployment this would trigger an outbound call via the integrated telephony system.`);
    return;
  }
  if(action.includes('Dispatch')||action.includes('Route')){
    alert('🚑 Mobile clinic dispatch request sent to routing module.\nNavigating to Mobile Clinic...');
    go('mc',document.querySelectorAll('.nb')[3]);return;
  }
  if(action.includes('Schedule')){
    alert('📅 Home visit scheduled. Social worker will be notified.');
    alertStates[id+'_done']=true;renderAlerts();
  }
}
function markAllRead(){ALERT_DEFS.forEach(a=>{alertStates[a.id+'_done']=true});renderAlerts()}

// ── PATIENT MODAL ────────────────────────────────────────────
function openModal(id){
  const p=PATIENTS.find(x=>x.id===id);
  if(!p) return;
  const sw=WORKERS.find(w=>w.id===p.sw_id)||{};
  const nf=nearestFac(p.lat,p.lng);
  const zone=p.distance>35?'🚫 Exclusion Zone':p.distance>15?'⚠️ Transition Zone':'✅ Safe Zone';
  document.getElementById('modal-content').innerHTML=`
    <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px">
      <div>
        <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:2px">${p.name}</div>
        <div style="font-size:12px;color:var(--mu)">${p.id} · ${p.age} yrs · ${p.gender==='F'?'Female':'Male'} · ${p.sub_county}</div>
      </div>
      ${rPill(p.risk)}
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">
      <div class="pf"><div class="pf-l">Condition</div><div class="pf-v">${p.condition}</div></div>
      <div class="pf"><div class="pf-l">Visit type</div><div class="pf-v">${p.visit_type}</div></div>
      <div class="pf"><div class="pf-l">Insurance</div><div class="pf-v">${p.insurance}</div></div>
      <div class="pf"><div class="pf-l">Last visit</div><div class="pf-v">${p.last_visit==='NaN'?'No record':p.last_visit}</div></div>
      <div class="pf"><div class="pf-l">Distance to care</div><div class="pf-v">${p.distance} km · ${zone}</div></div>
      <div class="pf"><div class="pf-l">Nearest facility</div><div class="pf-v">${nf?nf.name+' ('+nf.dist.toFixed(1)+' km)':'—'}</div></div>
      <div class="pf"><div class="pf-l">Dropout risk score</div><div class="pf-v">
        ${p.dropout_score}
        <div class="risk-bar" style="margin-top:4px"><div class="risk-fill" style="width:${p.dropout_score*100}%;background:${rColor(p.risk)}"></div></div>
      </div></div>
      <div class="pf"><div class="pf-l">Access score</div><div class="pf-v">
        ${p.access_score}
        <div class="risk-bar" style="margin-top:4px"><div class="risk-fill" style="width:${p.access_score*100}%;background:var(--tm)"></div></div>
      </div></div>
    </div>
    <div style="background:rgba(255,255,255,.04);border-radius:var(--rs);padding:10px 12px;margin-bottom:12px">
      <div style="font-size:11px;font-weight:600;color:var(--mu);text-transform:uppercase;margin-bottom:6px">Clinical Notes</div>
      <div style="font-size:13px;color:rgba(255,255,255,.75);line-height:1.6">${p.notes}</div>
    </div>
    <div style="background:rgba(255,255,255,.04);border-radius:var(--rs);padding:10px 12px;margin-bottom:12px">
      <div style="font-size:11px;font-weight:600;color:var(--mu);text-transform:uppercase;margin-bottom:6px">Social Worker</div>
      <div style="font-size:13px;font-weight:600;color:#fff">${sw.name||'—'}</div>
      <div style="font-size:12px;color:var(--mu)">${sw.sub_county||''} · ${sw.id||''}</div>
      <div style="font-size:12px;color:var(--mu);margin-top:2px">${sw.phone||''} · <a href="mailto:${sw.email||''}" style="color:var(--tm)">${sw.email||''}</a></div>
    </div>
    <div style="background:rgba(255,255,255,.04);border-radius:var(--rs);padding:10px 12px;margin-bottom:14px">
      <div style="font-size:11px;font-weight:600;color:var(--mu);text-transform:uppercase;margin-bottom:6px">Emergency Contact</div>
      <div style="font-size:13px;font-weight:600;color:#fff">${p.contact_name}</div>
      <div style="font-size:12px;color:var(--mu)">${p.contact_phone}</div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn btn-d" onclick="alert('📞 Calling ${p.contact_phone}')">📞 Call Emergency Contact</button>
      <button class="btn btn-t" onclick="alert('✅ Flag updated.')">✅ Update Status</button>
      <button class="btn btn-n" onclick="go('mc',document.querySelectorAll(\'.nb\')[3]);closeModal()">🚑 Route Mobile Clinic</button>
    </div>`;
  document.getElementById('patient-modal').classList.add('show');
}
function closeModal(e){
  if(!e||e.target===document.getElementById('patient-modal'))
    document.getElementById('patient-modal').classList.remove('show');
}

// ── SETTINGS ─────────────────────────────────────────────────
function saveSettings(){alert('✅ Settings saved successfully.');}
function doLogout(){if(confirm('Log out of HealthLink Kenya?')) window.location.reload();}

// ── INIT ─────────────────────────────────────────────────────
renderHub();
renderDB();
document.getElementById('set-sw-name').textContent=WORKERS[0].name;
document.getElementById('set-sw-role').textContent=WORKERS[0].role+' · '+WORKERS[0].sub_county;
document.getElementById('set-sw-id').textContent=WORKERS[0].id;
</script>
</body>
</html>
