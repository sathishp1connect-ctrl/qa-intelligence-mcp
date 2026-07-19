from src.qa_mcp_server.services.chroma_service import (
    add_defects,
    query_defects,
)
from src.qa_mcp_server.services.embedding_service import (
    generate_embedding,
)


HISTORICAL_DEFECTS = [
    {
        "id": "DEFECT-001",
        "title": "Login fails when invalid credentials are submitted",
        "description": (
            "Login test fails when a user submits invalid username "
            "or password. Expected invalid credentials error message "
            "but application returns an unexpected error."
        ),
        "component": "authentication",
    },
    {
        "id": "DEFECT-002",
        "title": "Checkout payment fails",
        "description": (
            "Checkout test fails while processing credit card payment. "
            "Payment gateway returns an unexpected server error."
        ),
        "component": "checkout",
    },
    {
        "id": "DEFECT-003",
        "title": "Search returns empty results",
        "description": (
            "Product search returns no results for valid product names "
            "even though matching products exist."
        ),
        "component": "search",
    },
    {
        "id": "DEFECT-004",
        "title": "Session expires immediately after login",
        "description": (
            "User successfully logs in but is redirected back to the "
            "login page because the authentication session expires."
        ),
        "component": "authentication",
    },
]


def ingest_historical_defects() -> dict:
    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for defect in HISTORICAL_DEFECTS:
        document = (
            f"{defect['title']}. "
            f"{defect['description']}"
        )

        ids.append(defect["id"])
        documents.append(document)
        embeddings.append(generate_embedding(document))

        metadatas.append(
            {
                "defect_id": defect["id"],
                "title": defect["title"],
                "component": defect["component"],
            }
        )

    add_defects(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return {
        "status": "success",
        "ingested": len(ids),
    }


def search_similar_defects(
    failure_text: str,
    top_k: int = 3,
) -> dict:
    if not failure_text.strip():
        return {
            "error": "Failure text cannot be empty."
        }

    if top_k < 1 or top_k > 10:
        return {
            "error": "top_k must be between 1 and 10."
        }

    embedding = generate_embedding(failure_text)

    result = query_defects(
        embedding=embedding,
        top_k=top_k,
    )

    matches = []

    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    for defect_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        similarity = max(
            0.0,
            min(1.0, 1.0 - (distance / 2.0)),
        )

        matches.append(
            {
                "id": defect_id,
                "title": metadata.get("title"),
                "component": metadata.get("component"),
                "similarity": round(similarity, 4),
                "document": document,
            }
        )

    return {
        "query": failure_text,
        "total_matches": len(matches),
        "matches": matches,
    }