from app.rag.retriever import retrieve

if __name__ == "__main__":
    queries = [
        "What is your refund policy?",
        "How long does delivery take?",
        "Do you deliver internationally?",
        "Can I cancel my order?",
        "What payment methods do you accept?"
    ]
    for q in queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {q}")
        answer = retrieve(q, top_k=3, rerank=True)
        print(f"Answer: {answer}")
        print(f"{'=' * 60}")
