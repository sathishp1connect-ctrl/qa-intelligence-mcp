import json
from pathlib import Path

REPORT_PATH = Path(__file__).resolve().parent.parent.parent.parent / "reports" / "merged-report.json"


def analyze_merged_report() -> dict:
    """
    Analyze the aggregated Playwright execution report and generate
    an AI-ready executive QA summary.
    """

    if not REPORT_PATH.exists():
        return {
            "status": "error",
            "message": "merged-report.json not found"
        }

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        report = json.load(f)

    failed_tests = [
        t["name"]
        for t in report.get("tests", [])
        if t.get("status") == "failed"
    ]

    pass_rate = round(
        (report["passed"] / report["total"]) * 100,
        2
    ) if report["total"] else 0

    return {
        "execution_summary": {
            "total": report["total"],
            "passed": report["passed"],
            "failed": report["failed"],
            "flaky": report["flaky"],
            "pass_rate": f"{pass_rate}%"
        },
        "failed_tests": failed_tests,
        "executive_summary": (
            f"{report['total']} tests executed. "
            f"{report['passed']} passed, "
            f"{report['failed']} failed. "
            f"Overall pass rate: {pass_rate}%."
        )
    }