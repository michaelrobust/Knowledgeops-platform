import sys
import os
sys.path.append(os.getcwd())

from app.services.vector_service import VectorService

print("🧪 Testing Vector Service")
print("=" * 40)

# 創建服務
vector_service = VectorService()
print(f"✅ Service created")

# 測試資料
test_docs = [
    {"text": "Artificial intelligence is the simulation of human intelligence", "source": "ai_guide.pdf", "page": 1},
    {"text": "Machine learning is a subset of AI that learns from data", "source": "ml_intro.pdf", "page": 1},
    {"text": "Deep learning uses neural networks with multiple layers", "source": "dl_basics.pdf", "page": 2},
]

# 添加文檔
print(f"\n📝 Adding {len(test_docs)} test documents...")
success = vector_service.add_documents(test_docs)
print(f"✅ Add result: {success}")

# 搜尋測試
test_queries = ["What is AI?", "How does machine learning work?"]
for query in test_queries:
    print(f"\n🔍 Searching: {query}")
    results = vector_service.search_similar(query, n_results=2)
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['source']} (page {result['page']}) - Score: {result['score']:.3f}")
        print(f"      Content: {result['content'][:80]}...")

# 統計資訊
stats = vector_service.get_stats()
print(f"\n📊 Database stats: {stats}")

print("\n🎉 Vector service test completed!")
