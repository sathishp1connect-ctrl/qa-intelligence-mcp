import hashlib
import math
import re


EMBEDDING_DIMENSION = 384


def generate_embedding(text: str) -> list[float]:
    """
    Generate a deterministic local embedding.

    This lightweight provider has no ML/native dependencies and is intended
    for local development. It can later be replaced by a production embedding
    provider without changing the vector-store or MCP layers.
    """
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    vector = [0.0] * EMBEDDING_DIMENSION

    tokens = re.findall(r"[a-z0-9]+", text.lower())

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()

        index = int.from_bytes(digest[:4], "big") % EMBEDDING_DIMENSION
        sign = 1.0 if digest[4] % 2 == 0 else -1.0

        vector[index] += sign

    magnitude = math.sqrt(sum(value * value for value in vector))

    if magnitude > 0:
        vector = [value / magnitude for value in vector]

    return vector