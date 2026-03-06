from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return model.encode(text, normalize_embeddings=True)

from faq_data import FAQS
from product_data import PRODUCTS

faq_questions = [faq["question"] for faq in FAQS]
faq_embeddings = embed(faq_questions)

product_names = [product["name"] for product in PRODUCTS]
product_embeddings = embed(product_names)

def search(query, top_k=1, min_similarity=0.45):
    query_embedding = embed(query)

    faq_similarities = np.dot(faq_embeddings, query_embedding)  # cosine sim (normalized)
    faq_sorted_idx = faq_similarities.argsort()[::-1]

    product_similarities = np.dot(product_embeddings, query_embedding)
    product_sorted_idx = product_similarities.argsort()[::-1]

    faq_context = []
    for i in faq_sorted_idx:
        if faq_similarities[i] < min_similarity:
            break
        faq_context.append(FAQS[i])
        if len(faq_context) >= top_k:
            break

    product_context = []
    for i in product_sorted_idx:
        if product_similarities[i] < min_similarity:
            break
        product_context.append(PRODUCTS[i])
        if len(product_context) >= top_k:
            break

    return faq_context, product_context