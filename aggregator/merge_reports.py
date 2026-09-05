import json
from pathlib import Path
from datetime import datetime, UTC

REPORT_DIR = Path("reports")
OUTPUT = REPORT_DIR / "merged-report.json"

merged = {
    "generated_at": datetime.now(UTC).isoformat(),
    "workers": 0,
    "total": 0,
    "passed": 0,
    "failed": 0,
    "flaky": 0,
    "duration_ms": 0,
    "tests": []
}

for report in REPORT_DIR.glob("*.json"):
    if report.name == "merged-report.json":
        continue

    with open(report, "r", encoding="utf-8") as f:
        data = json.load(f)

    merged["workers"] += 1

    stats = data.get("stats", {})
    merged["total"] += stats.get("expected", 0)
    merged["passed"] += stats.get("expected", 0)
    merged["failed"] += stats.get("unexpected", 0)
    merged["flaky"] += stats.get("flaky", 0)
    merged["duration_ms"] += stats.get("duration", 0)

    for suite in data.get("suites", []):
        for spec in suite.get("specs", []):
            for test in spec.get("tests", []):
                outcome = test.get("outcome", "unknown")

                merged["tests"].append({
                    "title": spec.get("title"),
                    "file": suite.get("file"),
                    "status": outcome
                })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2)

print("\n==============================")
print(" EXECUTIVE QA SUMMARY")
print("==============================")
print(f"Workers        : {merged['workers']}")
print(f"Total Tests    : {merged['total']}")
print(f"Passed         : {merged['passed']}")
print(f"Failed         : {merged['failed']}")
print(f"Flaky          : {merged['flaky']}")
print(f"Duration (ms)  : {merged['duration_ms']}")
print("==============================")

status = "PASS" if merged["failed"] == 0 else "FAIL"
print(f"Overall Status : {status}")

print(f"\nMerged report saved to: {OUTPUT}")