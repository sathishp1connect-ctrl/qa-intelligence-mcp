import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("qa-mcp-server")


@mcp.tool()
def health_check() -> str:
    """Check whether the QA MCP server is running."""
    return "QA MCP Server is running successfully!"


def collect_specs(suites: list) -> list:
    """Recursively collect all specs from Playwright suites."""
    specs = []

    for suite in suites:
        specs.extend(suite.get("specs", []))

        # Playwright suites can contain nested suites
        nested_suites = suite.get("suites", [])

        if nested_suites:
            specs.extend(collect_specs(nested_suites))

    return specs


@mcp.tool()
def summarize_playwright_results(report_path: str) -> dict:
    """Summarize test execution statistics from a Playwright JSON report."""

    path = Path(report_path)

    if not path.exists():
        return {
            "error": f"Report file not found: {report_path}"
        }

    with path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    suites = report.get("suites", [])

    specs = collect_specs(suites)

    summary = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "flaky": 0,
    }

    for spec in specs:

        for test in spec.get("tests", []):

            summary["total"] += 1

            status = test.get("status")

            if status == "expected":
                summary["passed"] += 1

            elif status == "unexpected":
                summary["failed"] += 1

            elif status == "skipped":
                summary["skipped"] += 1

            elif status == "flaky":
                summary["flaky"] += 1

    return summary


if __name__ == "__main__":
    mcp.run(transport="stdio")