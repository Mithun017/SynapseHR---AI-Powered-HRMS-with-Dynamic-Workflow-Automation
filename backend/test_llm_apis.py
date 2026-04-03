import os
import time
import httpx
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def test_groq():
    print("\n--- Testing Groq API ---")
    api_key = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
    model_name = "llama-3.3-70b-versatile"
    
    try:
        # Explicitly create an httpx client without proxies to avoid issues
        with httpx.Client(proxy=None) as http_client:
            client = Groq(api_key=api_key, http_client=http_client)
            start = time.time()
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "Say hi in one word"}]
            )
            end = time.time()
            print(f"Model: {model_name}")
            print(f"Response: {response.choices[0].message.content}")
            print(f"Time taken: {end - start:.2f} seconds")
    except Exception as e:
        print(f"Groq API Error: {e}")

def test_gemini():
    print("\n--- Testing Gemini API ---")
    # Using the key found in the notebook as a fallback
    api_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
    model_name = "gemini-flash-latest"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        start = time.time()
        response = model.generate_content("Say hi in one word")
        end = time.time()
        print(f"Model: {model_name}")
        print(f"Response: {response.text.strip()}")
        print(f"Time taken: {end - start:.2f} seconds")
    except Exception as e:
        print(f"Gemini API Error: {e}")

if __name__ == "__main__":
    test_groq()
    test_gemini()
