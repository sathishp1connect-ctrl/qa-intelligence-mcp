import json
from pathlib import Path

# Project reports folder
REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"
OUTPUT = REPORT_DIR / "merged-report.json"

merged = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "flaky": 0,
    "tests": []
}

# Read every pod report except the merged output
for report in REPORT_DIR.glob("*.json"):
    if report.name == "merged-report.json":
        continue

    with open(report, "r", encoding="utf-8") as f:
        data = json.load(f)

    merged["total"] += data.get("total", 0)
    merged["passed"] += data.get("passed", 0)
    merged["failed"] += data.get("failed", 0)
    merged["flaky"] += data.get("flaky", 0)
    merged["tests"].extend(data.get("tests", []))

# Write merged report
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2)

print("Merged report created successfully!")
print(f"Location: {OUTPUT}")
print(json.dumps(merged, indent=2))