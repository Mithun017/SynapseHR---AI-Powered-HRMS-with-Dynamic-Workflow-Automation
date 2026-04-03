from app.skills.base import BaseSkill
from app.services.ui_generator import generate_ui, UIType
from app.db.session import SessionLocal
from app.db.models import User, ChatMessage
from app.rbac.roles import Role
from sqlalchemy import desc

class ConversationSkill(BaseSkill):
    @property
    def name(self):
        return "conversation.review"

    def execute(self, user_id: int, user_role: str, entities: dict) -> dict:
        db = SessionLocal()
        try:
            target_user_id = entities.get("target_user_id") or user_id
            
            # Check target user's role
            target_user = db.query(User).filter(User.id == target_user_id).first()
            if not target_user:
                return generate_ui(UIType.ERROR_CARD, "User Not Found", {"message": f"Could not find user with ID {target_user_id}"})

            # ROLE-BASED VISIBILITY LOGIC
            # 1. Employees can ONLY see their own.
            if user_role == Role.EMPLOYEE and user_id != target_user_id:
                return generate_ui(UIType.ERROR_CARD, "Permission Denied", {"message": "You can only view your own conversation history."})
            
            # 2. Managers/Admins can see Employees.
            # 3. But Managers/Admins CANNOT see other Managers/Admins (Hierarchy check).
            is_leadership = user_role in [Role.MANAGER, Role.HR_OPS, Role.ADMIN]
            target_is_leadership = target_user.role in [Role.MANAGER, Role.HR_OPS, Role.ADMIN]

            if is_leadership and target_is_leadership and user_id != target_user_id:
                 return generate_ui(UIType.ERROR_CARD, "Permission Denied", {"message": f"You do not have permission to view {target_user.role} conversations."})

            # Fetch messages
            messages = db.query(ChatMessage).filter(ChatMessage.user_id == target_user_id).order_by(desc(ChatMessage.timestamp)).limit(20).all()
            
            rows = []
            for m in messages:
                rows.append({
                    "Time": m.timestamp.strftime("%H:%M"),
                    "From": m.role.upper(),
                    "Content": m.content[:50] + "..." if len(m.content) > 50 else m.content
                })

            return generate_ui(
                UIType.TABLE_CARD,
                f"Chat History: {target_user.name}",
                {
                    "columns": ["Time", "From", "Content"],
                    "rows": rows
                }
            )
        finally:
            db.close()
