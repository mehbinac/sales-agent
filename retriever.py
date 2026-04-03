from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return model.encode(text, normalize_embeddings=True)

import json

with open("data/faq_data.json", "r") as f:
    FAQS = json.load(f)
faq_questions = [faq["question"] for faq in FAQS]
faq_texts = [f"{faq['question']} {faq['answer']}" for faq in FAQS]
faq_embeddings = np.array([embed(text) for text in faq_texts])

with open("data/product_data.json", "r") as f:
    PRODUCTS = json.load(f)
product_names = [product["name"] for product in PRODUCTS]
product_texts = [
    f"""
    Product Name: {product['name']}
    Category: {product['category']}
    Price Range: {product['price_range']}
    Ideal For: {', '.join(product['ideal_for'])}
    Use Cases: {', '.join(product['use_cases'])}
    Features: {', '.join(product['features'])}
    Description: {product['description']}
    """
    for product in PRODUCTS
]
product_embeddings = np.array([embed(text) for text in product_texts])

def search(query, top_k=1, min_similarity=0.45):
    query_embedding = embed(query)

    faq_similarities = np.dot(faq_embeddings, query_embedding)  # cosine sim (normalized)
    faq_sorted_idx = faq_similarities.argsort()[::-1]

    product_similarities = np.dot(product_embeddings, query_embedding)
    product_sorted_idx = product_similarities.argsort()[::-1]

    faq_context = []
    faq_scores = []
    for i in faq_sorted_idx:
        if faq_similarities[i] < min_similarity:
            break
        faq_context.append(FAQS[i])
        faq_scores.append(faq_similarities[i])
        if len(faq_context) >= top_k:
            break

    product_context = []
    product_scores = []
    for i in product_sorted_idx:
        if product_similarities[i] < min_similarity:
            break
        product_context.append(PRODUCTS[i])
        product_scores.append(product_similarities[i])
        if len(product_context) >= top_k:
            break

    return faq_context, faq_scores, product_context, product_scores