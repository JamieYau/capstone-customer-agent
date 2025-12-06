import os
import chromadb
from chromadb.config import Settings
from app.rag.embeddings import get_embedding, cosine_similarity
import numpy as np

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
CHROMA_DIR = os.path.join(PROJECT_DIR, "..", "db", "chroma")
CHROMA_COLLECTION = "faqs"

def _get_client():
    return chromadb.PersistentClient(path=str(CHROMA_DIR))

def retrieve(query: str, top_k: int = 5, rerank: bool = True) -> str|None:
    """
    Query chroma for top_k candidates. Optionally rerank by cosine similarity
    using the embedding function (fast).
    Returns the best answer string or None.
    """
    client = _get_client()
    try:
        # Use get_or_create_collection for safety
        coll = client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"}  # Optional: specify distance metric
        )
    except Exception as e:
        # No collection or DB missing
        print("Chroma collection error:", e)
        return None

    # compute query embedding
    q_emb = get_embedding(query)

    # Query using the new API
    try:
        res = coll.query(
            query_embeddings=[q_emb],
            n_results=top_k,
            include=['metadatas', 'documents', 'distances']
        )
    except Exception as e:
        print(f"Query error: {e}")
        return None

    # Extract results
    docs = res.get('documents', [[]])
    docs = docs[0] if docs else []

    metadatas = res.get('metadatas', [[]])
    metadatas = metadatas[0] if metadatas else []

    distances = res.get('distances', [[]])
    distances = distances[0] if distances else []

    if not docs:
        return None

    # Build list of candidates with embeddings if we want rerank via cosine
    if rerank:
        # Re-rank using our own cosine similarity
        sims = []
        for meta in metadatas:
            # Use stored question from metadata for re-ranking
            question_text = meta.get('question', '')
            if not question_text:
                # Fallback to first document if no question in metadata
                continue
            doc_emb = get_embedding(question_text)
            sims.append(cosine_similarity(q_emb, doc_emb))

        if sims:
            # Pick best by similarity scores
            idx = int(np.argmax(sims))
            best_meta = metadatas[idx]
            best_doc = docs[idx]
            # Prefer stored answer in metadata if present
            return best_meta.get("answer") or best_doc
        else:
            # Fallback to first result
            best_meta = metadatas[0] if metadatas else {}
            best_doc = docs[0] if docs else ""
            return best_meta.get("answer") or best_doc
    else:
        # No re-ranking: return top-1 result
        best_meta = metadatas[0] if metadatas else {}
        best_doc = docs[0] if docs else ""
        return best_meta.get("answer") or best_doc
