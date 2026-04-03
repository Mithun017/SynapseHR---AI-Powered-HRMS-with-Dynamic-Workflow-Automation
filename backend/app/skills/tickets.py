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
                desc_text = inputs.get("description", f"Appeal for {category}")
                
                new_ticket = Ticket(
                    user_id=user_id, 
                    category=category, 
                    title=title, 
                    description=desc_text,
                    status="Pending"
                )
                db.add(new_ticket)
                db.commit()
                db.refresh(new_ticket)
                
                return generate_ui(
                    UIType.TICKET_CARD, 
                    "Request Submitted 🎫", 
                    {
                        "id": new_ticket.id,
                        "category": new_ticket.category,
                        "status": new_ticket.status,
                        "title": new_ticket.title,
                        "description": new_ticket.description
                    }
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
                    db.refresh(ticket)
                    return generate_ui(
                        UIType.TICKET_CARD, 
                        "Status Updated ✅", 
                        {
                            "id": ticket.id,
                            "category": ticket.category,
                            "status": ticket.status,
                            "title": ticket.title,
                            "description": ticket.description,
                            "manager_notes": ticket.manager_notes
                        }
                    )

            # 3. LIST TICKETS
            query = db.query(Ticket, User.name).join(User, Ticket.user_id == User.id)
            if user_role == "employee":
                query = query.filter(Ticket.user_id == user_id)
            
            results = query.order_by(desc(Ticket.created_at)).all()
            
            is_manager = user_role in ["manager", "admin"]
            
            final_cards = []
            for t, employee_name in results:
                final_cards.append(generate_ui(
                    UIType.TICKET_CARD,
                    f"Ticket #{t.id}", 
                    {
                        "id": t.id,
                        "employee_name": employee_name,
                        "category": t.category,
                        "status": t.status,
                        "title": t.title,
                        "description": t.description,
                        "manager_notes": t.manager_notes,
                        "can_approve": is_manager # Authoritative UI Guard
                    }
                ))

            # Return list of cards (App.jsx will handle it)
            return final_cards if final_cards else generate_ui(UIType.TEXT, "No Tickets", {"text": "You don't have any active tickets at this time."})
        finally:
            db.close()
