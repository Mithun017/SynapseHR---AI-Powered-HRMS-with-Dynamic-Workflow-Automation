from app.skills.base import BaseSkill
from app.services.ui_generator import generate_ui, UIType
from app.db.session import SessionLocal
from app.db.models import Ticket, User
from sqlalchemy import func

class AnalyticsSkill(BaseSkill):
    @property
    def name(self):
        return "analytics.stats"

    def execute(self, user_id: int, user_role: str, entities: dict) -> dict:
        db = SessionLocal()
        try:
            # Aggregate Ticket Categories
            stats = db.query(
                Ticket.category, 
                func.count(Ticket.id)
            ).group_by(Ticket.category).all()
            
            chart_data = [{"label": row[0] or "General", "value": row[1]} for row in stats]
            
            if not chart_data:
                chart_data = [{"label": "No Active Tickets", "value": 0}]

            return generate_ui(
                UIType.CHART_CARD,
                "Request Distribution 📊",
                {
                    "type": "pie",
                    "data": chart_data,
                    "summary": f"Total tickets in system: {len(db.query(Ticket).all())}"
                }
            )
        finally:
            db.close()
