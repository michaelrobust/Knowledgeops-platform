from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ...services.llm_service import LLMService

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Request models
class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True
    model: Optional[str] = None
    max_docs: int = 3

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    success: bool
    use_rag: bool
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Initialize LLM service
llm_service = LLMService()

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """
    Process chat query with optional RAG
    """
    try:
        result = llm_service.process_query(
            query=request.message,
            use_rag=request.use_rag,
            model=request.model
        )
        
        # Convert to response model
        response = ChatResponse(
            answer=result.get("answer", "No answer generated"),
            sources=result.get("sources", []),
            success=result.get("success", False),
            use_rag=result.get("use_rag", request.use_rag),
            model=result.get("model"),
            usage=result.get("usage"),
            error=result.get("error")
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Test vector service
        test_result = llm_service.search_relevant_documents("test", max_docs=1)
        
        return {
            "status": "healthy",
            "vector_service": "operational",
            "documents_available": len(test_result) > 0,
            "timestamp": "2025-08-04"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": "2025-08-04"
        }

@router.get("/stats")
async def get_stats():
    """
    Get service statistics
    """
    try:
        vector_stats = llm_service.vector_service.get_stats()
        
        return {
            "vector_database": vector_stats,
            "service_status": "operational",
            "features": {
                "vector_search": True,
                "llm_integration": True,
                "rag_pipeline": True
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "service_status": "error"
        }
