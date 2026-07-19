from pydantic import BaseModel, Field


class GitHubIssue(BaseModel):
    """A concise GitHub defect representation."""

    number: int
    title: str
    state: str
    labels: list[str] = Field(default_factory=list)
    url: str


class GitHubIssueResult(BaseModel):
    """Result returned by the GitHub defect fetcher."""

    repository: str
    total_returned: int
    issues: list[GitHubIssue] = Field(default_factory=list)