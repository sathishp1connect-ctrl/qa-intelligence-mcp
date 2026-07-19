import json

from src.qa_mcp_server.services.playwright_parser import (
    parse_playwright_report,
)


def summarize_playwright_results(
    report_path: str,
    max_failure_details: int = 20,
) -> dict:
    """
    Summarize and triage a Playwright JSON report.

    Args:
        report_path:
            Path to the Playwright JSON report.

        max_failure_details:
            Maximum failed/flaky test details
            returned to the MCP client.
    """

    if (
        not report_path
        or not report_path.strip()
    ):

        return {
            "error":
            "Report path cannot be empty."
        }

    if max_failure_details < 0:

        return {
            "error":
            "max_failure_details cannot be negative."
        }

    try:

        summary = parse_playwright_report(
            report_path=report_path,
            max_failure_details=max_failure_details,
        )

        return summary.model_dump()

    except FileNotFoundError:

        return {
            "error":
            f"Playwright report not found: "
            f"{report_path}"
        }

    except IsADirectoryError:

        return {
            "error":
            "Report path must point to a "
            f"JSON file: {report_path}"
        }

    except json.JSONDecodeError:

        return {
            "error":
            "Invalid JSON in Playwright "
            f"report: {report_path}"
        }

    except ValueError as error:

        return {
            "error": str(error)
        }

    except PermissionError:

        return {
            "error":
            "Permission denied while reading "
            f"Playwright report: {report_path}"
        }

    except OSError as error:

        return {
            "error":
            "Unable to read Playwright "
            f"report: {error}"
        }