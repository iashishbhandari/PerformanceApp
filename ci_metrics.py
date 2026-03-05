import json
import subprocess
import time
import os
from datetime import datetime

# Config
project="PerformanceApp.project"
scheme = "PerformanceApp"
destination = "generic/platform=iOS Simulator"
history_file = "ci_metrics_history.json"

# --- 1. Build ---
start_build = time.time()
build_result = subprocess.run(
    ["xcodebuild", "-project", project, "-scheme", scheme, "-destination", destination, "build"],
    capture_output=True, text=True
)
end_build = time.time()
build_time = end_build - start_build
warnings_count = build_result.stdout.count("warning:")
errors_count = build_result.stdout.count("error:")

# --- 2. Test ---
start_test = time.time()
test_result = subprocess.run(
    ["xcodebuild", "-project", project, "-scheme", scheme, "-destination", destination, "test"],
    capture_output=True, text=True
)
end_test = time.time()
test_duration = end_test - start_test
total_tests = test_result.stdout.count("Test Case '-")
passed_tests = test_result.stdout.count("passed")
failed_tests = test_result.stdout.count("failed")

# --- 3. Binary size ---
app_path = f"build/Debug-iphonesimulator/{scheme}.app"
dsym_path = f"build/Debug-iphonesimulator/{scheme}.app.dSYM"
binary_size_mb = os.path.getsize(app_path)/1024/1024 if os.path.exists(app_path) else 0
dsym_size_mb = os.path.getsize(dsym_path)/1024/1024 if os.path.exists(dsym_path) else 0

# --- 4. Startup time / memory (example) ---
startup_time_ms = 450
memory_mb = 120

# --- 5. New metrics entry ---
new_metrics = {
    "build_time_sec": build_time,
    "warnings_count": warnings_count,
    "errors_count": errors_count,
    "test_results": {
        "total": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "duration_sec": test_duration
    },
    "startup_time_ms": startup_time_ms,
    "memory_mb": memory_mb,
    "binary_size_mb": binary_size_mb,
    "dsym_size_mb": dsym_size_mb,
    "timestamp": datetime.utcnow().isoformat()
}

# --- 6. Append to history file ---
if os.path.exists(history_file):
    with open(history_file) as f:
        history = json.load(f)
else:
    history = []

history.append(new_metrics)
# Keep only last 30 runs
history = history[-30:]

with open(history_file, "w") as f:
    json.dump(history, f, indent=2)

print(f"Metrics saved. Total runs stored: {len(history)}")
