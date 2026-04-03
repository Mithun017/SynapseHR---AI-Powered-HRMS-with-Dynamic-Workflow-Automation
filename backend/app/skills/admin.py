from app.skills.base import BaseSkill
from app.services.ui_generator import generate_ui, UIType
from app.db.session import SessionLocal
from app.db.models import User

class AdminSkill(BaseSkill):
    @property
    def name(self):
        return "employee.add"

    def execute(self, user_id: int, user_role: str, entities: dict) -> dict:
        db = SessionLocal()
        try:
            # If we're adding a user
            if entities.get("name"):
                name = entities.get("name")
                role = entities.get("role", "employee").lower()
                dept = entities.get("department", "General")
                
                new_user = User(
                    name=name, 
                    role=role, 
                    department=dept,
                    password="password123" # Default password
                )
                db.add(new_user)
                db.commit()
                
                return generate_ui(
                    UIType.TEXT,
                    "Employee Created ✅",
                    {"text": f"Successfully created {role} record for {name} in {dept}. Initial password: password123"}
                )
                
            # Default: List users (employee.list)
            users = db.query(User).all()
            rows = [{"Name": u.name, "Role": u.role, "Department": u.department} for u in users]
            
            return generate_ui(
                UIType.TABLE_CARD,
                "Company Directory",
                {
                    "columns": ["Name", "Role", "Department"],
                    "rows": rows
                }
            )
        finally:
            db.close()
