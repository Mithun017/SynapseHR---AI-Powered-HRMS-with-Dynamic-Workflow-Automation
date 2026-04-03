from app.agents.memory import get_session, append_history, reset_session
from app.agents.intent_parser import parse_intent
from app.agents.planner import create_plan
from app.rbac.permissions import can_invoke, can_manage_user
from app.core.exceptions import RBACException
from app.services.ui_generator import generate_ui, UIType

# Import skills
from app.skills.tickets import TicketSkill
from app.skills.payroll import PayrollQuerySkill
from app.skills.onboarding import OnboardingInitiateSkill
from app.skills.admin import AdminSkill
from app.skills.analytics import AnalyticsSkill
from app.skills.reports import ReportsSkill
from app.skills.conversation import ConversationSkill
from app.db.models import User, ChatMessage
from app.db.session import SessionLocal

SKILL_REGISTRY = {
    "ticket.manage": TicketSkill(),
    "payroll.query": PayrollQuerySkill(),
    "onboarding.initiate": OnboardingInitiateSkill(),
    "employee.add": AdminSkill(),
    "employee.list": AdminSkill(),
    "analytics.stats": AnalyticsSkill(),
    "reports.generate": ReportsSkill(),
    "conversation.review": ConversationSkill()
}

def handle_chat(session_id: str, user_id: int, user_role: str, message: str) -> dict:
    session = get_session(session_id)
    if session.get("user_id") and session["user_id"] != user_id:
        print(f"RBAC: Identity Switched in session {session_id}. Resetting history.")
        reset_session(session_id)
        session = get_session(session_id) # Fresh session
        
    session["user_id"] = user_id
    append_history(session_id, {"role": "user", "content": message})
    
    # 0. FETCH AUTHORITATIVE ROLE FROM DB
    db = SessionLocal()
    try:
        user_record = db.query(User).filter(User.id == user_id).first()
        if user_record:
            user_role = user_record.role.lower() # Authoritative Override
            print(f"RBAC: Overriding session role with DB role: {user_role} for user {user_id}")
            
        # Log User Message
        user_msg = ChatMessage(user_id=user_id, role="user", content=message)
        db.add(user_msg)
        db.commit()
    except Exception as e:
        print(f"RBAC/DB Error: {e}")
    finally:
        db.close()
    
    # 1. Parse intent & Multi-step Plan
    try:
        parsed = parse_intent(message, session["history"], user_role)
    except Exception as e:
        print(f"Critical error in parse_intent: {e}")
        parsed = {"plan": ["unknown"], "confidence": 0.0, "reasoning": "System error during parsing.", "clarification_needed": True, "extracted_entities": {}}
        
    plan = parsed.get("plan", ["unknown"])
    
    # 2. Clarification logic
    if parsed.get("clarification_needed"):
        return {
            "intent": plan[0] if plan else "unknown",
            "confidence": parsed.get("confidence", 0.0),
            "reasoning": parsed.get("reasoning", "I'd love to help you with that! Could you provide a bit more detail?"),
            "clarification_needed": True,
            "actions": [],
            "ui": generate_ui(UIType.FORM_CARD, "I'm here to help! 👋", {"message": parsed.get("reasoning", "How can I assist you today?"), "fields": ["date", "reason"]})
        }
        
    if "unknown" in plan:
          return {
            "intent": "unknown",
            "confidence": parsed.get("confidence", 0.0),
            "reasoning": parsed.get("reasoning", "I'm your SynapseHR assistant! I can help you with leave requests, payroll queries, or onboarding. What would you like to do?"),
            "clarification_needed": True,
            "actions": [],
            "ui": generate_ui(UIType.TEXT, "Welcome to SynapseHR 🤗", {"text": "I'm here to make your HR tasks easier. You can ask me things like 'I want to apply for leave tomorrow' or 'Show me my last payslip'."})
          }
         
    # 3. Execution Loop (Multi-Step)
    final_uis = []
    execution_actions = []
    is_dashboard = "system.dashboard" in plan or message.lower() in ["show my workspace", "dashboard"]
    
    for skill_name in plan:
        try:
            # RBAC Check
            can_invoke(user_role, skill_name)
            
            # Execute Skill
            skill = SKILL_REGISTRY.get(skill_name)
            if skill:
                 result_ui = skill.execute(user_id, user_role, parsed.get("extracted_entities", {}))
                 execution_actions.append(f"{skill_name} completed")
                 if result_ui:
                     final_uis.append(result_ui)
            else:
                 execution_actions.append(f"Skipped {skill_name} (not implemented)")
                 
        except RBACException as e:
            execution_actions.append(f"Blocked {skill_name} by RBAC")
            # If it's the dashboard, we don't want to show ugly error cards for missing permissions
            if not is_dashboard:
                final_uis.append(generate_ui(UIType.ERROR_CARD, "Permission Denied", {"message": str(e)}))
        except Exception as e:
            print(f"Error during skill execution ({skill_name}): {e}")
            final_uis.append(generate_ui(UIType.ERROR_CARD, "System Error", {"message": f"Skill '{skill_name}' failed: {str(e)}"}))
            execution_actions.append(f"Execution failed: {str(e)}")
        
    # Return the last UI if only one, or the list if multiple
    ui_to_return = final_uis[0] if len(final_uis) == 1 else (final_uis if len(final_uis) > 1 else None)
    if not ui_to_return:
        ui_to_return = generate_ui(UIType.TEXT, "SynapseHR Assistant", {"text": "I've processed your request, but there's no specific visual feedback for this action."})

    # 4. Persist Assistant Message to DB
    assistant_content = parsed.get("reasoning", "Processed successfully.")
    db = SessionLocal()
    try:
        asst_msg = ChatMessage(user_id=user_id, role="assistant", content=assistant_content)
        db.add(asst_msg)
        db.commit()
    except Exception as e:
        print(f"Error saving assistant message: {e}")
    finally:
        db.close()

    return {
        "intent": ", ".join(plan),
        "confidence": parsed.get("confidence", 0.0),
        "reasoning": assistant_content,
        "clarification_needed": False,
        "actions": execution_actions,
        "ui": ui_to_return,
        "message": f"Successfully processed your request: {', '.join(execution_actions)}"
    }
