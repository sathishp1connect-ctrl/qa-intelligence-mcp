from unittest.mock import patch

from src.qa_mcp_server.models.github_issue import (
    GitHubIssue,
    GitHubIssueResult,
)
from src.qa_mcp_server.tools.github import (
    fetch_github_defects,
)


@patch(
    "src.qa_mcp_server.tools.github."
    "fetch_github_issues"
)
def test_fetch_github_defects(
    mock_fetch,
):

    mock_fetch.return_value = GitHubIssueResult(
        repository=(
            "sathishp1connect-ctrl/"
            "qa-intelligence-mcp"
        ),
        total_returned=1,
        issues=[
            GitHubIssue(
                number=1,
                title="Login test fails",
                state="open",
                labels=["bug"],
                url=(
                    "https://github.com/"
                    "example/repo/issues/1"
                ),
            )
        ],
    )

    result = fetch_github_defects(
        owner="sathishp1connect-ctrl",
        repo="qa-intelligence-mcp",
    )

    assert result["total_returned"] == 1
    assert (
        result["issues"][0]["title"]
        == "Login test fails"
    )


def test_invalid_state():

    result = fetch_github_defects(
        owner="owner",
        repo="repo",
        state="invalid",
    )

    assert (
        "State must be"
        in result["error"]
    )


def test_invalid_limit():

    result = fetch_github_defects(
        owner="owner",
        repo="repo",
        limit=101,
    )

    assert (
        "Limit must be"
        in result["error"]
    )