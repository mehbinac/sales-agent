import pytest
from app.services.semantic_search import SemanticSearchService


@pytest.fixture
def search_service():
    """Create a semantic search service instance"""
    return SemanticSearchService()


def test_load_faqs(search_service):
    """Test loading FAQs"""
    faqs = search_service.get_all_faqs()
    assert len(faqs) > 0
    assert all(hasattr(f, 'question') for f in faqs)
    assert all(hasattr(f, 'answer') for f in faqs)


def test_search_faqs(search_service):
    """Test FAQ semantic search"""
    # Search for shipping-related questions
    results = search_service.search_faqs("shipping time", top_k=2)
    assert len(results) <= 2
    assert all(len(item) == 2 for item in results)  # Each result is (FAQ, score)
    
    # Check that results contain FAQ objects
    for faq, score in results:
        assert hasattr(faq, 'question')
        assert hasattr(faq, 'answer')
        assert 0 <= score <= 1


def test_search_faqs_relevance(search_service):
    """Test that FAQ search returns relevant results"""
    # Search for return policy
    results = search_service.search_faqs("return policy", top_k=3)
    
    if results:
        # The top result should be about returns
        top_faq, top_score = results[0]
        assert "return" in top_faq.question.lower() or "return" in top_faq.answer.lower()
