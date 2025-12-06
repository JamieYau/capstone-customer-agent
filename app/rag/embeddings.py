from openai import OpenAI
import os
import numpy as np

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = "text-embedding-3-small"


def get_embedding(text: str) -> list[float]:
    """Return embedding vector for text."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    return resp.data[0].embedding


def batch_embeddings(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    """Compute embeddings in batches (returns list of vectors)."""
    out = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        out.extend([r.embedding for r in resp.data])
    return out


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    return float((a @ b) / denom) if denom != 0 else 0.0
