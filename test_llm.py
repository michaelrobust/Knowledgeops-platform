import sys
import os

# 確保可以找到 app 模組
sys.path.append(os.getcwd())

try:
    from app.services.llm_service import LLMService
    print("✅ LLM Service imported successfully!")
    
    # 測試初始化
    llm = LLMService()
    print("✅ LLM Service instance created!")
    print(f"📄 Model: {llm.model}")
    print(f"🔧 API Available: {llm.client is not None}")
    
    # 簡單測試（如果有 API key）
    if hasattr(llm, 'test_connection'):
        result = llm.test_connection()
        print(f"🌐 Connection test: {result}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"⚠️ Other error: {e}")
