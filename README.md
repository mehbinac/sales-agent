# AI Sales Agent (FastAPI + Streamlit + Semantic Retrieval)

A lightweight AI sales assistant for travel gear. The app combines:
- FastAPI for the chat API
- Streamlit for the web chat UI
- SentenceTransformers for semantic retrieval from local FAQ/product data
- Groq LLM for final response generation

## What This Repository Contains

This repository is a compact, single-folder implementation (not a multi-package app structure).

Top-level files:
- `main.py`: FastAPI backend with `POST /chat`
- `app.py`: Streamlit chat frontend
- `retriever.py`: Embedding + semantic search over local JSON datasets
- `logger.py`: Session logging to JSON files under `logs/`
- `data/faq_data.json`: FAQ dataset
- `data/product_data.json`: Product catalog dataset
- `requirements.txt`: Python dependencies

## Project Layout (Current Workspace)

```text
sales-agent/
├── app.py                     # Streamlit frontend
├── main.py                    # FastAPI backend
├── retriever.py               # Embedding model + semantic retrieval
├── logger.py                  # Session logging utility
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── LICENSE                    # MIT license text
├── .gitignore                 # Ignore rules (.venv, .env, logs, __pycache__)
├── .env                       # Local env vars (not committed)
├── data/
│   ├── faq_data.json          # FAQ dataset
│   └── product_data.json      # Product dataset
├── logs/                      # Runtime-generated JSON sessions
├── __pycache__/               # Runtime bytecode cache
├── tests/                     # Present but currently empty
└── final final/               # Extra folder containing a nested venv (not used by app)
```

Notes:
- Core runtime code is only `main.py`, `app.py`, `retriever.py`, and `logger.py`.
- `logs/` and `__pycache__/` are generated during execution.
- `final final/` is not imported or referenced by the app startup path.

## How It Works

1. User sends a message from Streamlit UI.
2. FastAPI receives the message and conversation history.
3. Retriever finds top semantic matches from:
   - FAQ entries (`data/faq_data.json`)
   - Product entries (`data/product_data.json`)
4. Retrieved context is injected into a prompt.
5. Groq model (`llama-3.1-8b-instant`) generates a sales-focused reply.
6. Interaction is saved to a timestamped JSON log file.

## Prerequisites

- Python 3.10+
- Internet access on first run (to download embedding model)
- A Groq API key

## Setup

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd sales-agent
```

### 2. Create and activate virtual environment

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows (Git Bash):
```bash
python -m venv .venv
source .venv/Scripts/activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the repo root with:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Run the Application

### Terminal 1: Start FastAPI backend

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2: Start Streamlit frontend

```bash
streamlit run app.py --server.port 8501
```

Open:
- Streamlit UI: `http://127.0.0.1:8501`
- FastAPI docs: `http://127.0.0.1:8000/docs`

Optional quick API check:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I need a carry-on backpack","history":[]}'
```

## API

### `POST /chat`

Request body:

```json
{
  "message": "I need a carry-on bag for weekend trips",
  "history": []
}
```

Response body:

```json
{
  "response": "...assistant reply...",
  "updated_history": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## Data Files

### FAQ schema (`data/faq_data.json`)
Each item includes:
- `id`
- `question`
- `answer`

### Product schema (`data/product_data.json`)
Each item includes:
- `id`
- `name`
- `category`
- `price_range`
- `ideal_for` (list)
- `features` (list)
- `description`
- `use_cases` (list)

## Logging

Each run creates a session log in `logs/`:
- File format: `session_YYYYMMDD_HHMMSS.json`
- Entries include user input, retrieved context, similarity scores, and assistant reply.

## Notes and Limitations

- The retriever preloads data and embeddings at import time.
- First startup may be slower while `all-MiniLM-L6-v2` downloads.
- If no results pass similarity threshold (`min_similarity=0.45`), context can be sparse.
- `tests/` currently exists but is empty in this repo state.
- The repository includes an extra folder `final final/` with a nested virtual environment; it is not part of the active app flow.

## Quick Troubleshooting

- `KeyError: 'GROQ_API_KEY'`:
  Add `GROQ_API_KEY` to `.env` and restart backend.
- Backend not reachable from Streamlit:
  Ensure FastAPI is running on `127.0.0.1:8000`.
- Slow first request:
  Wait for embedding model download/cache to complete.

## License

MIT - see `LICENSE`.
