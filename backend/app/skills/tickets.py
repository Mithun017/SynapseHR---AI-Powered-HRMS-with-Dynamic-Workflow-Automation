from app.skills.base import BaseSkill
from app.db.session import SessionLocal
from app.db.models import Ticket, User
from app.services.ui_generator import generate_ui, UIType
from sqlalchemy import desc

class TicketSkill(BaseSkill):
    @property
    def name(self):
        return "ticket.manage"

    def execute(self, user_id: int, user_role: str, inputs: dict) -> dict:
        db = SessionLocal()
        try:
            action = inputs.get("action", "list")
            
            # 1. CREATE TICKET
            if action == "create" or inputs.get("description"):
                category = inputs.get("category", "General")
                title = inputs.get("title", f"New {category} Request")
                desc_text = inputs.get("description", "No description provided.")
                
                new_ticket = Ticket(
                    user_id=user_id, 
                    category=category, 
                    title=title, 
                    description=desc_text,
                    status="Pending"
                )
                db.add(new_ticket)
                db.commit()
                return generate_ui(
                    UIType.TEXT, 
                    "Ticket Raised 🎫", 
                    {"text": f"Your ticket for '{title}' has been submitted and is currently 'Pending'."}
                )

            # 2. UPDATE TICKET (Manager/Admin Only)
            ticket_id = inputs.get("ticket_id")
            new_status = inputs.get("new_status")
            if action == "update" and ticket_id and new_status:
                if user_role not in ["manager", "admin"]:
                    return generate_ui(UIType.ERROR_CARD, "Permission Denied", {"message": "Only managers can update ticket status."})
                
                ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
                if ticket:
                    ticket.status = new_status
                    if inputs.get("notes"):
                        ticket.manager_notes = inputs.get("notes")
                    db.commit()
                    return generate_ui(UIType.TEXT, "Ticket Updated", {"text": f"Ticket #{ticket_id} status changed to {new_status}."})

            # 3. LIST TICKETS
            query = db.query(Ticket, User.name).join(User, Ticket.user_id == User.id)
            if user_role == "employee":
                query = query.filter(Ticket.user_id == user_id)
            
            results = query.order_by(desc(Ticket.created_at)).all()
            
            rows = []
            for t, employee_name in results:
                rows.append({
                    "ID": t.id,
                    "Employee": employee_name,
                    "Category": t.category,
                    "Title": t.title,
                    "Status": t.status,
                    "Created": t.created_at.strftime("%Y-%m-%d"),
                    "employee_name": employee_name,
                    "description": t.description,
                    "status": t.status,
                    "manager_notes": t.manager_notes
                })

            return generate_ui(
                UIType.TICKET_CARD, # Use multi-card or specific ticket type
                "Ticket Management", 
                {
                    "columns": ["ID", "Employee", "Category", "Title", "Status", "Created"],
                    "rows": rows
                }
            )
        finally:
            db.close()
