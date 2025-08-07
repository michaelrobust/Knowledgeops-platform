# 讀取並更新 document_parser.py
import re

with open('app/services/document_parser.py', 'r') as f:
    content = f.read()

# 找到 parse_document 方法
if 'def parse_document' in content:
    # 檢查是否已支援 PDF
    if '.pdf' not in content:
        print("Adding PDF support to parse_document...")
        
        # 在 parse_document 方法中加入 PDF 處理
        old_pattern = r"(def parse_document.*?:.*?\n.*?)(if.*?\.txt.*?:)"
        new_code = r"\1if file_path.lower().endswith('.pdf'):\n            return self.parse_pdf(file_path)\n        el\2"
        
        content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)
        
        with open('app/services/document_parser.py', 'w') as f:
            f.write(content)
        
        print("✅ PDF support added!")
    else:
        print("✅ PDF support already exists!")
else:
    print("❌ Could not find parse_document method")
