from mcp.server.fastmcp import FastMCP
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from src.qa_mcp_server.metrics import (
    MCP_REQUESTS,
    MCP_DURATION,
    TESTS_PASSED,
    TESTS_FAILED,
    FLAKY_TESTS,
)

from src.qa_mcp_server.tools.github import fetch_github_defects
from src.qa_mcp_server.tools.playwright import summarize_playwright_results
from src.qa_mcp_server.tools.rag import (
    find_similar_defects,
    ingest_defects,
)
from src.qa_mcp_server.tools.triage import triage_failure
from src.qa_mcp_server.tools.report_analyzer import analyze_merged_report

from aggregator.qa_summary import generate_summary


# -----------------------------------
# MCP Server
# -----------------------------------

mcp = FastMCP(
    "qa-intelligence-mcp",
    host="0.0.0.0",
    port=8000,
)

# -----------------------------------
# Initialize Prometheus label series
# (Fixes "No Data" in Grafana)
# -----------------------------------

for tool in [
    "health_check",
    "playwright_test_summary",
    "github_defect_fetcher",
    "ingest_historical_defects",
    "similar_defect_search",
    "triage_test_failure",
    "regression_execution_summary",
    "get_qa_summary",
]:
    MCP_REQUESTS.labels(tool=tool)
    MCP_DURATION.labels(tool=tool)


# -----------------------------------
# Metrics Endpoint
# -----------------------------------

@mcp.custom_route("/metrics", methods=["GET"])
async def metrics(request):
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


# -----------------------------------
# MCP Tools
# -----------------------------------

@mcp.tool()
def health_check() -> str:
    """Check whether the MCP server is running."""

    MCP_REQUESTS.labels(tool="health_check").inc()

    with MCP_DURATION.labels(tool="health_check").time():
        return "QA Intelligence MCP Server is running successfully!"


@mcp.tool()
def playwright_test_summary(
    report_path: str,
    max_failure_details: int = 20,
) -> dict:
    """Summarize Playwright JSON report."""

    MCP_REQUESTS.labels(tool="playwright_test_summary").inc()

    with MCP_DURATION.labels(tool="playwright_test_summary").time():

        result = summarize_playwright_results(
            report_path=report_path,
            max_failure_details=max_failure_details,
        )

        TESTS_PASSED.inc(result.get("passed", 0))
        TESTS_FAILED.inc(result.get("failed", 0))
        FLAKY_TESTS.inc(result.get("flaky", 0))

        return result


@mcp.tool()
def github_defect_fetcher(
    owner: str,
    repo: str,
    state: str = "open",
    label: str = "bug",
    limit: int = 20,
) -> dict:
    """Fetch GitHub defects."""

    MCP_REQUESTS.labels(tool="github_defect_fetcher").inc()

    with MCP_DURATION.labels(tool="github_defect_fetcher").time():
        return fetch_github_defects(
            owner=owner,
            repo=repo,
            state=state,
            label=label,
            limit=limit,
        )


@mcp.tool()
def ingest_historical_defects() -> dict:
    """Load historical defects into ChromaDB."""

    MCP_REQUESTS.labels(tool="ingest_historical_defects").inc()

    with MCP_DURATION.labels(tool="ingest_historical_defects").time():
        return ingest_defects()


@mcp.tool()
def similar_defect_search(
    failure_text: str,
    top_k: int = 3,
) -> dict:
    """Semantic similarity search."""

    MCP_REQUESTS.labels(tool="similar_defect_search").inc()

    with MCP_DURATION.labels(tool="similar_defect_search").time():
        return find_similar_defects(
            failure_text=failure_text,
            top_k=top_k,
        )


@mcp.tool()
def triage_test_failure(
    failure_text: str,
    github_owner: str,
    github_repo: str,
    top_k: int = 3,
) -> dict:
    """AI-powered intelligent failure triage."""

    MCP_REQUESTS.labels(tool="triage_test_failure").inc()

    with MCP_DURATION.labels(tool="triage_test_failure").time():
        return triage_failure(
            failure_text=failure_text,
            github_owner=github_owner,
            github_repo=github_repo,
            top_k=top_k,
        )


@mcp.tool()
def regression_execution_summary() -> dict:
    """Distributed Playwright executive summary."""

    MCP_REQUESTS.labels(tool="regression_execution_summary").inc()

    with MCP_DURATION.labels(tool="regression_execution_summary").time():
        return analyze_merged_report()


@mcp.tool()
def get_qa_summary() -> dict:
    """Executive QA Summary."""

    MCP_REQUESTS.labels(tool="get_qa_summary").inc()

    with MCP_DURATION.labels(tool="get_qa_summary").time():
        return generate_summary()


# -----------------------------------
# Start HTTP MCP Server
# -----------------------------------

if __name__ == "__main__":
    mcp.run(transport="streamable-http")