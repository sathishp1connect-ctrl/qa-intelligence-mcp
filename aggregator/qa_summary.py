import json
from pathlib import Path

REPORT = Path("reports/merged-report.json")

def generate_summary():
    with open(REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = data["total"]
    passed = data["passed"]
    failed = data["failed"]
    flaky = data["flaky"]
    workers = data["workers"]

    pass_rate = round((passed / total) * 100, 2) if total else 0

    status = "PASS" if failed == 0 else "FAIL"

    recommendation = (
        "Release approved."
        if failed == 0 and flaky == 0
        else "Investigate failed or flaky tests before release."
    )

    return {
        "status": status,
        "workers": workers,
        "total_tests": total,
        "pass_rate": pass_rate,
        "failed": failed,
        "flaky": flaky,
        "recommendation": recommendation
    }

if __name__ == "__main__":
    print(json.dumps(generate_summary(), indent=2))