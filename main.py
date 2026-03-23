import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

from retriever import search
from logger import log_interaction

load_dotenv()

app = FastAPI()

client = Groq(api_key=os.environ["GROQ_API_KEY"])


class ChatRequest(BaseModel):
    message: str
    history: list = []


class ChatResponse(BaseModel):
    response: str
    updated_history: list


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_input = req.message
    history = req.history

    # Retrieve top semantic matches from FAQ and product catalogs.
    relevant_faqs, faq_scores, relevant_products, product_scores = search(user_input, top_k=1)

    faq_context = "\n".join([
        f"Q: {faq['question']}\nA: {faq['answer']}"
        for faq in relevant_faqs
    ])
    faq_scores_str = ", ".join([f"{score:.2f}" for score in faq_scores])

    product_context = "\n".join([
        f"Product: {product['name']}\n"
        f"Category: {product['category']}\n"
        f"Price Range: {product['price_range']}\n"
        f"Description: {product['description']}\n"
        f"Features: {', '.join(product['features'])}\n"
        f"Ideal For: {', '.join(product['ideal_for'])}\n"
        f"Use Cases: {', '.join(product['use_cases'])}"
        for product in relevant_products
    ])
    product_scores_str = ", ".join([f"{score:.2f}" for score in product_scores])

    combined_context = f"""Relevant FAQ information:
        {faq_context}

        Relevant product information:
        {product_context}
        """

    messages = history.copy()

    if not messages:
        messages.append({
            "role": "system",
            "content": """You are a confident and strategic AI sales agent.
    `
            Your job is not just to answer questions, but to actively guide the customer toward a clear decision.

            You should:
            - Lead the conversation, not just react.
            - Narrow options quickly.
            - Ask one purposeful question that moves closer to a recommendation.
            - When enough context is available, confidently recommend a specific solution and explain why it is the best fit.

            Keep your tone natural and conversational.
            Avoid sounding scripted or overly formal.
            Do not generate customer responses.
            """
        })

    # Inject retrieved context into the user turn sent to the model.
    messages.append({
        "role": "user",
        "content": f"{combined_context}\n\nUser question: {user_input}"
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        max_tokens=200
    )

    assistant_reply = response.choices[0].message.content

    # Return assistant reply and keep full thread for multi-turn chat.
    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    log_interaction({
        "user_input": user_input,
        "faq_context": faq_context,
        "faq_scores": faq_scores_str,
        "product_context": product_context,
        "product_scores": product_scores_str,
        "assistant_reply": assistant_reply
    })

    return ChatResponse(
        response=assistant_reply,
        updated_history=messages
    )