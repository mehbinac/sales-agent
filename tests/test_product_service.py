import pytest
from app.services.product_service import ProductService


@pytest.fixture
def product_service():
    """Create a product service instance"""
    return ProductService()


def test_load_products(product_service):
    """Test loading products"""
    products = product_service.get_all_products()
    assert len(products) > 0
    assert all(hasattr(p, 'id') for p in products)
    assert all(hasattr(p, 'name') for p in products)


def test_get_product_by_id(product_service):
    """Test getting product by ID"""
    product = product_service.get_product_by_id(1)
    assert product is not None
    assert product.id == 1
    
    # Test non-existent product
    product = product_service.get_product_by_id(9999)
    assert product is None


def test_search_products(product_service):
    """Test product search"""
    # Search by name
    results = product_service.search_products("headphones")
    assert len(results) > 0
    assert any("headphone" in p.name.lower() for p in results)
    
    # Search with category filter
    results = product_service.search_products("", category="Electronics")
    assert all(p.category == "Electronics" for p in results)
    
    # Search with price filters
    results = product_service.search_products("", min_price=50, max_price=100)
    assert all(50 <= p.price <= 100 for p in results)


def test_get_categories(product_service):
    """Test getting categories"""
    categories = product_service.get_categories()
    assert len(categories) > 0
    assert isinstance(categories, list)
    assert "Electronics" in categories


def test_get_recommendations(product_service):
    """Test getting recommendations"""
    # Test recommendations by product ID
    recommendations = product_service.get_recommendations(product_id=1, max_results=3)
    assert len(recommendations) <= 3
    
    # Test recommendations by category
    recommendations = product_service.get_recommendations(category="Electronics", max_results=5)
    assert len(recommendations) <= 5
    assert all(p.category == "Electronics" for p in recommendations)
