from typing import List, Dict, Any, Tuple
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from app.models.schemas import ChatMessage, Product, FAQ
from app.services.product_service import ProductService
from app.services.semantic_search import SemanticSearchService
from app.utils.config import MODEL_NAME
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChatAgentService:
    """LangChain-based chat agent for e-commerce"""
    
    def __init__(self):
        self.product_service = ProductService()
        self.search_service = SemanticSearchService()
        logger.info(f"Loading LLM model: {MODEL_NAME}")
        self._initialize_llm()
        self._initialize_chain()
    
    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
            
            pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=512,
                temperature=0.7,
                top_p=0.95,
            )
            
            self.llm = HuggingFacePipeline(pipeline=pipe)
            logger.info("LLM initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            raise
    
    def _initialize_chain(self):
        """Initialize the LangChain chain"""
        template = """You are a helpful e-commerce sales assistant. Help customers find products and answer questions.

Context: {context}
History: {history}
Customer: {input}
Assistant:"""
        
        prompt = PromptTemplate(
            input_variables=["context", "history", "input"],
            template=template
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=prompt)
        logger.info("LangChain chain initialized")
    
    def _build_context(self, message: str) -> Tuple[str, List[Product], List[FAQ]]:
        """Build context from product search and FAQ search"""
        context_parts = []
        relevant_products = []
        relevant_faqs = []
        
        # Search for relevant products
        products = self.product_service.search_products(message)
        if products:
            relevant_products = products[:5]
            context_parts.append(f"Found {len(products)} relevant products:")
            for p in relevant_products[:3]:
                context_parts.append(f"- {p.name}: ${p.price} ({p.category})")
        
        # Search FAQs
        faq_results = self.search_service.search_faqs(message, top_k=2)
        if faq_results:
            relevant_faqs = [faq for faq, score in faq_results if score > 0.5]
            if relevant_faqs:
                context_parts.append("\nRelevant FAQ:")
                for faq in relevant_faqs:
                    context_parts.append(f"Q: {faq.question}")
                    context_parts.append(f"A: {faq.answer}")
        
        context = "\n".join(context_parts) if context_parts else "No specific context available."
        return context, relevant_products, relevant_faqs
    
    def chat(self, message: str, history: List[ChatMessage] = None) -> Tuple[str, List[Product], List[FAQ]]:
        """Process a chat message and return response"""
        if history is None:
            history = []
        
        try:
            # Build context
            context, products, faqs = self._build_context(message)
            
            # Format history
            history_text = "\n".join([
                f"{msg.role}: {msg.content}" for msg in history[-5:]
            ]) if history else "No previous conversation."
            
            # Generate response
            response = self.chain.run(
                context=context,
                history=history_text,
                input=message
            )
            
            logger.info(f"Generated response for: {message[:50]}...")
            return response.strip(), products, faqs
        
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "I apologize, but I'm having trouble processing your request. Please try again.", [], []
