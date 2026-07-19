from mcp.server.fastmcp import FastMCP

from src.qa_mcp_server.tools.playwright import summarize_playwright_results


mcp = FastMCP("qa-mcp-server")


@mcp.tool()
def health_check() -> str:
    """Check whether the QA MCP server is running."""
    return "QA MCP Server is running successfully!"


@mcp.tool()
def playwright_test_summary(report_path: str) -> dict:
    """Summarize execution statistics from a Playwright JSON test report."""
    return summarize_playwright_results(report_path)


if __name__ == "__main__":
    mcp.run(transport="stdio")