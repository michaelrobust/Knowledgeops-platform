print("=== Final Vector Service Test ===\n")

import sys
# 清除快取
for module in list(sys.modules.keys()):
    if 'vector_service' in module:
        del sys.modules[module]

from app.services.vector_service import VectorService

print("Initializing Vector Service...")
vs = VectorService()

print("\nTesting add documents...")
test_docs = [{
    "content": "Python is a great programming language for AI and machine learning.",
    "metadata": {"source": "test.txt", "page": 1}
}]
vs.add_documents(test_docs)

print("\nTesting search...")
results = vs.search_similar("Python programming", max_docs=1)
if results:
    print(f"✅ Found {len(results)} results")
    print(f"First result score: {results[0].get('score', 0):.2f}")
else:
    print("❌ No results found")

print("\nGetting stats...")
stats = vs.get_stats()
print(f"Stats: {stats}")

if stats.get('status') == 'operational':
    print("\n🎉 SUCCESS! Vector service is fully operational!")
else:
    print("\n⚠️ Vector service status:", stats.get('status'))
