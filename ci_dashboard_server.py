import json
import os
from aiohttp import web

# Mobile-friendly dashboard
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <title>iOS CI Metrics Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { background:#111; color:white; font-family:Arial, sans-serif; padding:10px; margin:0; }
    h1,h2 { margin:10px 0; }
    .chart-container {
      background:white; padding:10px; border-radius:10px; margin-bottom:20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    canvas { width:100% !important; height:200px !important; }
  </style>
</head>
<body>
<h1>iOS CI Metrics Dashboard</h1>

<div class="chart-container">
  <h2>Build Time (sec)</h2>
  <canvas id="buildTimeChart"></canvas>
</div>

<div class="chart-container">
  <h2>Test Duration (sec)</h2>
  <canvas id="testDurationChart"></canvas>
</div>

<div class="chart-container">
  <h2>Binary Size (MB)</h2>
  <canvas id="binarySizeChart"></canvas>
</div>

<div class="chart-container">
  <h2>Startup Time (ms)</h2>
  <canvas id="startupChart"></canvas>
</div>

<script>
let metrics = [];

async function loadMetrics() {
  try {
    const res = await fetch("/ci_metrics_history.json");
    metrics = await res.json();
    updateCharts();
  } catch(e) { console.error("Failed to load metrics:", e); }
}

function updateCharts() {
  const labels = metrics.map((_, i)=>i+1);

  buildTimeChart.data.labels = labels;
  buildTimeChart.data.datasets[0].data = metrics.map(m=>m.build_time_sec);
  buildTimeChart.update();

  testDurationChart.data.labels = labels;
  testDurationChart.data.datasets[0].data = metrics.map(m=>m.test_results.duration_sec);
  testDurationChart.update();

  binarySizeChart.data.labels = labels;
  binarySizeChart.data.datasets[0].data = metrics.map(m=>m.binary_size_mb);
  binarySizeChart.update();

  startupChart.data.labels = labels;
  startupChart.data.datasets[0].data = metrics.map(m=>m.startup_time_ms);
  startupChart.update();
}

const buildTimeChart = new Chart(document.getElementById("buildTimeChart"), {
  type:"line", data:{ labels:[], datasets:[{label:"Build Time (sec)", data:[], borderColor:"lime", tension:0.3}] }
});
const testDurationChart = new Chart(document.getElementById("testDurationChart"), {
  type:"line", data:{ labels:[], datasets:[{label:"Test Duration (sec)", data:[], borderColor:"orange", tension:0.3}] }
});
const binarySizeChart = new Chart(document.getElementById("binarySizeChart"), {
  type:"line", data:{ labels:[], datasets:[{label:"Binary Size (MB)", data:[], borderColor:"blue", tension:0.3}] }
});
const startupChart = new Chart(document.getElementById("startupChart"), {
  type:"line", data:{ labels:[], datasets:[{label:"Startup Time (ms)", data:[], borderColor:"red", tension:0.3}] }
});

loadMetrics();
</script>
</body>
</html>
"""

history_file = "ci_metrics_history.json"

async def index(request):
    return web.Response(text=HTML_PAGE, content_type="text/html")

async def metrics_file(request):
    if os.path.exists(history_file):
        with open(history_file) as f:
            data = json.load(f)
        return web.json_response(data)
    else:
        return web.json_response([], status=200)

app = web.Application()
app.router.add_get("/", index)
app.router.add_get(f"/{history_file}", metrics_file)

if __name__ == "__main__":
    web.run_app(app, port=8080)