import json

from src.qa_mcp_server.tools.playwright import (
    summarize_playwright_results,
)


REAL_REPORT = (
    "sample-data/"
    "real-playwright-report.json"
)


def test_valid_playwright_report():

    result = summarize_playwright_results(
        REAL_REPORT
    )

    summary = result["summary"]

    assert summary["total"] == 4
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["skipped"] == 1
    assert summary["flaky"] == 1

    assert (
        result["failed_tests"][0]["title"]
        == "failing test"
    )

    assert (
        result["flaky_tests"][0]["title"]
        == "flaky test"
    )


def test_empty_report_path():

    result = summarize_playwright_results(
        ""
    )

    assert (
        result["error"]
        == "Report path cannot be empty."
    )


def test_missing_report():

    path = "sample-data/missing.json"

    result = summarize_playwright_results(
        path
    )

    assert "not found" in result["error"]


def test_directory_path():

    result = summarize_playwright_results(
        "sample-data"
    )

    assert (
        "must point to a JSON file"
        in result["error"]
    )


def test_malformed_json(
    tmp_path,
):

    report = (
        tmp_path
        / "invalid.json"
    )

    report.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    result = summarize_playwright_results(
        str(report)
    )

    assert (
        "Invalid JSON"
        in result["error"]
    )


def test_invalid_playwright_schema(
    tmp_path,
):

    report = (
        tmp_path
        / "invalid-schema.json"
    )

    report.write_text(
        json.dumps(
            {
                "random": "data"
            }
        ),
        encoding="utf-8",
    )

    result = summarize_playwright_results(
        str(report)
    )

    assert (
        "missing 'suites'"
        in result["error"]
    )


def test_negative_detail_limit():

    result = summarize_playwright_results(
        REAL_REPORT,
        max_failure_details=-1,
    )

    assert (
        "cannot be negative"
        in result["error"]
    )


def test_truncation():

    result = summarize_playwright_results(
        REAL_REPORT,
        max_failure_details=0,
    )

    assert (
        result[
            "failed_details_truncated"
        ]
        is True
    )

    assert (
        result[
            "flaky_details_truncated"
        ]
        is True
    )

    assert (
        result["failed_tests"]
        == []
    )

    assert (
        result["flaky_tests"]
        == []
    )