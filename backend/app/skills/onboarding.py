from app.skills.base import BaseSkill
from app.db.session import SessionLocal
from app.db.models import OnboardingTask
from app.services.ui_generator import generate_ui, UIType
from app.services.audit import log_audit

class OnboardingInitiateSkill(BaseSkill):
    @property
    def name(self):
        return "onboarding.initiate"

    def execute(self, user_id: int, user_role: str, inputs: dict) -> dict:
        target_user_id = inputs.get("target_user_id")
        
        db = SessionLocal()
        try:
            # Fetch tasks for this user to show current progress
            user_tasks = db.query(OnboardingTask).filter(OnboardingTask.user_id == target_user_id).all()
            task_list = [t.task for t in user_tasks] if user_tasks else ["Setup Email", "Provide Laptop", "Sign NDA"]
            
            return generate_ui(
                ui_type=UIType.ONBOARDING_CARD,
                title="Employee Onboarding",
                data={"target_user_id": target_user_id, "tasks": task_list, "status": "active"}
            )
        finally:
            db.close()
