from app.skills.base import BaseSkill
from app.db.session import SessionLocal
from app.db.models import User, Payroll, Ticket
from app.services.ui_generator import generate_ui, UIType
from sqlalchemy import func

class ReportsSkill(BaseSkill):
    @property
    def name(self):
        return "reports.generate"

    def execute(self, user_id: int, user_role: str, entities: dict) -> dict:
        db = SessionLocal()
        try:
            total_employees = db.query(User).count()
            total_payroll = db.query(func.sum(Payroll.salary)).scalar() or 0.0
            pending_tickets = db.query(Ticket).filter(Ticket.status == "In Process").count()
            
            report_data = {
                "Total Employees": total_employees,
                "Monthly Payroll": f"${total_payroll:,.2f}",
                "Pending Requests": pending_tickets,
                "Generated At": func.now().label("now")
            }
            
            return generate_ui(
                UIType.TABLE_CARD,
                "Executive Summary Report",
                {
                    "columns": ["Metric", "Value"],
                    "rows": [
                        {"Metric": "Active Headcount", "Value": total_employees},
                        {"Metric": "Total Monthly Cost", "Value": f"${total_payroll:,.2f}"},
                        {"Metric": "Open Ticket Count", "Value": pending_tickets}
                    ]
                }
            )
        finally:
            db.close()
