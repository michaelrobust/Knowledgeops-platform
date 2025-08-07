import os
from app.services.vector_service import VectorService
from app.services.document_parser import DocumentParser

# Initialize services
vs = VectorService()
parser = DocumentParser()

# Clear old data
vs.clear_all()
print("✅ Cleared old data")

# Process all txt files in storage
storage_dir = "storage"
txt_files = [f for f in os.listdir(storage_dir) if f.endswith('.txt')]

print(f"\n📄 Found {len(txt_files)} text files to process:")
for file in txt_files:
    print(f"  - {file}")

total_chunks = 0

for filename in txt_files:
    filepath = os.path.join(storage_dir, filename)
    print(f"\n📝 Processing: {filename}")
    
    try:
        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create chunks
        chunks = []
        chunk_size = 500
        overlap = 50
        
        for i in range(0, len(content), chunk_size - overlap):
            chunk_text = content[i:i + chunk_size]
            if chunk_text.strip():
                chunks.append({
                    "content": chunk_text.strip(),
                    "metadata": {
                        "filename": filename,
                        "chunk_index": len(chunks),
                        "source_file": filename
                    }
                })
        
        # Add to vector database
        if chunks:
            vs.add_documents(chunks)
            print(f"  ✅ Added {len(chunks)} chunks from {filename}")
            total_chunks += len(chunks)
        
    except Exception as e:
        print(f"  ❌ Error processing {filename}: {e}")

# Verify
final_stats = vs.get_stats()
print(f"\n🎉 Processing complete!")
print(f"Total chunks in database: {final_stats.get('total_chunks', 0)}")

# Test search
print("\n🔍 Testing search...")
test_results = vs.search_similar("Python best practices", 3)
if test_results:
    print(f"✅ Search working! Found {len(test_results)} results")
    print(f"First result: {test_results[0].get('content', '')[:100]}...")
else:
    print("❌ Search not working - no results found")
