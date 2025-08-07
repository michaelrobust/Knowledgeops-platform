import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        """Initialize with working Groq model"""
        self.groq_client = None
        self.model_type = "fallback"
        
        groq_key = os.getenv("GROQ_API_KEY")
        
        if groq_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=groq_key)
                self.model_type = "groq"
                # 使用可用的最強模型
                self.groq_model = "llama3-70b-8192"
                print(f"✅ Groq LLM initialized with {self.groq_model}")
            except Exception as e:
                print(f"❌ Groq init failed: {e}")
        else:
            print("❌ No GROQ_API_KEY found")
        
        # Vector service
        try:
            from app.services.vector_service import VectorService
            self.vector_service = VectorService()
            print("✅ Vector service connected")
        except Exception as e:
            print(f"⚠️ Vector service: {e}")
            self.vector_service = None
    
    def process_query(self, query: str, context: List[Dict] = None, use_rag: bool = True, max_docs: int = 5) -> Dict[str, Any]:
        """Process query with Groq Llama3"""
        
        # Get RAG documents
        sources = []
        rag_context = ""
        
        if use_rag and self.vector_service:
            try:
                results = self.vector_service.search_similar(query, max_docs)
                if results:
                    sources = results
                    rag_context = "\n\n".join([
                        f"Document {i+1}: {r.get('content', '')[:300]}..."
                        for i, r in enumerate(results[:3])
                    ])
            except Exception as e:
                print(f"RAG error: {e}")
        
        # Use Groq
        if self.groq_client:
            try:
                messages = []
                
                # System message
                system_msg = "You are a helpful AI assistant with perfect memory of our conversation."
                if rag_context:
                    system_msg += f"\n\nRelevant documents from knowledge base:\n{rag_context}\n\nUse these documents to answer when relevant."
                
                messages.append({"role": "system", "content": system_msg})
                
                # Add conversation context
                if context:
                    for msg in context[-6:]:  # Last 3 exchanges
                        role = msg.get("role", "user")
                        content = msg.get("content", "")
                        if content:
                            messages.append({"role": role, "content": content})
                
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
                print(f"❌ Groq error: {e}")
                return self._fallback_response(query, sources)
        
        return self._fallback_response(query, sources)
    
    def _fallback_response(self, query: str, sources: List) -> Dict:
        """Fallback when Groq not available"""
        if sources:
            answer = f"Found {len(sources)} relevant documents for: {query}\n\n"
            for i, s in enumerate(sources[:3], 1):
                content = s.get('content', '')[:200]
                answer += f"{i}. {content}...\n"
        else:
            answer = f"Processing: {query} (AI service not available)"
        
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
