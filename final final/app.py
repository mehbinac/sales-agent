import streamlit as st
import requests

# Backend API endpoint for chat requests
API_URL = "http://127.0.0.1:8000/chat"

# Configure Streamlit page settings
st.set_page_config(page_title="AI Sales Agent", layout="centered")
st.title("🤖 AI Sales Agent")

# Initialize conversation history (stores full message thread with system message, user queries, assistant responses)
# This is sent to backend to maintain multi-turn context
if "history" not in st.session_state:
    st.session_state.history = []

# Initialize chat display list (stores only user and assistant messages for UI rendering)
# Separate from history to avoid showing system message in chat interface
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

# Render all previous messages in the chat interface
for msg in st.session_state.chat_display:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get user input from chat input box
user_input = st.chat_input("Type your message...")

# Process new user message
if user_input:
    # Add user message to display list (for UI rendering)
    st.session_state.chat_display.append({
        "role": "user",
        "content": user_input
    })

    # Display user message in chat bubble
    with st.chat_message("user"):
        st.write(user_input)

    # Send request to FastAPI backend with spinner for UX feedback
    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL,
            json={
                "message": user_input,
                "history": st.session_state.history
            }
        )

    # Handle successful API response
    if response.status_code == 200:
        data = response.json()
        # Extract LLM response from backend
        reply = data["response"]

        # Update conversation history with backend's version (includes system message and full context)
        # This persists for next request to maintain multi-turn context
        st.session_state.history = data["updated_history"]

        # Add assistant response to display list (for UI rendering)
        st.session_state.chat_display.append({
            "role": "assistant",
            "content": reply
        })

        # Display assistant message in chat bubble
        with st.chat_message("assistant"):
            st.write(reply)

    # Handle API connection errors
    else:
        st.error("Error connecting to backend")
