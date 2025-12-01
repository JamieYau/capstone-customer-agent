from openai import OpenAI
from app.config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

# Simple embedding function
def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Used for queries
def embed_query(query: str):
    return get_embedding(query)

# Simple dot product similarity between vectors
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = sum(a * a for a in vec1) ** 0.5
    mag2 = sum(b * b for b in vec2) ** 0.5
    return dot / (mag1 * mag2)

# Embed FAQ question and compare with query embedding
def embed_docs(faq_question: str, query_embedding):
    doc_embedding = get_embedding(faq_question)
    return cosine_similarity(doc_embedding, query_embedding)
