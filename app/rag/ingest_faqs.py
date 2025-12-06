import os
import json

import chromadb
from app.rag.embeddings import batch_embeddings

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(PROJECT_DIR, "data", "faqs.json")
CHROMA_DIR = os.path.join(PROJECT_DIR, "..", "db", "chroma")  # project-root/db/chroma

def ingest():
    # Create directory if needed
    os.makedirs(CHROMA_DIR, exist_ok=True)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Create or get collection
    collection = client.get_or_create_collection(
        name="faqs",
        metadata={"source": "faqs"}
    )

    # Load faqs.json
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        faqs = json.load(f)

    texts = [f"{q['question']}\n\n{q.get('answer','')}" for q in faqs]
    ids = [f"faq-{i}" for i in range(len(faqs))]
    metadatas = [{"question": q["question"], "answer": q.get("answer","")} for q in faqs]

    # Compute embeddings (batched)
    print("Computing embeddings (OpenAI)...")
    vectors = batch_embeddings(texts, batch_size=16)

    # Upsert into chroma
    print(f"Upserting {len(texts)} FAQ vectors into Chroma at {CHROMA_DIR} ...")
    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=vectors
    )

    print("Ingestion complete.")


if __name__ == "__main__":
    ingest()
