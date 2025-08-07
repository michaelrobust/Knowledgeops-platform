from pypdf import PdfReader
import os

# 測試 PyPDF 是否正常工作
print("Testing PDF parsing capability...\n")

# 如果有測試 PDF
if os.path.exists("test_python_guide.pdf"):
    try:
        reader = PdfReader("test_python_guide.pdf")
        
        print(f"✅ PDF loaded successfully!")
        print(f"Number of pages: {len(reader.pages)}")
        
        # 提取第一頁文字
        first_page = reader.pages[0]
        text = first_page.extract_text()
        
        print(f"\nFirst page content (first 200 chars):")
        print(text[:200])
        
        print("\n✅ PDF parsing works!")
        
    except Exception as e:
        print(f"❌ Error parsing PDF: {e}")
else:
    print("❌ No test PDF found. Create one first.")

# 測試 DocumentParser 對 PDF 的支援
print("\n" + "="*50)
print("Testing DocumentParser with PDF...\n")

try:
    from app.services.document_parser import DocumentParser
    
    parser = DocumentParser()
    
    # 檢查 parser 是否支援 PDF
    if hasattr(parser, 'parse_pdf'):
        print("✅ DocumentParser has PDF support")
    else:
        print("⚠️ DocumentParser might need PDF support added")
        
except Exception as e:
    print(f"Error testing DocumentParser: {e}")
