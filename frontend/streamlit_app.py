import streamlit as st
import requests
from typing import List, Dict
import json

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="E-commerce Sales Agent",
    page_icon="🛒",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'products' not in st.session_state:
    st.session_state.products = []


def call_api(endpoint: str, method: str = "GET", data: dict = None):
    """Call the API"""
    try:
        url = f"{API_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None


def display_product(product: dict):
    """Display a product card"""
    with st.container():
        st.markdown(f"### {product['name']}")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Category:** {product['category']}")
            st.write(f"**Description:** {product['description']}")
            st.write(f"**Features:**")
            for feature in product['features']:
                st.write(f"  • {feature}")
        
        with col2:
            st.markdown(f"## ${product['price']:.2f}")
            st.write(f"⭐ Rating: {product['rating']}/5")
            st.write(f"📦 Stock: {product['stock']}")
        
        st.divider()


def main():
    st.title("🛒 E-commerce Sales Agent")
    st.markdown("Welcome! I'm your AI shopping assistant. How can I help you today?")
    
    # Sidebar
    with st.sidebar:
        st.header("Features")
        
        # Product Browser
        with st.expander("📦 Browse Products", expanded=False):
            if st.button("Load All Products"):
                products = call_api("/products")
                if products:
                    st.session_state.products = products
            
            if st.session_state.products:
                st.write(f"Showing {len(st.session_state.products)} products")
                
                # Category filter
                categories = call_api("/categories")
                if categories:
                    category = st.selectbox("Filter by Category", ["All"] + categories)
                    if category != "All":
                        filtered = [p for p in st.session_state.products if p['category'] == category]
                    else:
                        filtered = st.session_state.products
                    
                    for product in filtered[:5]:
                        st.markdown(f"**{product['name']}** - ${product['price']}")
        
        # Search
        with st.expander("🔍 Search Products", expanded=False):
            search_query = st.text_input("Search for products")
            if st.button("Search") and search_query:
                result = call_api("/products/search", "POST", {"query": search_query})
                if result:
                    st.session_state.products = result
                    st.success(f"Found {len(result)} products")
        
        # FAQ
        with st.expander("❓ FAQs", expanded=False):
            faqs = call_api("/faqs")
            if faqs:
                for faq in faqs[:5]:
                    st.markdown(f"**Q: {faq['question']}**")
                    st.markdown(f"A: {faq['answer']}")
                    st.divider()
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat with Sales Agent")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Display associated products
            if "products" in message and message["products"]:
                st.markdown("**Relevant Products:**")
                for product in message["products"]:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**{product['name']}**")
                            st.caption(product['description'][:100] + "...")
                        with col2:
                            st.write(f"${product['price']}")
                        with col3:
                            st.write(f"⭐ {product['rating']}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about our products..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = call_api(
                    "/chat",
                    "POST",
                    {
                        "message": prompt,
                        "conversation_history": [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages[-5:]
                        ]
                    }
                )
                
                if response:
                    st.write(response["response"])
                    
                    # Store and display products
                    message_data = {
                        "role": "assistant",
                        "content": response["response"]
                    }
                    
                    if response.get("products"):
                        message_data["products"] = response["products"]
                        st.markdown("**Relevant Products:**")
                        for product in response["products"]:
                            with st.container():
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.write(f"**{product['name']}**")
                                    st.caption(product['description'][:100] + "...")
                                with col2:
                                    st.write(f"${product['price']}")
                                with col3:
                                    st.write(f"⭐ {product['rating']}")
                    
                    st.session_state.messages.append(message_data)
                else:
                    error_msg = "Sorry, I couldn't process your request. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Product showcase
    if st.session_state.products:
        st.header("📦 Product Showcase")
        for product in st.session_state.products[:6]:
            display_product(product)


if __name__ == "__main__":
    main()
