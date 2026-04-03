from app.skills.base import BaseSkill
from app.db.session import SessionLocal
from app.db.models import Payroll
from app.services.ui_generator import generate_ui, UIType
from app.services.audit import log_audit

class PayrollQuerySkill(BaseSkill):
    @property
    def name(self):
        return "payroll.query"

    def execute(self, user_id: int, user_role: str, inputs: dict) -> dict:
        month = inputs.get("month", "April")
        
        db = SessionLocal()
        try:
            payroll = db.query(Payroll).filter(Payroll.user_id == user_id, Payroll.month == month).first()
            if not payroll:
                return generate_ui(
                    ui_type=UIType.ERROR_CARD,
                    title="Payroll Data Not Found",
                    data={"message": f"No records found for {month}."}
                )
            
            log_audit(user_id, self.name, f"Queried payroll for {month}", "Success")
            
            return generate_ui(
                ui_type=UIType.PAYROLL_CARD,
                title=f"Payslip: {month}",
                data={"salary": f"${payroll.salary}", "status": payroll.status, "month": month}
            )
        finally:
            db.close()
