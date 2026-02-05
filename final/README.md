LLM runtime: Ollama (Mistral / Llama3)

Agent framework: LangChain (Haystack later is optional, not now)

Backend: FastAPI

Frontend: Streamlit

Vector store (temp): FAISS (in-memory)

Data: JSON files


ecommerce-sales-agent/
│
├── backend/
│   ├── main.py
│   ├── agent/
│   ├── data/
│
├── frontend/
│   └── app.py
│
├── tests/
├── docker/
├── requirements.txt
├── README.md



“We evaluated OpenChatKit for a full-stack conversational AI pipeline, but chose Ollama during early stages to optimize iteration speed and focus on agent behavior. OpenChatKit remains a future scalability option.”



Llama 3 8B Instruct was selected as the primary model due to its strong conversational abilities and instruction-following, which are critical for sales-oriented dialogue. Mistral 7B was retained as a fallback model for faster, deterministic responses such as product queries and FAQs.



Due to limited local compute and storage resources, the LLM inference layer was deployed on a cloud-based environment (Google Colab) and exposed via a lightweight API. The local application acts as a thin client, enabling scalable development while preserving system modularity

Colab provides free GPU access and rapid iteration, which is ideal for early-stage LLM experimentation and agent development under limited local compute resources.

