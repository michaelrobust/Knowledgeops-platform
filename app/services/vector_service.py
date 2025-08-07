"""
Vector Database Service for KnowledgeOps Platform
Handles document embedding and similarity search
"""
import os
import logging
from typing import List, Dict, Any, Optional
import hashlib

# 直接導入，不用 try/except
import chromadb
from sentence_transformers import SentenceTransformer

VECTOR_AVAILABLE = True  # Always enabled

class VectorService:
    def __init__(self, persist_directory: str = "./data/vector_db"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        if VECTOR_AVAILABLE:
            # Initialize ChromaDB
            self.client = chromadb.PersistentClient(path=persist_directory)
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Vector service initialized with ChromaDB")
        else:
            self.client = None
            self.collection = None
            self.embedding_model = None
            print("❌ Vector service in mock mode")
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to vector database"""
        if not VECTOR_AVAILABLE:
            print("📝 Mock: Would add", len(documents), "documents")
            return True
            
        try:
            texts = []
            metadatas = []
            ids = []
            
            for i, doc in enumerate(documents):
                text = doc.get('content', '')
                metadata = doc.get('metadata', {})
                
                # Generate unique ID
                doc_id = hashlib.md5(f"{text[:100]}_{i}".encode()).hexdigest()
                
                texts.append(text)
                metadatas.append(metadata)
                ids.append(doc_id)
            
            # Get embeddings
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Added {len(documents)} documents to vector DB")
            return True
            
        except Exception as e:
            print(f"❌ Error adding documents: {e}")
            return False
    
    def search_similar(self, query: str, max_docs: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if not VECTOR_AVAILABLE:
            # Return mock results
            return [
                {
                    'content': f'Mock result for query: {query}',
                    'metadata': {'source': 'mock'},
                    'score': 0.9
                }
            ]
        
        try:
            # Get query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=max_docs
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'score': 1 - results['distances'][0][i] if results['distances'] else 0
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Error searching: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector database statistics"""
        if not VECTOR_AVAILABLE:
            return {
                'total_chunks': 0,
                'status': 'mock_mode'
            }
        
        try:
            count = self.collection.count()
            return {
                'total_chunks': count,
                'collection_name': 'documents',
                'embedding_model': 'all-MiniLM-L6-v2',
                'status': 'operational'
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {'total_chunks': 0, 'status': 'error'}
    
    def clear_all(self) -> bool:
        """Clear all documents from the database"""
        if not VECTOR_AVAILABLE:
            return True
            
        try:
            self.client.delete_collection("documents")
            self.collection = self.client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            print("✅ Vector database cleared")
            return True
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            return False
