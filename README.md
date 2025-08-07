# KnowledgeOps Platform

## 🚀 Enterprise RAG System with Conversation Memory

### Features
- 🔍 Semantic search with vector embeddings (ChromaDB)
- 🤖 LLM integration (Groq Llama3-70B)
- 💭 Conversation memory system
- 📄 Multi-format document support (PDF, DOCX, TXT)
- 🎨 Modern responsive UI
- ⚡ Real-time query processing

### Tech Stack
- **Backend**: FastAPI, Python 3.10
- **Vector DB**: ChromaDB
- **LLM**: Groq API (Llama3-70B)
- **Embeddings**: Sentence Transformers
- **Frontend**: Vanilla JS, HTML5, CSS3

### Quick Start

#### 1. Clone the repository
git clone https://github.com/yourusername/knowledgeops-platform.git
cd knowledgeops-platform

#### 2. Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#### 3. Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

#### 4. Run the application
python main_simple.py

#### 5. Open browser
http://localhost:8000

### Docker Deployment
docker-compose up -d

### API Endpoints
- GET / - Web interface
- GET /health - Health check
- POST /query - Query with RAG and memory
- POST /upload - Upload single document
- POST /upload-batch - Upload multiple documents
- GET /documents - List documents

### Performance Metrics
- Query response time: < 2 seconds
- Document processing: ~100 pages/minute
- Concurrent users: 50+
- Memory retention: Full conversation context

### License
MIT License

### Author
Michael Yeh - 2024
