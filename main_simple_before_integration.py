from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_frontend():
    if os.path.exists('frontend/index.html'):
        return FileResponse('frontend/index.html')
    return {"message": "KnowledgeOps Platform API is running!"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "documents_count": 0,
        "vectors_count": 0,
        "total_tokens": 0
    }

@app.post("/query")
async def query_for_frontend(request: dict):
    # 模擬回應
    return {
        "answer": f"This is a simulated response to: '{request.get('question', '')}'. Please integrate your RAG system.",
        "sources": [{"content": "Simulated source", "metadata": {"filename": "example.pdf", "page": 1}}],
        "confidence": 0.85
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    return {
        "message": "File uploaded successfully (simulated)",
        "filename": file.filename,
        "chunks_created": 5
    }

@app.get("/documents")
async def list_documents():
    return []

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    return {"message": "Document deleted successfully"}
