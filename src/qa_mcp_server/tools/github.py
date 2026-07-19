from src.qa_mcp_server.services.github_service import (
    GitHubServiceError,
    fetch_github_issues,
)


def fetch_github_defects(
    owner: str,
    repo: str,
    state: str = "open",
    label: str = "bug",
    limit: int = 20,
) -> dict:
    """
    Fetch defect issues from a GitHub repository.

    The default label is 'bug'.
    """

    try:
        result = fetch_github_issues(
            owner=owner,
            repo=repo,
            state=state,
            label=label or None,
            limit=limit,
        )

        return result.model_dump()

    except (
        ValueError,
        GitHubServiceError,
    ) as error:
        return {
            "error": str(error)
        }