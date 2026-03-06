import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
# from test_groq import test_groq
from retriever import search

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
                relevant_faqs, relevant_products = search(user_input, top_k=1)

                faq_context = "\n".join([
                    f"Q: {faq['question']}\nA: {faq['answer']}"
                    for faq in relevant_faqs
                ])
                product_context = "\n".join([
                    f"Product: {product['name']}\nDescription: {product['description']}"
                    for product in relevant_products
                ])
                st.session_state.messages.append(
                    {"role": "system", "content": f"Relevant FAQ information:\n{faq_context}"},
                )
                st.session_state.messages.append(
                    {"role": "system", "content": f"Relevant product information:\n{product_context}"},
                )
                st.session_state.messages.append(
                    {"role": "user", "content": user_input}
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

if __name__ == "__main__":
    main()
