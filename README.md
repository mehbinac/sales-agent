# AI-Powered E-commerce Sales Agent 🛒🤖

An intelligent conversational sales agent for e-commerce, powered by open-source AI technologies including LangChain, SentenceTransformers, and Hugging Face models.

## Features ✨

- **Conversational AI Chat Agent**: LangChain-powered chat interface using open-source LLMs (Google Flan-T5)
- **Product Search & Discovery**: Intelligent product search with filtering by category, price, and features
- **Smart Recommendations**: Context-aware product recommendations based on user preferences
- **Semantic FAQ Search**: Find answers using SentenceTransformers embeddings for natural language queries
- **RESTful API**: FastAPI-based backend with comprehensive endpoints
- **Modern Web UI**: Streamlit-based interactive frontend
- **Fully Dockerized**: Easy deployment with Docker and docker-compose
- **Production Ready**: Logging, error handling, and unit tests included

## Architecture 🏗️

```
sales-agent/
├── app/
│   ├── api/           # FastAPI endpoints
│   ├── models/        # Pydantic schemas
│   ├── services/      # Business logic (chat agent, search, recommendations)
│   └── utils/         # Configuration and logging
├── data/              # Product catalog and FAQ database (JSON)
├── frontend/          # Streamlit UI
├── tests/             # Unit tests
├── docker-compose.yml # Container orchestration
└── requirements.txt   # Python dependencies
```

## Tech Stack 🛠️

### AI/ML Components
- **LangChain**: Orchestration framework for LLM applications
- **Hugging Face Transformers**: Open-source LLM (google/flan-t5-base)
- **SentenceTransformers**: Semantic search with embeddings (all-MiniLM-L6-v2)

### Backend
- **FastAPI**: High-performance async API framework
- **Pydantic**: Data validation and settings management
- **Python 3.10**: Core programming language

### Frontend
- **Streamlit**: Interactive web application framework

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Pytest**: Testing framework

## Quick Start 🚀

### Prerequisites
- Docker and Docker Compose installed
- Or Python 3.10+ for local development
- **Internet connection required for first run** (to download AI models from Hugging Face)

### Option 1: Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/mehbinac/sales-agent.git
cd sales-agent
```

2. Start the services:
```bash
docker-compose up --build
```

3. Access the applications:
   - **Frontend (Streamlit)**: http://localhost:8501
   - **API Documentation**: http://localhost:8000/docs
   - **API Health Check**: http://localhost:8000/health

### Option 2: Local Development

1. Clone the repository:
```bash
git clone https://github.com/mehbinac/sales-agent.git
cd sales-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the API server:
```bash
python -m uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

5. In a new terminal, start the Streamlit frontend:
```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```

## API Documentation 📚

### Key Endpoints

#### Products
- `GET /products` - Get all products
- `GET /products/{id}` - Get product by ID
- `POST /products/search` - Search products with filters
- `GET /categories` - Get all categories
- `POST /recommendations` - Get product recommendations

#### FAQs
- `GET /faqs` - Get all FAQs
- `POST /faqs/search` - Semantic search for FAQs

#### Chat
- `POST /chat` - Chat with the AI sales agent

Full interactive API documentation available at: `http://localhost:8000/docs`

## Usage Examples 💡

### Chat with the Agent
```python
import requests

response = requests.post("http://localhost:8000/chat", json={
    "message": "I'm looking for wireless headphones under $100",
    "conversation_history": []
})

print(response.json())
```

### Search Products
```python
response = requests.post("http://localhost:8000/products/search", json={
    "query": "bluetooth",
    "category": "Electronics",
    "max_price": 100
})

products = response.json()
```

### Get Recommendations
```python
response = requests.post("http://localhost:8000/recommendations", json={
    "product_id": 1,
    "max_results": 5
})

recommendations = response.json()
```

## Testing 🧪

Run the test suite:

```bash
pytest tests/ -v
```

Run specific test files:
```bash
pytest tests/test_api.py -v
pytest tests/test_product_service.py -v
pytest tests/test_semantic_search.py -v
```

## Project Structure 📁

```
sales-agent/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py              # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_agent.py        # LangChain chat agent
│   │   ├── product_service.py   # Product management
│   │   └── semantic_search.py   # FAQ semantic search
│   └── utils/
│       ├── __init__.py
│       ├── config.py            # Configuration
│       └── logger.py            # Logging setup
├── data/
│   ├── products.json            # Product catalog
│   └── faqs.json                # FAQ database
├── frontend/
│   └── streamlit_app.py         # Streamlit UI
├── tests/
│   ├── __init__.py
│   ├── test_api.py              # API tests
│   ├── test_product_service.py  # Service tests
│   └── test_semantic_search.py  # Search tests
├── .env.example                 # Environment template
├── .gitignore
├── docker-compose.yml           # Multi-container setup
├── Dockerfile.api               # API container
├── Dockerfile.frontend          # Frontend container
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Configuration ⚙️

Configuration is managed through environment variables. Copy `.env.example` to `.env` and customize:

```bash
# Application Settings
APP_NAME=E-commerce Sales Agent
LOG_LEVEL=INFO

# LLM Settings
MODEL_NAME=google/flan-t5-base
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Streamlit Settings
STREAMLIT_PORT=8501
```

## Data Models 📊

### Product Catalog
- 10 sample products across multiple categories
- Each product includes: name, category, price, description, features, stock, rating

### FAQ Database
- 10 common e-commerce FAQs
- Covers: returns, shipping, payments, warranties, support

Both datasets are in JSON format and easily extensible.

## Features in Detail 🔍

### 1. Conversational Chat Agent
- Powered by Google Flan-T5 model via LangChain
- Context-aware responses using conversation history
- Automatically searches products and FAQs based on user queries
- Returns relevant products and information in responses

### 2. Product Search
- Full-text search across product names, descriptions, and features
- Filters by category, price range
- Intelligent matching and ranking

### 3. Recommendations
- Category-based recommendations
- Product similarity recommendations
- Configurable result limits

### 4. Semantic FAQ Search
- Uses SentenceTransformers for embedding-based search
- Finds semantically similar questions even with different wording
- Returns top-k most relevant FAQs with similarity scores

## Logging 📝

Logs are written to:
- Console (stdout)
- `logs/app.log` file

Log levels can be configured via the `LOG_LEVEL` environment variable.

## Docker Deployment 🐳

The application consists of two services:

1. **API Service**: FastAPI backend with the chat agent
2. **Frontend Service**: Streamlit web interface

Both services are orchestrated via docker-compose for easy deployment.

### Build and Run
```bash
docker-compose up --build
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

## Development 👨‍💻

### Adding New Products
Edit `data/products.json` to add new products following the existing schema.

### Adding New FAQs
Edit `data/faqs.json` to add new FAQ entries.

### Extending the Chat Agent
Modify `app/services/chat_agent.py` to customize the LLM prompt or add new capabilities.

### Customizing the UI
Edit `frontend/streamlit_app.py` to modify the user interface.

## Troubleshooting 🔧

### Model Download Issues
The first run downloads the LLM and embedding models from Hugging Face. This may take time depending on your connection.

**Model sizes:**
- Flan-T5 base model: ~900 MB
- SentenceTransformers model: ~80 MB

Models are cached after first download in `~/.cache/huggingface/`

### Memory Requirements
The Flan-T5 base model requires approximately 1-2 GB of RAM. For lower memory environments, consider using a smaller model like `google/flan-t5-small`.

### API Connection Issues
Ensure the API is running before starting the frontend. Check `http://localhost:8000/health` to verify the API is accessible.

### Network Restrictions
If running in an environment with restricted internet access:
- Product search and recommendations will work normally (no models needed)
- Semantic FAQ search and AI chat features will be unavailable until models are downloaded
- The application gracefully degrades - core features remain functional

## Future Enhancements 🚀

- [ ] Add user authentication and session management
- [ ] Implement shopping cart functionality
- [ ] Add product image support
- [ ] Integrate with real payment gateways
- [ ] Add more sophisticated recommendation algorithms
- [ ] Support for multiple languages
- [ ] Deploy to cloud platforms (AWS, GCP, Azure)

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [LangChain](https://github.com/langchain-ai/langchain) for the LLM framework
- [Hugging Face](https://huggingface.co/) for the open-source models
- [SentenceTransformers](https://www.sbert.net/) for semantic search capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent API framework
- [Streamlit](https://streamlit.io/) for the intuitive UI framework

## Support 💬

For issues, questions, or contributions, please open an issue on GitHub.

---

Built with ❤️ using open-source AI technologies