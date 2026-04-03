import json
import httpx
from app.core.config import settings

def call_llm(prompt: str) -> str:
    # 1. Determine provider
    provider = settings.DEFAULT_LLM_PROVIDER.lower()
    
    # 2. Groq Logic
    if provider == "groq" and settings.GROQ_API_KEY:
        from groq import Groq
        with httpx.Client(proxy=None) as http_client:
            client = Groq(api_key=settings.GROQ_API_KEY, http_client=http_client)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return response.choices[0].message.content

    # 3. Gemini Logic
    if provider == "gemini" and settings.GEMINI_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)
        return response.text

    # Mock/Fallback
    return "Error: No LLM provider configured or available."
