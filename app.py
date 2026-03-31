import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/chat")

st.set_page_config(page_title="AI Sales Agent", layout="centered")
st.title("🤖 AI Sales Agent")

# Full thread used by backend for context continuity.
if "history" not in st.session_state:
    st.session_state.history = []

# UI-only messages (keeps system prompt hidden from chat view).
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

for msg in st.session_state.chat_display:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_display.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Send user query plus current history to backend.
    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL,
            json={
                "message": user_input,
                "history": st.session_state.history
            }
        )

    if response.status_code == 200:
        data = response.json()
        reply = data["response"]

        # Persist backend-updated thread for the next turn.
        st.session_state.history = data["updated_history"]

        st.session_state.chat_display.append({
            "role": "assistant",
            "content": reply
        })

        with st.chat_message("assistant"):
            st.write(reply)

    else:
        st.error("Error connecting to backend")
