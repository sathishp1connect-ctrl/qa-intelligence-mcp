from mcp.server.fastmcp import FastMCP

from src.qa_mcp_server.tools.github import fetch_github_defects
from src.qa_mcp_server.tools.playwright import summarize_playwright_results
from src.qa_mcp_server.tools.rag import (
    find_similar_defects,
    ingest_defects,
)
from src.qa_mcp_server.tools.triage import triage_failure
from src.qa_mcp_server.tools.report_analyzer import analyze_merged_report


# Create the MCP server
# Bind to all network interfaces so Kubernetes Service traffic can reach it.
mcp = FastMCP(
    "qa-intelligence-mcp",
    host="0.0.0.0",
    port=8000,
)


@mcp.tool()
def health_check() -> str:
    """Check whether the QA Intelligence MCP server is running."""
    return "QA Intelligence MCP Server is running successfully!"


@mcp.tool()
def playwright_test_summary(
    report_path: str,
    max_failure_details: int = 20,
) -> dict:
    """
    Analyze and summarize a Playwright JSON test report.

    Returns execution statistics and bounded details
    about failed and flaky tests.
    """
    return summarize_playwright_results(
        report_path=report_path,
        max_failure_details=max_failure_details,
    )


@mcp.tool()
def github_defect_fetcher(
    owner: str,
    repo: str,
    state: str = "open",
    label: str = "bug",
    limit: int = 20,
) -> dict:
    """
    Fetch defect issues from a GitHub repository.
    """
    return fetch_github_defects(
        owner=owner,
        repo=repo,
        state=state,
        label=label,
        limit=limit,
    )


@mcp.tool()
def ingest_historical_defects() -> dict:
    """
    Ingest historical defect data into ChromaDB.
    """
    return ingest_defects()


@mcp.tool()
def similar_defect_search(
    failure_text: str,
    top_k: int = 3,
) -> dict:
    """
    Find historical defects semantically similar to a test failure.
    """
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
    """
    Perform intelligent test failure triage using
    GitHub + ChromaDB + RAG.
    """
    return triage_failure(
        failure_text=failure_text,
        github_owner=github_owner,
        github_repo=github_repo,
        top_k=top_k,
    )


@mcp.tool()
def regression_execution_summary() -> dict:
    """
    Generate an executive QA summary from the merged
    distributed Playwright execution report.
    """
    return analyze_merged_report()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")