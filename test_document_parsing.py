from app.services.document_parser import parse_document, chunk_document

print("🔍 Testing document parsing...")

# 測試解析文字檔案
try:
    result = parse_document("storage/uploads/test.txt")
    print("✅ Document parsed successfully!")
    print(f"📄 File: {result['file_name']}")
    print(f"📊 Word count: {result['word_count']}")
    print(f"📝 Content preview: {result['content'][:100]}...")
    print(f"🔤 Character count: {result['char_count']}")
    print(f"📋 File type: {result['file_type']}")
    
    print("\n🧩 Testing chunking...")
    chunks = chunk_document("storage/uploads/test.txt", chunk_size=100, overlap=20)
    print(f"✅ Created {len(chunks)} chunks")
    if chunks:
        print(f"📝 First chunk: {chunks[0]['text'][:50]}...")
        
except Exception as e:
    print(f"❌ Error: {e}")
