<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Health Intelligence Dashboard</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  background: #f5f7fa;
}

.nav {
  background: #1e293b;
  color: white;
  padding: 10px;
  display: flex;
  gap: 10px;
}

.nav button {
  background: #334155;
  border: none;
  color: white;
  padding: 8px 12px;
  cursor: pointer;
}

.page {
  display: none;
  padding: 20px;
}

.active {
  display: block;
}

#nakuru-map {
  height: 400px;
  margin-top: 10px;
}
</style>
</head>

<body>

<div class="nav">
  <button onclick="swNav('dashboard')">Dashboard</button>
  <button onclick="swNav('geomap')">Map</button>
</div>

<!-- DASHBOARD -->
<div id="dashboard" class="page active">
  <h2>Dashboard</h2>
  <table border="1" cellpadding="8">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Condition</th>
      </tr>
    </thead>
    <tbody id="tableBody"></tbody>
  </table>
</div>

<!-- MAP -->
<div id="geomap" class="page">
  <h2>Geo Map</h2>
  <div id="nakuru-map"></div>
</div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script>
// ✅ CLEAN STATE (no duplicates)
let allPatients = [
  {id: 1, name: "John Doe", condition: "Diabetes"},
  {id: 2, name: "Jane Smith", condition: "Hypertension"},
  {id: 3, name: "Alex Kim", condition: "Asthma"}
];

let dbFiltered = [...allPatients];

// ✅ NAVIGATION
function swNav(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(page).classList.add('active');

  if (page === 'geomap') {
    setTimeout(initMap, 100);
  }
}

// ✅ TABLE RENDER
function renderTable() {
  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = '';

  dbFiltered.forEach(p => {
    const row = `
      <tr>
        <td>${p.id}</td>
        <td>${p.name}</td>
        <td>${p.condition}</td>
      </tr>
    `;
    tbody.innerHTML += row;
  });
}

// ✅ MAP
let mapInitialized = false;

function initMap() {
  if (mapInitialized) return;

  const map = L.map('nakuru-map').setView([-0.3031, 36.0800], 11);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
  }).addTo(map);

  L.marker([-0.3031, 36.0800]).addTo(map)
    .bindPopup("Nakuru Center")
    .openPopup();

  mapInitialized = true;
}

// ✅ INIT
renderTable();
</script>

</body>
</html>
