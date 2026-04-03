import json
import os
from datetime import datetime
from app.services.llm_service import call_llm

def parse_intent(message: str, history: list, role: str) -> dict:
    """Uses LLM to parse intent, extract entities, and provide a confidence score."""
    
    current_date = datetime.now().strftime("%Y-%m-%d %A")
    
    prompt = f"""
    You are an AI-HR orchestrator for SynapseHR. You are extremely friendly, professional, and eager to help the user.
    Analyze the user's message and history to extract intent and entities.
    
    Current Date: {current_date}
    User Role: {role}
    
    Extracted Intents (one or more): 
    - ticket.manage, payroll.query, onboarding.initiate, employee.add, employee.list, analytics.stats, reports.generate, conversation.review, system.dashboard, unknown
    
    Special Logic:
    - If user says 'show employee chats', 'review conversations', 'see history for [name]', the intent is 'conversation.review'.
    - If user says 'make dashboard', 'build dashboard', 'show my workspace', the intent is 'system.dashboard'.
    - Based on User Role ({role}), the plan for 'system.dashboard' MUST be:
        - ADMIN: ["employee.list", "analytics.stats", "reports.generate"]
        - MANAGER: ["ticket.manage", "analytics.stats"]
        - EMPLOYEE: ["ticket.manage", "payroll.query"]
    - If user wants to "raise a ticket", "complain", "request leave", "salary issue", "project help", the intent is 'ticket.manage' with action 'create'.
    - If manager says "approve", "deny", "reject", the intent is 'ticket.manage' with action 'update'.
    - If the message starts with 'ACTION:', the message IS the intent. (e.g. 'ACTION:leave.request' means plan is ["leave.request"])
    
    Friendly Instructions:
    - If the user greets you ('hi', 'hello', 'hey'), set plan to ["unknown"], confidence to 1.0, and clarification_needed to true.
    - In the 'reasoning' field, provide a very warm welcome and ask specifically how you can help with HR tasks like leave, payroll, or onboarding.
    - KEEP IT PERSONAL. Use phrases like "I'd be happy to help you today!"

    Smart Extraction:
    - If user says 'tomorrow' relative to {current_date}, calculate the exact date.
    - If user says 'fever', 'sick', etc., map reason to 'Sick Leave'.
    - If user says 'vacation', 'trip', etc., map reason to 'Vacation'.

    Return JSON with:
    1. plan: List of strings (the skill names to execute)
    2. extracted_entities: (e.g. date, month, reason, name, role)
    3. confidence: (0.0 to 1.0)
    4. clarification_needed: (boolean)
    5. reasoning: (A friendly, helpful conversational response)

    User Message: "{message}"
    
    Example Output for "hi":
    {{
        "plan": ["unknown"],
        "extracted_entities": {{}},
        "confidence": 1.0,
        "clarification_needed": true,
        "reasoning": "Hi there! 👋 I'm your SynapseHR assistant. I'd love to help you today. Would you like to check your leave balance, view your latest payslip, or maybe start an onboarding process?"
    }}
    """
    
    if message.startswith("ACTION:"):
        action = message.replace("ACTION:", "").strip()
        return {
            "plan": [action],
            "extracted_entities": {},
            "confidence": 1.0,
            "clarification_needed": False,
            "reasoning": "Direct system action triggered."
        }
    
    try:
        raw_response = call_llm(prompt)
        clean_json = raw_response.strip()
        
        # More robust JSON extraction
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[-1].split("```")[0].strip()
        elif "```" in clean_json:
             clean_json = clean_json.split("```")[-1].split("```")[0].strip()
             
        # Remove any leading/trailing non-JSON characters like "Output:" or "Result:"
        if not clean_json.startswith("{") and "{" in clean_json:
            clean_json = clean_json[clean_json.find("{"):]
        if not clean_json.endswith("}") and "}" in clean_json:
            clean_json = clean_json[:clean_json.rfind("}")+1]
            
        parsed = json.loads(clean_json)
        
        # Ensure all required fields exist to prevent KeyError downstream
        return {
            "plan": parsed.get("plan", ["unknown"]),
            "extracted_entities": parsed.get("extracted_entities", {}),
            "confidence": parsed.get("confidence", 0.5),
            "clarification_needed": parsed.get("clarification_needed", False),
            "reasoning": parsed.get("reasoning", "Parsed by LLM.")
        }
    except Exception as e:
        print(f"LLM parsing failed: {e}. Raw response: {raw_response if 'raw_response' in locals() else 'None'}")
        # SIMPLE FALLBACK HEURISTIC
        msg_low = message.lower()
        if "workspace" in msg_low or "dashboard" in msg_low:
             dash_plan = ["ticket.manage", "payroll.query"]
             if role == "admin": dash_plan = ["employee.list", "analytics.stats", "reports.generate"]
             if role == "manager": dash_plan = ["ticket.manage", "analytics.stats"]
             return {"plan": dash_plan, "confidence": 1.0, "clarification_needed": False, "extracted_entities": {}, "reasoning": "Loading your personalized workspace..."}
        
        if "leave" in msg_low or "sick" in msg_low or "vacation" in msg_low:
             return {
                 "plan": ["ticket.manage"], 
                 "confidence": 0.9, 
                 "clarification_needed": False, 
                 "extracted_entities": {"category": "Leave", "action": "create"}, 
                 "reasoning": "I'd be happy to help with your leave appeal! I've prepared a request that will be sent to your manager for approval."
             }
        
        return {
            "plan": ["unknown"],
            "confidence": 0.1,
            "clarification_needed": True,
            "extracted_entities": {},
            "reasoning": "Hi there! 👋 I'm your SynapseHR assistant. I didn't quite catch that, but I'm here to help! Would you like to check your leave, view your payroll, or start an onboarding process?"
        }
