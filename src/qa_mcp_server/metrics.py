from prometheus_client import Counter, Histogram

# Total MCP tool invocations
MCP_REQUESTS = Counter(
    "qa_mcp_requests_total",
    "Total number of MCP tool requests",
    ["tool"]
)

# Tool execution duration
MCP_DURATION = Histogram(
    "qa_mcp_duration_seconds",
    "Execution time of MCP tools",
    ["tool"]
)

# QA execution metrics
TESTS_PASSED = Counter(
    "qa_tests_passed_total",
    "Total passed Playwright tests"
)

TESTS_FAILED = Counter(
    "qa_tests_failed_total",
    "Total failed Playwright tests"
)

FLAKY_TESTS = Counter(
    "qa_flaky_tests_total",
    "Total flaky Playwright tests"
)