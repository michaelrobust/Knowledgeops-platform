import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ No API key!")
    exit(1)

client = Groq(api_key=api_key)

# 測試不同的模型
models_to_test = [
    "llama3-8b-8192",      # Llama 3 8B
    "llama3-70b-8192",     # Llama 3 70B (更強大)
    "gemma-7b-it",         # Google Gemma
    "gemma2-9b-it",        # Gemma 2
    "llama-3.1-8b-instant", # Llama 3.1
    "llama-3.1-70b-versatile", # Llama 3.1 70B
    "llama-3.2-3b-preview",    # Llama 3.2 小模型
    "mixtral-8x7b-32768"   # 舊的（應該失敗）
]

print("Testing available Groq models:\n")

for model in models_to_test:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'hello' in one word"}],
            max_tokens=10,
            temperature=0
        )
        answer = response.choices[0].message.content
        print(f"✅ {model}: {answer}")
    except Exception as e:
        error_msg = str(e)
        if "decommissioned" in error_msg:
            print(f"❌ {model}: DECOMMISSIONED")
        elif "does not exist" in error_msg:
            print(f"❌ {model}: NOT FOUND")
        else:
            print(f"❌ {model}: {error_msg[:50]}...")

print("\n✅ Use one of the working models above!")
