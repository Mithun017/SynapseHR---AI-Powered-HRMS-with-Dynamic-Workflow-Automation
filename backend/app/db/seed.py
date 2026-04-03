from app.db.session import engine, Base, SessionLocal
from app.db.models import User, LeaveBalance, Payroll, Ticket

def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    users = [
        User(id=1, name="Mithun", role="employee", department="Engineering", password="emp1@123"),
        User(id=2, name="Sushma", role="manager", department="Management", password="manager@123"),
        User(id=3, name="Makesh", role="admin", department="HR", password="admin@123"),
    ]
    db.add_all(users)
    db.commit()

    balances = [
        LeaveBalance(user_id=1, total=20, used=2),
        LeaveBalance(user_id=2, total=25, used=5),
        LeaveBalance(user_id=3, total=30, used=0),
    ]
    db.add_all(balances)

    payrolls = [
        Payroll(user_id=1, month="April", salary=5000.0, tax=500.0, bonus=200.0),
        Payroll(user_id=2, month="April", salary=8000.0, tax=1200.0, bonus=500.0),
        Payroll(user_id=3, month="April", salary=7000.0, tax=1000.0, bonus=300.0),
    ]
    db.add_all(payrolls)
    
    tickets = [
        Ticket(user_id=1, category="Leave", title="Vacation Request", description="Family trip from 2024-04-10 to 2024-04-12", status="Approved"),
        Ticket(user_id=1, category="Salary", title="Salary Discrepancy", description="Bonus from March not reflected", status="Pending"),
        Ticket(user_id=2, category="Project", title="Resource Allocation", description="Need help with the Q2 roadmap", status="Approved"),
        Ticket(user_id=1, category="Project", title="Project Status Update", description="Monthly summary for the Adya project", status="Pending"),
    ]
    db.add_all(tickets)
    
    db.commit()
    db.close()
    print("Database seeded completely with Unified Tickets.")

if __name__ == "__main__":
    seed_data()
