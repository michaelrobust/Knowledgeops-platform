import os
from dotenv import load_dotenv
from groq import Groq

# 載入 .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"✅ API Key loaded: {api_key[:20]}...")

try:
    client = Groq(api_key=api_key)
    
    # 快速測試
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "user", "content": "Say 'Groq is working!' in 5 words or less"}
        ],
        max_tokens=20
    )
    
    print(f"🤖 Groq says: {response.choices[0].message.content}")
    print("✅ SUCCESS - Groq API is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check if your API key is valid")
