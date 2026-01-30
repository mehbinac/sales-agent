import pytest
from fastapi.testclient import TestClient
from app.api.main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_products(client):
    """Test get all products endpoint"""
    response = client.get("/products")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0


def test_get_product_by_id(client):
    """Test get product by ID endpoint"""
    response = client.get("/products/1")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == 1
    assert "name" in product
    
    # Test non-existent product
    response = client.get("/products/9999")
    assert response.status_code == 404


def test_search_products(client):
    """Test product search endpoint"""
    response = client.post(
        "/products/search",
        json={"query": "headphones"}
    )
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)


def test_get_categories(client):
    """Test get categories endpoint"""
    response = client.get("/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) > 0


def test_get_recommendations(client):
    """Test recommendations endpoint"""
    response = client.post(
        "/recommendations",
        json={"product_id": 1, "max_results": 3}
    )
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 3


def test_get_faqs(client):
    """Test get FAQs endpoint"""
    response = client.get("/faqs")
    assert response.status_code == 200
    faqs = response.json()
    assert isinstance(faqs, list)
    assert len(faqs) > 0


def test_search_faqs(client):
    """Test FAQ search endpoint"""
    response = client.post(
        "/faqs/search?query=shipping&top_k=2"
    )
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) <= 2
