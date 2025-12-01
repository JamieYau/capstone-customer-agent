import json
from app.utils.embeddings import embed_query, embed_docs

def load_faqs():
    with open("app/data/faqs.json", "r") as f:
        return json.load(f)

def retrieve_faq_answer(user_query):
    faqs = load_faqs()
    query_vec = embed_query(user_query)

    best_match = None
    best_score = -1

    for faq in faqs:
        score = embed_docs(faq["question"], query_vec)
        if score > best_score:
            best_score = score
            best_match = faq

    return best_match["answer"] if best_match else "Sorry, I don't know that."
