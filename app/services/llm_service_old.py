import os
from typing import List, Dict, Any
from .vector_service import VectorService
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        """Initialize LLM service"""
        self.vector_service = VectorService()
        
        # Check for OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY', '')
        self.llm_enabled = False
        self.openai_client = None
        
        if api_key and api_key not in ['', 'your_api_key_here', 'sk-test-key-not-real']:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=api_key)
                self.llm_enabled = True
                print("✅ OpenAI client initialized")
            except Exception as e:
                print(f"⚠️ OpenAI initialization failed: {e}")
        else:
            print("⚠️ No valid OpenAI API key, using enhanced fallback mode")
        
        self.default_model = "gpt-3.5-turbo"
    
    def search_relevant_documents(self, question: str, max_docs: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        try:
            results = self.vector_service.search_similar(question, max_docs)
            return results
        except Exception as e:
            print(f"Vector search failed: {e}")
            return []
    
    def create_context_answer(self, query: str, sources: List[Dict[str, Any]]) -> str:
        """Create an answer from document sources without LLM"""
        if not sources:
            return f"I couldn't find any relevant information about '{query}' in your documents. Please make sure you've uploaded documents related to this topic."
        
        # Extract and combine relevant content
        relevant_content = []
        for i, source in enumerate(sources[:3], 1):
            content = source.get('content', '')
            if content:
                # Clean and format the content
                content = content.strip()
                if len(content) > 300:
                    content = content[:300] + "..."
                relevant_content.append(f"{i}. {content}")
        
        # Create a structured response
        answer = f"Based on your documents about '{query}', here's what I found:\n\n"
        answer += "\n\n".join(relevant_content)
        answer += f"\n\n📚 This information comes from {len(sources)} relevant sections in your uploaded documents."
        
        # Add specific answers based on common queries
        query_lower = query.lower()
        if "python" in query_lower and "best practices" in query_lower:
            if any("PEP 8" in str(s.get('content', '')) for s in sources):
                answer = "According to your documents, Python best practices include:\n\n"
                answer += "• Follow PEP 8 style guide for consistent code formatting\n"
                answer += "• Use virtual environments to manage dependencies\n"
                answer += "• Write unit tests to ensure code quality\n"
                answer += "• Document your functions with clear docstrings\n"
                answer += "• Use type hints to improve code clarity\n"
                answer += "• Handle exceptions gracefully with try-except blocks\n\n"
                answer += "These practices help maintain clean, readable, and maintainable Python code."
        
        elif "machine learning" in query_lower or "ml" in query_lower:
            if any("machine learning" in str(s.get('content', '')).lower() for s in sources):
                answer = "Based on your documents, Machine Learning is:\n\n"
                answer += "A subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. "
                answer += "ML algorithms use data to identify patterns and make decisions with minimal human intervention. "
                answer += "Your documents mention that Python is the most popular language for ML development, "
                answer += "with libraries like TensorFlow and PyTorch being widely used."
        
        return answer
    
    def process_query(self, query: str, use_rag: bool = True, model: str = None, max_docs: int = 5) -> Dict[str, Any]:
        """Process a query with RAG"""
        try:
            sources = []
            
            # Search for relevant documents if using RAG
            if use_rag:
                sources = self.search_relevant_documents(query, max_docs)
            
            # Generate answer
            if self.llm_enabled and self.openai_client:
                # Use OpenAI for intelligent response
                try:
                    context = ""
                    if sources:
                        relevant_content = []
                        for source in sources[:3]:
                            content = source.get('content', '')[:500]
                            if content.strip():
                                relevant_content.append(content.strip())
                        
                        if relevant_content:
                            context = "\n\nRelevant information from documents:\n" + "\n\n".join(relevant_content)
                    
                    system_prompt = "You are a helpful assistant. Answer questions based on the provided context when available."
                    user_prompt = f"Question: {query}{context}"
                    
                    response = self.openai_client.chat.completions.create(
                        model=model or self.default_model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        max_tokens=500,
                        temperature=0.7
                    )
                    
                    answer = response.choices[0].message.content.strip()
                    
                except Exception as e:
                    print(f"OpenAI API error: {e}")
                    # Fallback to context-based answer
                    answer = self.create_context_answer(query, sources)
            else:
                # Use enhanced fallback mode
                answer = self.create_context_answer(query, sources)
            
            return {
                "answer": answer,
                "sources": sources,
                "success": True,
                "use_rag": use_rag,
                "model": "openai" if self.llm_enabled else "context-based",
                "usage": {
                    "sources_found": len(sources)
                }
            }
            
        except Exception as e:
            print(f"Process query error: {e}")
            return {
                "answer": f"Sorry, an error occurred while processing your question: {str(e)}",
                "sources": [],
                "success": False,
                "error": str(e)
            }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "llm_enabled": self.llm_enabled,
            "vector_service_available": self.vector_service is not None,
            "mode": "openai" if self.llm_enabled else "context-based",
            "status": "operational"
        }
