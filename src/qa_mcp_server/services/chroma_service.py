import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CHROMA_URL = "http://localhost:8000"
TENANT = "default_tenant"
DATABASE = "default_database"
COLLECTION_NAME = "historical_defects"


class ChromaServiceError(Exception):
    """Raised when communication with ChromaDB fails."""


def _request(
    method: str,
    path: str,
    payload: dict | None = None,
):
    url = f"{CHROMA_URL}{path}"

    data = None

    headers = {
        "Content-Type": "application/json",
    }

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = Request(
        url=url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urlopen(request, timeout=15) as response:
            content = response.read().decode("utf-8")

            if not content:
                return None

            return json.loads(content)

    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")

        raise ChromaServiceError(
            f"ChromaDB HTTP {error.code}: {body}"
        ) from error

    except URLError as error:
        raise ChromaServiceError(
            f"Unable to connect to ChromaDB: {error.reason}"
        ) from error


def get_or_create_collection() -> str:
    path = (
        f"/api/v2/tenants/{TENANT}"
        f"/databases/{DATABASE}/collections"
    )

    result = _request(
        "POST",
        path,
        {
            "name": COLLECTION_NAME,
            "get_or_create": True,
        },
    )

    return result["id"]


def add_defects(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
) -> None:
    collection_id = get_or_create_collection()

    path = (
        f"/api/v2/tenants/{TENANT}"
        f"/databases/{DATABASE}"
        f"/collections/{collection_id}/upsert"
    )

    _request(
        "POST",
        path,
        {
            "ids": ids,
            "documents": documents,
            "embeddings": embeddings,
            "metadatas": metadatas,
        },
    )


def query_defects(
    embedding: list[float],
    top_k: int = 3,
) -> dict:
    collection_id = get_or_create_collection()

    path = (
        f"/api/v2/tenants/{TENANT}"
        f"/databases/{DATABASE}"
        f"/collections/{collection_id}/query"
    )

    return _request(
        "POST",
        path,
        {
            "query_embeddings": [embedding],
            "n_results": top_k,
            "include": [
                "documents",
                "metadatas",
                "distances",
            ],
        },
    )