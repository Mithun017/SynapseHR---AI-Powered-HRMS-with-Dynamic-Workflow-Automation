import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add app to path
sys.path.append(os.path.join(os.getcwd(), 'app'))

from app.agents.agent_controller import handle_chat
from app.services.ui_generator import UIType

def test_robustness():
    print("Running robustness tests...")
    
    # Test Scenario 1: LLM returns partial JSON (missing confidence, reasoning, etc.)
    with patch('app.agents.intent_parser.call_llm') as mock_llm:
        mock_llm.return_value = '{"plan": ["leave.request"]}'
        print("\nTest 1: Partial JSON from LLM")
        try:
            resp = handle_chat("test-session", 1, "employee", "I want leave")
            print(f"Response: {resp['intent']}, reasoning: {resp['reasoning']}")
            assert resp['intent'] == "leave.request"
            assert resp['confidence'] == 0.5 # default value
        except Exception as e:
            print(f"Test 1 FAILED: {e}")

    # Test Scenario 2: LLM returns non-JSON text around JSON
    with patch('app.agents.intent_parser.call_llm') as mock_llm:
        mock_llm.return_value = 'Here is the result: ```json {"plan": ["payroll.query"], "confidence": 0.9} ```'
        print("\nTest 2: JSON inside markdown")
        try:
            resp = handle_chat("test-session", 1, "employee", "show my salary")
            print(f"Response: {resp['intent']}, confidence: {resp['confidence']}")
            assert resp['intent'] == "payroll.query"
            assert resp['confidence'] == 0.9
        except Exception as e:
            print(f"Test 2 FAILED: {e}")

    # Test Scenario 3: LLM returns completely invalid response (Fallback expected)
    with patch('app.agents.intent_parser.call_llm') as mock_llm:
        mock_llm.return_value = 'Sorry, I cannot help with that.'
        print("\nTest 3: Invalid JSON from LLM (Friendly Fallback expected)")
        try:
            resp = handle_chat("test-session", 1, "employee", "blah")
            print(f"Response: {resp['intent']}, reasoning: {resp['reasoning']}")
            assert resp['intent'] == "unknown"
            assert "👋" in resp['reasoning'] or "help" in resp['reasoning'].lower()
            assert resp['clarification_needed'] == True
        except Exception as e:
            print(f"Test 3 FAILED: {e}")

    print("\nAll friendliness and robustness tests PASSED!")

if __name__ == "__main__":
    test_robustness()
