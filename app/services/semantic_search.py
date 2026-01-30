import json
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from app.models.schemas import FAQ
from app.utils.config import FAQS_FILE, EMBEDDING_MODEL
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SemanticSearchService:
    """Service for semantic search using sentence transformers"""
    
    def __init__(self):
        self.faqs: List[FAQ] = []
        self.faq_embeddings = None
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.load_faqs()
    
    def load_faqs(self):
        """Load FAQs from JSON file and create embeddings"""
        try:
            with open(FAQS_FILE, 'r') as f:
                data = json.load(f)
                self.faqs = [FAQ(**item) for item in data]
            
            # Create embeddings for FAQ questions
            questions = [faq.question for faq in self.faqs]
            self.faq_embeddings = self.model.encode(questions, convert_to_tensor=False)
            logger.info(f"Loaded {len(self.faqs)} FAQs with embeddings")
        except Exception as e:
            logger.error(f"Error loading FAQs: {e}")
            self.faqs = []
            self.faq_embeddings = None
    
    def search_faqs(self, query: str, top_k: int = 3) -> List[Tuple[FAQ, float]]:
        """Search FAQs using semantic similarity"""
        if not self.faqs or self.faq_embeddings is None:
            return []
        
        try:
            # Encode the query
            query_embedding = self.model.encode([query], convert_to_tensor=False)[0]
            
            # Calculate cosine similarity
            similarities = np.dot(self.faq_embeddings, query_embedding) / (
                np.linalg.norm(self.faq_embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Get top-k results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            results = [(self.faqs[idx], float(similarities[idx])) for idx in top_indices]
            
            logger.info(f"FAQ search for '{query}' returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching FAQs: {e}")
            return []
    
    def get_all_faqs(self) -> List[FAQ]:
        """Get all FAQs"""
        return self.faqs
