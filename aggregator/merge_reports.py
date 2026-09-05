import json
from pathlib import Path
from datetime import datetime

# Reports directory
REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"
OUTPUT = REPORT_DIR / "merged-report.json"

# Executive merged summary
merged = {
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "workers": 0,
    "total": 0,
    "passed": 0,
    "failed": 0,
    "flaky": 0,
    "duration_ms": 0,
    "worker_reports": [],
    "tests": []
}

# Read every worker report
for report in REPORT_DIR.glob("*.json"):
    if report.name == "merged-report.json":
        continue

    with open(report, "r", encoding="utf-8") as f:
        data = json.load(f)

    merged["workers"] += 1
    merged["total"] += data.get("total", 0)
    merged["passed"] += data.get("passed", 0)
    merged["failed"] += data.get("failed", 0)
    merged["flaky"] += data.get("flaky", 0)
    merged["duration_ms"] += data.get("duration_ms", 0)

    merged["worker_reports"].append({
        "worker": report.stem,
        "passed": data.get("passed", 0),
        "failed": data.get("failed", 0),
        "flaky": data.get("flaky", 0),
        "duration_ms": data.get("duration_ms", 0)
    })

    merged["tests"].extend(data.get("tests", []))

# Ensure reports folder exists
REPORT_DIR.mkdir(exist_ok=True)

# Write merged report
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2)

print("Merged report created successfully!")
print(f"Location: {OUTPUT}")
print(json.dumps(merged, indent=2))