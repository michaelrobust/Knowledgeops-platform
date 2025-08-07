import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"1. API Key loaded: {api_key[:20] if api_key else 'NOT FOUND'}...")

if not api_key:
    print("❌ No API key in .env file!")
    print("Run: echo 'GROQ_API_KEY=your-key' > .env")
    exit(1)

try:
    print("2. Creating Groq client...")
    client = Groq(api_key=api_key)
    
    print("3. Testing API call...")
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "user", "content": "Say 'Groq works!' in exactly 3 words"}
        ],
        max_tokens=10
    )
    
    answer = response.choices[0].message.content
    print(f"✅ Groq Response: {answer}")
    print("✅ GROQ API IS WORKING!")
    
except Exception as e:
    print(f"❌ Groq Error: {e}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. Network connection")
    print("3. Groq service down")
