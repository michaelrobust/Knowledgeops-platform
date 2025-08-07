import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Database
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
    
    # Limits
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    MAX_CHUNKS_PER_DOC = int(os.getenv("MAX_CHUNKS_PER_DOC", 100))
    
    # Security
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Model
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3-70b-8192")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
