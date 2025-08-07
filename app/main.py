from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api.routes import chat
import os
from typing import List

# Create FastAPI app
app = FastAPI(
    title="KnowledgeOps Platform",
    description="RAG-powered Knowledge Management System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include routers
app.include_router(chat.router)

@app.get("/")
async def serve_frontend():
    """
    Serve frontend HTML file
    """
    if os.path.exists('frontend/index.html'):
        return FileResponse('frontend/index.html')
    
    return {
        "message": "Welcome to KnowledgeOps Platform",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Document processing",
            "Vector search",
            "RAG pipeline",
            "LLM integration"
        ]
    }

@app.get("/health")
async def health():
    """
    Enhanced health check for frontend compatibility
    """
    try:
        # Get document count if storage directory exists
        doc_count = 0
        if os.path.exists("storage"):
            doc_count = len([f for f in os.listdir("storage") if f.endswith(('.pdf', '.docx'))])
        
        return {
            "status": "healthy",
            "service": "knowledgeops-platform",
            "documents_count": doc_count,
            "vectors_count": 0,  # You can implement this based on your vector service
            "total_tokens": 0    # You can implement this based on your usage tracking
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "documents_count": 0,
            "vectors_count": 0,
            "total_tokens": 0
        }

# Add frontend-compatible endpoints
@app.post("/query")
async def query_for_frontend(request: dict):
    """
    Frontend-compatible query endpoint
    """
    try:
        # Redirect to existing chat endpoint with proper formatting
        from .api.routes.chat import chat_query, ChatRequest
        
        chat_request = ChatRequest(
            message=request.get("question", ""),
            use_rag=True,
            max_docs=request.get("max_results", 5)
        )
        
        result = await chat_query(chat_request)
        
        # Format response for frontend compatibility
        return {
            "answer": result.answer,
            "sources": result.sources,
            "confidence": 0.85  # You can implement confidence scoring
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Document upload endpoint for frontend
    """
    try:
        # Check file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Create storage directory if it doesn't exist
        storage_dir = "storage"
        os.makedirs(storage_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(storage_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # TODO: Process document with your existing services
        # You can call your document parser and vector service here
        # Example:
        # from .services.document_parser import DocumentParser
        # from .services.vector_service import VectorService
        # parser = DocumentParser()
        # vector_service = VectorService()
        # chunks = parser.parse_document(file_path)
        # vector_service.add_documents(chunks)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "chunks_created": 10  # Replace with actual chunk count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """
    List uploaded documents
    """
    try:
        documents = []
        storage_dir = "storage"
        
        if os.path.exists(storage_dir):
            for i, filename in enumerate(os.listdir(storage_dir)):
                if filename.endswith(('.pdf', '.docx')):
                    documents.append({
                        "id": f"doc_{i}",
                        "filename": filename,
                        "chunks": 10  # Replace with actual chunk count
                    })
        
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """
    Delete document
    """
    try:
        # TODO: Implement document deletion
        # This should also remove from vector database
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
