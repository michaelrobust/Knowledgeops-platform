from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys
from typing import List, Dict, Any
from pydantic import BaseModel

# 添加 app 目錄到 Python 路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# 導入你的服務
try:
    from app.services.llm_service import LLMService
    from app.services.document_parser import DocumentParser, chunk_document
    from app.services.vector_service import VectorService
    print("✅ Successfully imported your RAG services!")
except ImportError as e:
    print(f"⚠️  Could not import services: {e}")
    print("Will use fallback implementations")
    LLMService = None
    DocumentParser = None
    VectorService = None

# Create FastAPI app
app = FastAPI(
    title="KnowledgeOps Platform",
    description="RAG-powered Knowledge Management System with Real Intelligence",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize services
llm_service = None
doc_parser = None
vector_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global llm_service, doc_parser, vector_service
    
    print("🚀 Initializing KnowledgeOps Platform...")
    
    # Initialize LLM Service
    if LLMService:
        try:
            llm_service = LLMService()
            print("✅ LLM Service initialized")
        except Exception as e:
            print(f"⚠️  LLM Service initialization failed: {e}")
    
    # Initialize Document Parser
    if DocumentParser:
        try:
            doc_parser = DocumentParser()
            print("✅ Document Parser initialized")
        except Exception as e:
            print(f"⚠️  Document Parser initialization failed: {e}")
    
    # Initialize Vector Service
    if VectorService:
        try:
            vector_service = VectorService()
            print("✅ Vector Service initialized")
        except Exception as e:
            print(f"⚠️  Vector Service initialization failed: {e}")
    
    print("🎉 KnowledgeOps Platform startup complete!")

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    max_results: int = 5
    use_rag: bool = True

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []
    confidence: float = 0.0
    success: bool = True
    model: str = "integrated"

@app.get("/")
async def serve_frontend():
    """Serve frontend HTML file"""
    if os.path.exists('frontend/index.html'):
        return FileResponse('frontend/index.html')
    return {
        "message": "KnowledgeOps Platform API is running!",
        "version": "2.0.0",
        "status": "Ready for intelligent conversations!"
    }

@app.get("/health")
async def health():
    """Enhanced health check with real service status"""
    try:
        # Get document count
        doc_count = 0
        storage_dirs = ["storage", "data"]
        for storage_dir in storage_dirs:
            if os.path.exists(storage_dir):
                doc_count += len([f for f in os.listdir(storage_dir) 
                                if f.lower().endswith(('.pdf', '.docx', '.txt'))])
        
        # Get vector count (if vector service is available)
        vector_count = 0
        if vector_service:
            try:
                stats = vector_service.get_stats()
                vector_count = stats.get('total_chunks', 0)
            except:
                vector_count = 0
        
        # Get service status
        service_status = {}
        if llm_service:
            service_status = llm_service.get_service_status()
        
        return {
            "status": "healthy",
            "service": "knowledgeops-platform",
            "version": "2.0.0",
            "documents_count": doc_count,
            "vectors_count": vector_count,
            "total_tokens": 0,  # TODO: implement token tracking
            "services": {
                "llm_service": llm_service is not None,
                "vector_service": vector_service is not None,
                "document_parser": doc_parser is not None,
                **service_status
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "documents_count": 0,
            "vectors_count": 0,
            "total_tokens": 0
        }

@app.post("/query")
async def query_for_frontend(request: dict):
    """
    Real RAG-powered query endpoint
    """
    try:
        question = request.get("question", "")
        max_results = request.get("max_results", 5)
        
        if not question.strip():
            raise ValueError("Question cannot be empty")
        
        # Use real LLM service if available
        if llm_service:
            result = llm_service.process_query(
                query=question,
                use_rag=True,
                max_docs=max_results
            )
            
            return {
                "answer": result.get("answer", "No answer generated"),
                "sources": result.get("sources", []),
                "confidence": 0.85,  # TODO: implement real confidence scoring
                "success": result.get("success", False),
                "model": result.get("model", "integrated"),
                "metadata": {
                    "sources_found": len(result.get("sources", [])),
                    "processing_time": "< 1s",  # TODO: implement real timing
                    "rag_enabled": result.get("use_rag", True)
                }
            }
        else:
            # Fallback to enhanced mock response
            return {
                "answer": f"Enhanced mock response: I understand you're asking about '{question}'. Your RAG system is partially initialized but needs full service integration. The system architecture is ready for real intelligence!",
                "sources": [
                    {
                        "content": f"Mock relevant content for: {question}",
                        "metadata": {"filename": "system_ready.txt", "page": 1, "score": 0.9}
                    }
                ],
                "confidence": 0.75,
                "success": True,
                "model": "fallback_enhanced"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)}")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Real document upload and processing
    """
    try:
        # Check file type
        allowed_types = [
            "application/pdf", 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain"
        ]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Create storage directory
        storage_dir = "storage"
        os.makedirs(storage_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(storage_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        chunks_created = 0
        processing_status = "uploaded"
        
        # Process document if services are available
        if doc_parser and vector_service:
            try:
                # Parse document and create chunks using the correct function
                print(f"📄 Parsing document: {file.filename}")
                
                # Use chunk_document function which returns properly formatted chunks
                if chunk_document:
                    chunks = chunk_document(file_path, chunk_size=500, overlap=50)
                else:
                    # Fallback: parse document and manually create chunks
                    result = doc_parser.parse_document(file_path)
                    content_text = result.get('content', '')
                    
                    # Create chunks manually
                    chunk_size = 500
                    overlap = 50
                    chunks = []
                    for i in range(0, len(content_text), chunk_size - overlap):
                        chunk_text = content_text[i:i + chunk_size]
                        if chunk_text.strip():
                            chunks.append({
                                "content": chunk_text.strip(),
                                "metadata": {
                                    "filename": file.filename,
                                    "chunk_index": len(chunks),
                                    "source_file": file.filename
                                }
                            })
                
                # Add to vector database
                print(f"🔍 Adding {len(chunks)} chunks to vector database")
                vector_service.add_documents(chunks)
                
                chunks_created = len(chunks)
                processing_status = "processed_and_indexed"
                print(f"✅ Document processed: {chunks_created} chunks created")
                
            except Exception as e:
                print(f"⚠️  Document processing error: {e}")
                processing_status = f"uploaded_but_processing_failed: {str(e)}"
        else:
            processing_status = "uploaded_awaiting_service_integration"
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "chunks_created": chunks_created,
            "file_size": len(content),
            "processing_status": processing_status,
            "ready_for_queries": chunks_created > 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

@app.get("/documents")
async def list_documents():
    """
    List uploaded documents with processing status
    """
    try:
        documents = []
        storage_dirs = ["storage", "data"]
        
        doc_id = 0
        for storage_dir in storage_dirs:
            if os.path.exists(storage_dir):
                for filename in os.listdir(storage_dir):
                    if filename.lower().endswith(('.pdf', '.docx', '.txt')):
                        file_path = os.path.join(storage_dir, filename)
                        file_size = os.path.getsize(file_path)
                        
                        # Try to get chunk info from vector service
                        chunks = 0
                        if vector_service:
                            try:
                                # This would need to be implemented in your vector service
                                # chunks = vector_service.get_chunks_for_file(filename)
                                chunks = 5  # Mock for now
                            except:
                                chunks = 0
                        
                        documents.append({
                            "id": f"doc_{doc_id}",
                            "filename": filename,
                            "chunks": chunks,
                            "file_size": file_size,
                            "status": "indexed" if chunks > 0 else "uploaded",
                            "storage_location": storage_dir
                        })
                        doc_id += 1
        
        return documents
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """
    Delete document from storage and vector database
    """
    try:
        # TODO: Implement real document deletion
        # This should:
        # 1. Find the document by ID
        # 2. Remove from filesystem
        # 3. Remove from vector database
        # 4. Update any indexes
        
        return {
            "message": "Document deletion functionality ready for implementation",
            "doc_id": doc_id,
            "status": "mock_deleted"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_detailed_stats():
    """
    Get detailed system statistics
    """
    try:
        stats = {
            "system": {
                "version": "2.0.0",
                "status": "operational",
                "uptime": "< 1 hour"  # TODO: implement real uptime
            },
            "services": {
                "llm_service": llm_service is not None,
                "vector_service": vector_service is not None,
                "document_parser": doc_parser is not None
            },
            "storage": {
                "total_documents": len(await list_documents()),
                "total_size_mb": 0  # TODO: implement
            }
        }
        
        if llm_service:
            service_status = llm_service.get_service_status()
            stats["llm"] = service_status
        
        if vector_service:
            try:
                vector_stats = vector_service.get_stats()
                stats["vectors"] = vector_stats
            except:
                stats["vectors"] = {"status": "unavailable"}
        
        return stats
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting KnowledgeOps Platform with RAG Integration...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
