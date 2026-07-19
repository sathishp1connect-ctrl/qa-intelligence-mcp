import json
import re
from pathlib import Path
from typing import Any

from src.qa_mcp_server.models.test_results import (
    TestDetail,
    TestStatistics,
    TestSummary,
)


ANSI_PATTERN = re.compile(
    r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
)

MAX_ERROR_LENGTH = 1000
DEFAULT_MAX_DETAILS = 20


def strip_ansi(text: str) -> str:
    """Remove ANSI terminal formatting codes."""

    return ANSI_PATTERN.sub("", text)


def collect_specs(suites: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Recursively collect specs from Playwright suites."""

    specs = []

    for suite in suites:

        specs.extend(
            suite.get("specs", [])
        )

        nested_suites = suite.get(
            "suites",
            [],
        )

        if nested_suites:
            specs.extend(
                collect_specs(nested_suites)
            )

    return specs


def get_error_message(
    results: list[dict[str, Any]],
) -> str | None:
    """
    Extract a concise error message.

    Error output is truncated to protect
    the MCP/LLM context window.
    """

    for result in reversed(results):

        error = result.get("error")

        if not error:
            continue

        message = error.get("message")

        if message:

            clean_message = strip_ansi(
                message
            )

            return clean_message[
                :MAX_ERROR_LENGTH
            ]

    return None


def validate_report_structure(
    report: Any,
) -> None:
    """Validate the minimum Playwright JSON structure."""

    if not isinstance(report, dict):

        raise ValueError(
            "Playwright report must be a JSON object."
        )

    if "suites" not in report:

        raise ValueError(
            "Invalid Playwright report: "
            "missing 'suites' field."
        )

    if not isinstance(
        report["suites"],
        list,
    ):

        raise ValueError(
            "Invalid Playwright report: "
            "'suites' must be a list."
        )


def parse_playwright_report(
    report_path: str,
    max_failure_details: int = DEFAULT_MAX_DETAILS,
) -> TestSummary:
    """
    Parse a Playwright JSON report.

    All tests are counted.

    Only a bounded number of failed/flaky
    test details are returned to protect
    the MCP client context window.
    """

    path = Path(report_path)

    if not path.exists():

        raise FileNotFoundError(
            f"Playwright report not found: "
            f"{report_path}"
        )

    if not path.is_file():

        raise IsADirectoryError(
            f"Report path is not a file: "
            f"{report_path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        report = json.load(file)

    validate_report_structure(
        report
    )

    specs = collect_specs(
        report["suites"]
    )

    statistics = TestStatistics()

    failed_tests = []
    flaky_tests = []

    for spec in specs:

        spec_title = spec.get(
            "title",
            "Unknown test",
        )

        tests = spec.get(
            "tests",
            [],
        )

        for test in tests:

            statistics.total += 1

            status = test.get(
                "status"
            )

            results = test.get(
                "results",
                [],
            )

            retry_count = max(
                len(results) - 1,
                0,
            )

            if status == "expected":

                statistics.passed += 1

            elif status == "unexpected":

                statistics.failed += 1

                if (
                    len(failed_tests)
                    < max_failure_details
                ):

                    failed_tests.append(
                        TestDetail(
                            title=spec_title,
                            retry_count=retry_count,
                            error=get_error_message(
                                results
                            ),
                        )
                    )

            elif status == "skipped":

                statistics.skipped += 1

            elif status == "flaky":

                statistics.flaky += 1

                if (
                    len(flaky_tests)
                    < max_failure_details
                ):

                    flaky_tests.append(
                        TestDetail(
                            title=spec_title,
                            retry_count=retry_count,
                        )
                    )

    return TestSummary(

        summary=statistics,

        failed_tests=failed_tests,

        flaky_tests=flaky_tests,

        failed_details_truncated=(
            statistics.failed
            > len(failed_tests)
        ),

        flaky_details_truncated=(
            statistics.flaky
            > len(flaky_tests)
        ),
    )