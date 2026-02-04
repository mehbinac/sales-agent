from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.models.schemas import (
    Product, FAQ, ChatRequest, ChatResponse, 
    SearchRequest, RecommendationRequest, ChatMessage
)
from app.services.product_service import ProductService
from app.services.semantic_search import SemanticSearchService
from app.services.chat_agent import ChatAgentService
from app.utils.logger import get_logger
from app.utils.config import APP_NAME
import os

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(title=APP_NAME, version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
product_service = None
search_service = None
chat_agent = None  # Lazy load due to model size

# Feature flags (default enabled)
ENABLE_SEMANTIC_SEARCH = os.getenv("ENABLE_SEMANTIC_SEARCH", "true").lower() == "true"
ENABLE_CHAT_AGENT = os.getenv("ENABLE_CHAT_AGENT", "true").lower() == "true"


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global product_service, search_service, chat_agent
    logger.info("Starting up application...")
    
    # Initialize product service (no model needed)
    product_service = ProductService()


def _ensure_search_service():
    """Lazy initialize semantic search service"""
    global search_service
    if not ENABLE_SEMANTIC_SEARCH:
        raise HTTPException(status_code=503, detail="Semantic search disabled")
    if not search_service:
        try:
            search_service = SemanticSearchService()
        except Exception as e:
            logger.warning(f"Failed to initialize semantic search: {e}")
            raise HTTPException(status_code=503, detail="Search service not initialized")


def _ensure_chat_agent():
    """Lazy initialize chat agent"""
    global chat_agent
    if not ENABLE_CHAT_AGENT:
        raise HTTPException(status_code=503, detail="Chat agent disabled")
    if not chat_agent:
        try:
            chat_agent = ChatAgentService()
        except Exception as e:
            logger.warning(f"Failed to initialize chat agent: {e}")
            raise HTTPException(status_code=503, detail="Chat agent not initialized")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "E-commerce Sales Agent API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/products", response_model=List[Product])
async def get_products():
    """Get all products"""
    if not product_service:
        raise HTTPException(status_code=503, detail="Product service not initialized")
    try:
        products = product_service.get_all_products()
        return products
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get product by ID"""
    if not product_service:
        raise HTTPException(status_code=503, detail="Product service not initialized")
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products/search", response_model=List[Product])
async def search_products(request: SearchRequest):
    """Search products"""
    if not product_service:
        raise HTTPException(status_code=503, detail="Product service not initialized")
    try:
        products = product_service.search_products(
            query=request.query,
            category=request.category,
            min_price=request.min_price,
            max_price=request.max_price
        )
        return products
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories", response_model=List[str])
async def get_categories():
    """Get all product categories"""
    if not product_service:
        raise HTTPException(status_code=503, detail="Product service not initialized")
    try:
        categories = product_service.get_categories()
        return categories
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recommendations", response_model=List[Product])
async def get_recommendations(request: RecommendationRequest):
    """Get product recommendations"""
    if not product_service:
        raise HTTPException(status_code=503, detail="Product service not initialized")
    try:
        recommendations = product_service.get_recommendations(
            product_id=request.product_id,
            category=request.category,
            max_results=request.max_results
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/faqs", response_model=List[FAQ])
async def get_faqs():
    """Get all FAQs"""
    try:
        _ensure_search_service()
        faqs = search_service.get_all_faqs()
        return faqs
    except Exception as e:
        logger.error(f"Error getting FAQs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/faqs/search", response_model=List[FAQ])
async def search_faqs(query: str, top_k: int = 3):
    """Search FAQs using semantic search"""
    try:
        _ensure_search_service()
        results = search_service.search_faqs(query, top_k)
        return [faq for faq, score in results]
    except Exception as e:
        logger.error(f"Error searching FAQs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the sales agent"""
    try:
        _ensure_chat_agent()
        response, products, faqs = chat_agent.chat(
            message=request.message,
            history=request.conversation_history
        )
        
        return ChatResponse(
            response=response,
            products=products,
            faqs=faqs
        )
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    from app.utils.config import API_HOST, API_PORT
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)
