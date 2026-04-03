import httpx
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n--- Testing Health Check ---")
    try:
        response = httpx.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_chat(message, role="EMPLOYEE", user_id=1):
    print(f"\n--- Testing Chat: '{message}' (Role: {role}) ---")
    payload = {
        "message": message,
        "user_id": user_id,
        "role": role,
        "session_id": "test_session"
    }
    try:
        response = httpx.post(f"{BASE_URL}/api/agent/chat", json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Intent: {data.get('intent')}")
        print(f"Reasoning: {data.get('reasoning')}")
        ui = data.get('ui')
        if ui:
            print(f"UI Type: {ui.get('type')}")
        else:
            print("No UI generated.")
    except Exception as e:
        print(f"Chat failed: {e}")

if __name__ == "__main__":
    test_health()
    
    # Test cases for each skill
    test_chat("I want to take leave tomorrow due to fever.") # Leave
    test_chat("Show me my workspace dashboard.", role="MANAGER") # Dashboard Manager
    test_chat("Who is onboarding currently?", role="ADMIN") # Onboarding
    test_chat("What is my current salary?", role="EMPLOYEE") # Payroll
    test_chat("Tell me a joke") # Unknown/Clarification
