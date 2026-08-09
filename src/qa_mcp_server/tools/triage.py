from src.qa_mcp_server.tools.github import fetch_github_defects
from src.qa_mcp_server.tools.rag import find_similar_defects


def triage_failure(
    failure_text: str,
    github_owner: str,
    github_repo: str,
    top_k: int = 3,
) -> dict:
    """
    Perform consolidated QA failure triage.

    Combines:
    - Current Playwright failure context
    - Live GitHub defects
    - Semantically similar historical defects
    """

    if not failure_text or not failure_text.strip():
        return {
            "error": "failure_text cannot be empty."
        }

    # Fetch currently open GitHub defects
    github_defects = fetch_github_defects(
        owner=github_owner,
        repo=github_repo,
        state="open",
        label="bug",
        limit=20,
    )

    # Search historical defects using BGE + ChromaDB
    similar_defects = find_similar_defects(
        failure_text=failure_text,
        top_k=top_k,
    )

    return {
        "failure": {
            "text": failure_text,
        },
        "live_defects": github_defects,
        "similar_historical_defects": similar_defects,
        "triage_metadata": {
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "vector_store": "ChromaDB",
            "top_k": top_k,
        },
    }