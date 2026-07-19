from pydantic import BaseModel, Field


class TestDetail(BaseModel):
    """Details about a failed or flaky Playwright test."""

    title: str
    retry_count: int = 0
    error: str | None = None


class TestStatistics(BaseModel):
    """Execution statistics for a Playwright test run."""

    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    flaky: int = 0


class TestSummary(BaseModel):
    """Complete triage summary of a Playwright execution."""

    summary: TestStatistics = Field(default_factory=TestStatistics)

    failed_tests: list[TestDetail] = Field(default_factory=list)
    flaky_tests: list[TestDetail] = Field(default_factory=list)

    failed_details_truncated: bool = False
    flaky_details_truncated: bool = False