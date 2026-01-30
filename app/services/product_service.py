import json
from typing import List, Optional
from pathlib import Path
from app.models.schemas import Product
from app.utils.config import PRODUCTS_FILE
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProductService:
    """Service for managing products"""
    
    def __init__(self):
        self.products: List[Product] = []
        self.load_products()
    
    def load_products(self):
        """Load products from JSON file"""
        try:
            with open(PRODUCTS_FILE, 'r') as f:
                data = json.load(f)
                self.products = [Product(**item) for item in data]
            logger.info(f"Loaded {len(self.products)} products")
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            self.products = []
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.products
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None
    
    def search_products(
        self, 
        query: str, 
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """Search products by query and filters"""
        results = []
        query_lower = query.lower()
        
        for product in self.products:
            # Check category filter
            if category and product.category != category:
                continue
            
            # Check price filters
            if min_price and product.price < min_price:
                continue
            if max_price and product.price > max_price:
                continue
            
            # Search in name, description, and features
            if (query_lower in product.name.lower() or 
                query_lower in product.description.lower() or
                any(query_lower in feature.lower() for feature in product.features)):
                results.append(product)
        
        logger.info(f"Search '{query}' returned {len(results)} products")
        return results
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return [p for p in self.products if p.category == category]
    
    def get_recommendations(
        self, 
        product_id: Optional[int] = None, 
        category: Optional[str] = None,
        max_results: int = 5
    ) -> List[Product]:
        """Get product recommendations"""
        if product_id:
            # Recommend products from same category
            product = self.get_product_by_id(product_id)
            if product:
                category = product.category
        
        if category:
            candidates = self.get_products_by_category(category)
            if product_id:
                # Exclude the current product
                candidates = [p for p in candidates if p.id != product_id]
        else:
            # Return top-rated products
            candidates = self.products
        
        # Sort by rating and return top results
        recommendations = sorted(candidates, key=lambda p: p.rating, reverse=True)[:max_results]
        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        return list(set(p.category for p in self.products))
