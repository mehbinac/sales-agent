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


# Request schema
class ChatRequest(BaseModel):
    message: str
    history: list = []


# Response schema
class ChatResponse(BaseModel):
    response: str
    updated_history: list


# API endpoint that handles chat requests from frontend
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Extract user message and conversation history from request
    user_input = req.message
    history = req.history

    # Step 1: Retrieve relevant FAQs and products using semantic search
    # search() returns top_k matches with similarity scores for each
    relevant_faqs, faq_scores, relevant_products, product_scores = search(user_input, top_k=1)

    # Format FAQs into readable string for LLM context
    faq_context = "\n".join([
        f"Q: {faq['question']}\nA: {faq['answer']}"
        for faq in relevant_faqs
    ])
    # Convert similarity scores to formatted strings for logging
    faq_scores_str = ", ".join([f"{score:.2f}" for score in faq_scores])

    # Format products into detailed context string with all relevant attributes
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
    # Convert product scores to formatted strings for logging
    product_scores_str = ", ".join([f"{score:.2f}" for score in product_scores])

    # Combine FAQ and product information into single context prompt for LLM
    combined_context = f"""Relevant FAQ information:
        {faq_context}

        Relevant product information:
        {product_context}
        """

    # Step 2: Build message thread for LLM
    # Create a copy of history to avoid mutating frontend's state
    messages = history.copy()

    # Add system message only on first request (when history is empty)
    # Subsequent requests will already have it from previous response
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

    # Add user message with retrieved context to message thread
    # Context includes relevant FAQs and products to help LLM make informed recommendations
    messages.append({
        "role": "user",
        "content": f"{combined_context}\n\nUser question: {user_input}"
    })

    # Step 3: Call Groq API with the complete message thread
    # temperature=0.3 keeps responses focused and deterministic (lower = more deterministic)
    # max_tokens=200 limits response length for concise recommendations
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        max_tokens=200
    )

    # Extract the LLM response
    assistant_reply = response.choices[0].message.content

    # Add assistant response to message thread for next multi-turn request
    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    # Step 4: Log interaction to JSON file for monitoring and debugging
    log_interaction({
        "user_input": user_input,
        "faq_context": faq_context,
        "faq_scores": faq_scores_str,
        "product_context": product_context,
        "product_scores": product_scores_str,
        "assistant_reply": assistant_reply
    })

    # Return LLM response and updated message history to frontend
    # Frontend stores updated_history for next request to maintain conversation context
    return ChatResponse(
        response=assistant_reply,
        updated_history=messages
    )