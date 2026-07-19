import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


EMBEDDING_URL = "http://localhost:8080/embed"


class EmbeddingServiceError(Exception):
    """Raised when the embedding service cannot generate an embedding."""


def generate_embedding(text: str) -> list[float]:
    """
    Generate a semantic embedding using the local BGE embedding model
    served by Hugging Face Text Embeddings Inference (TEI).
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    payload = json.dumps(
        {
            "inputs": [text.strip()]
        }
    ).encode("utf-8")

    request = Request(
        url=EMBEDDING_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

    except HTTPError as error:
        body = error.read().decode(
            "utf-8",
            errors="replace",
        )

        raise EmbeddingServiceError(
            f"Embedding service HTTP {error.code}: {body}"
        ) from error

    except URLError as error:
        raise EmbeddingServiceError(
            f"Unable to connect to embedding service: {error.reason}"
        ) from error

    if not result or not isinstance(result, list):
        raise EmbeddingServiceError(
            "Embedding service returned an invalid response."
        )

    embedding = result[0]

    if not isinstance(embedding, list):
        raise EmbeddingServiceError(
            "Embedding service returned an invalid embedding."
        )

    return embedding