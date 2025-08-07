import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        """Initialize LLM Service with Groq"""
        self.groq_client = None
        self.model_type = "fallback"
        
        # Initialize Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=groq_key)
                self.model_type = "groq"
                self.groq_model = "mixtral-8x7b-32768"
                print(f"✅ Groq LLM initialized successfully!")
                print(f"   Using model: {self.groq_model}")
            except Exception as e:
                print(f"⚠️ Groq init failed: {e}")
        
        # Import vector service
        try:
            from app.services.vector_service import VectorService
            self.vector_service = VectorService()
        except:
            self.vector_service = None
    
    def process_query(self, query: str, context: List[Dict] = None, use_rag: bool = True, max_docs: int = 5) -> Dict[str, Any]:
        """Process query with Groq"""
        
        # Get RAG documents if enabled
        sources = []
        rag_context = ""
        
        if use_rag and self.vector_service:
            try:
                search_results = self.vector_service.search_similar(query, max_docs)
                if search_results:
                    sources = search_results
                    rag_context = "\n".join([
                        f"Doc {i+1}: {r.get('content', '')[:300]}"
                        for i, r in enumerate(search_results[:3])
                    ])
            except Exception as e:
                print(f"RAG error: {e}")
        
        # Use Groq if available
        if self.groq_client:
            try:
                messages = []
                
                # Add system message with RAG context
                system_msg = "You are a helpful assistant."
                if rag_context:
                    system_msg += f"\n\nUse these documents to answer:\n{rag_context}"
                messages.append({"role": "system", "content": system_msg})
                
                # Add conversation context if provided
                if context:
                    for msg in context[-6:]:  # Last 3 exchanges
                        messages.append({
                            "role": msg.get("role", "user"),
                            "content": msg.get("content", "")
                        })
                
                # Add current query
                messages.append({"role": "user", "content": query})
                
                # Call Groq
                response = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                answer = response.choices[0].message.content
                
                return {
                    "answer": answer,
                    "sources": sources,
                    "success": True,
                    "model": f"groq/{self.groq_model}",
                    "use_rag": bool(rag_context)
                }
                
            except Exception as e:
                print(f"Groq error: {e}")
                return self._fallback_response(query, sources)
        
        return self._fallback_response(query, sources)
    
    def _fallback_response(self, query: str, sources: List) -> Dict:
        """Fallback when no AI available"""
        if sources:
            answer = f"Found {len(sources)} relevant documents for: {query}\n\n"
            for i, s in enumerate(sources[:3], 1):
                answer += f"{i}. {s.get('content', '')[:200]}...\n"
        else:
            answer = f"Processing query: {query} (No AI service available)"
        
        return {
            "answer": answer,
            "sources": sources,
            "success": True,
            "model": "fallback",
            "use_rag": bool(sources)
        }
    
    def get_service_status(self) -> Dict:
        return {
            "llm_type": self.model_type,
            "groq_available": self.groq_client is not None,
            "model": self.groq_model if self.groq_client else "none"
        }
