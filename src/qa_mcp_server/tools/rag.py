from src.qa_mcp_server.services.chroma_service import (
    ChromaServiceError,
)
from src.qa_mcp_server.services.rag_service import (
    ingest_historical_defects,
    search_similar_defects,
)


def ingest_defects() -> dict:
    """Ingest historical defects into the vector database."""

    try:
        return ingest_historical_defects()

    except ChromaServiceError as error:
        return {
            "error": str(error)
        }


def find_similar_defects(
    failure_text: str,
    top_k: int = 3,
) -> dict:
    """Find historical defects similar to a test failure."""

    try:
        return search_similar_defects(
            failure_text=failure_text,
            top_k=top_k,
        )

    except ChromaServiceError as error:
        return {
            "error": str(error)
        }