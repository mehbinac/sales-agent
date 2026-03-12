import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
# from test_groq import test_groq
from retriever import search
from logger import log_interaction

def main():

    load_dotenv()

    # Initialize Groq client
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": """You are a confident and strategic AI sales agent.

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
                }
        ]

    st.set_page_config(page_title="Groq Test App", layout="centered")
    st.title("🧪 Groq + Streamlit Test")

    user_input = st.text_area("Enter a message")

    if st.button("Send"):
        if not user_input.strip():
            st.warning("Please enter a message.")
        else:
            with st.spinner("Calling Groq..."):
                relevant_faqs, faq_scores, relevant_products, product_scores = search(user_input, top_k=1)

                faq_context = "\n".join([
                    f"Q: {faq['question']}\nA: {faq['answer']}"
                    for faq in relevant_faqs
                ])
                faq_scores_str = ", ".join([f"{score:.2f}" for score in faq_scores])
                product_context = "\n".join([
                    f"Product: {product['name']}\nCategory: {product['category']}\nPrice Range: {product['price_range']}\nDescription: {product['description']}\nFeatures: {', '.join(product['features'])}\nIdeal For: {', '.join(product['ideal_for'])}\nUse Cases: {', '.join(product['use_cases'])}"
                    for product in relevant_products
                ])
                product_scores_str = ", ".join([f"{score:.2f}" for score in product_scores])
                # Instead of appending system messages mid-conversation, create one combined context
                combined_context = f"""Relevant FAQ information:
                {faq_context}
                
                Relevant product information:
                {product_context}"""
                
                st.session_state.messages.append(
                    {"role": "user", "content": f"{combined_context}\n\nUser question: {user_input}"}
                )

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.3,
                    max_tokens=200
                )
                assistant_reply = response.choices[0].message.content
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_reply}
                )
                st.subheader("Response")
                st.write(assistant_reply)

                # Log the interaction
                log_interaction({
                    "user_input": user_input,
                    "faq_context": faq_context,
                    "faq_scores": faq_scores_str,
                    "product_context": product_context,
                    "product_scores": product_scores_str,
                    "assistant_reply": assistant_reply
                })

if __name__ == "__main__":
    main()
