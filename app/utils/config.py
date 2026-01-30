import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
PRODUCTS_FILE = DATA_DIR / "products.json"
FAQS_FILE = DATA_DIR / "faqs.json"

# Application settings
APP_NAME = os.getenv("APP_NAME", "E-commerce Sales Agent")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# LLM settings
MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-base")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Streamlit settings
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
