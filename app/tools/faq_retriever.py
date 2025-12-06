from app.rag.retriever import retrieve

def retrieve_faq_answer(user_query: str) -> str:
    # try RAG
    ans = retrieve(user_query, top_k=5, rerank=True)
    if not ans:
        return "Sorry, I don't know that. Try rephrasing your question or contact support."
    return ans
