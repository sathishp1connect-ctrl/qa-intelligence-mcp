from mcp.server.fastmcp import FastMCP

from src.qa_mcp_server.tools.github import fetch_github_defects
from src.qa_mcp_server.tools.playwright import summarize_playwright_results
from src.qa_mcp_server.tools.rag import (
    find_similar_defects,
    ingest_defects,
)
from src.qa_mcp_server.tools.triage import triage_failure


# Create the MCP server
mcp = FastMCP("qa-intelligence-mcp")


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

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
        state: Issue state: open, closed, or all.
        label: Issue label to filter by.
        limit: Maximum number of issues to fetch.
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

    Generates semantic embeddings and stores historical
    defects in the ChromaDB vector database.
    """
    return ingest_defects()


@mcp.tool()
def similar_defect_search(
    failure_text: str,
    top_k: int = 3,
) -> dict:
    """
    Find historical defects semantically similar to a test failure.

    Args:
        failure_text: Playwright failure or error text to search for.
        top_k: Maximum number of similar defects to return.
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
    Perform intelligent test failure triage.

    Combines:
    - Test failure context
    - Live GitHub defects
    - Semantically similar historical defects from ChromaDB

    Args:
        failure_text: Playwright test failure or error text.
        github_owner: GitHub repository owner.
        github_repo: GitHub repository name.
        top_k: Maximum number of similar historical defects to return.
    """
    return triage_failure(
        failure_text=failure_text,
        github_owner=github_owner,
        github_repo=github_repo,
        top_k=top_k,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")