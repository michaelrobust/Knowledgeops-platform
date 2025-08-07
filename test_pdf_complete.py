from app.services.document_parser import DocumentParser
import os

print("=== Testing PDF Support in DocumentParser ===\n")

parser = DocumentParser()

# 測試 PDF 檔案
pdf_file = "test_python_guide.pdf"

if os.path.exists(pdf_file):
    print(f"Testing: {pdf_file}")
    result = parser.parse_document(pdf_file)
    
    if result.get('success'):
        print("✅ PDF parsing successful!")
        print(f"Content length: {len(result.get('content', ''))} characters")
        print(f"\nFirst 300 characters of content:")
        print("-" * 40)
        print(result.get('content', '')[:300])
        print("-" * 40)
        print(f"\nMetadata: {result.get('metadata', {})}")
    else:
        print(f"❌ PDF parsing failed: {result}")
else:
    print(f"❌ {pdf_file} not found")

# 列出所有 PDF 檔案
print("\n=== Available PDF files ===")
for file in os.listdir('.'):
    if file.endswith('.pdf'):
        print(f"  - {file}")

for file in os.listdir('storage'):
    if file.endswith('.pdf'):
        print(f"  - storage/{file}")
