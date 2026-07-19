import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.qa_mcp_server.models.github_issue import (
    GitHubIssue,
    GitHubIssueResult,
)


GITHUB_API_URL = "https://api.github.com"


class GitHubServiceError(Exception):
    """Raised when communication with GitHub fails."""


def fetch_github_issues(
    owner: str,
    repo: str,
    state: str = "open",
    label: str | None = None,
    limit: int = 20,
) -> GitHubIssueResult:
    """Fetch repository issues from GitHub."""

    if not owner.strip():
        raise ValueError("GitHub owner cannot be empty.")

    if not repo.strip():
        raise ValueError("GitHub repository cannot be empty.")

    if state not in {"open", "closed", "all"}:
        raise ValueError(
            "State must be 'open', 'closed', or 'all'."
        )

    if limit < 1 or limit > 100:
        raise ValueError(
            "Limit must be between 1 and 100."
        )

    query = {
        "state": state,
        "per_page": limit,
        "sort": "updated",
        "direction": "desc",
    }

    if label:
        query["labels"] = label

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/issues?"
        f"{urlencode(query)}"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "qa-intelligence-mcp",
    }

    token = os.getenv("GITHUB_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(
        url,
        headers=headers,
        method="GET",
    )

    try:
        with urlopen(
            request,
            timeout=15,
        ) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

    except HTTPError as error:
        if error.code == 404:
            raise GitHubServiceError(
                f"GitHub repository not found: "
                f"{owner}/{repo}"
            ) from error

        if error.code == 403:
            raise GitHubServiceError(
                "GitHub API request forbidden or "
                "rate limit exceeded."
            ) from error

        raise GitHubServiceError(
            f"GitHub API returned HTTP {error.code}."
        ) from error

    except URLError as error:
        raise GitHubServiceError(
            f"Unable to connect to GitHub: "
            f"{error.reason}"
        ) from error

    except TimeoutError as error:
        raise GitHubServiceError(
            "GitHub API request timed out."
        ) from error

    issues = []

    for item in data:

        # GitHub's Issues API can also return pull requests.
        if "pull_request" in item:
            continue

        labels = [
            label_data["name"]
            for label_data in item.get("labels", [])
            if "name" in label_data
        ]

        issues.append(
            GitHubIssue(
                number=item["number"],
                title=item["title"],
                state=item["state"],
                labels=labels,
                url=item["html_url"],
            )
        )

    return GitHubIssueResult(
        repository=f"{owner}/{repo}",
        total_returned=len(issues),
        issues=issues,
    )