from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String, index=True)  # employee, manager, hr_ops, admin
    department = Column(String)
    password = Column(String, default="password123") # Mock password

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)  # Leave, Payroll, Project, Other
    title = Column(String)
    description = Column(String)
    status = Column(String, default="In Process")  # Approved, Denied, In Process
    manager_notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class LeaveBalance(Base):
    __tablename__ = "leave_balances"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Integer, default=20)
    used = Column(Integer, default=0)
    user = relationship("User")

class Payroll(Base):
    __tablename__ = "payrolls"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    month = Column(String)
    salary = Column(Float)
    tax = Column(Float, default=0.0)
    bonus = Column(Float, default=0.0)
    status = Column(String, default="paid")
    user = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    skill = Column(String)
    action = Column(String)
    result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # user, assistant
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task = Column(String)
    status = Column(String, default="pending")
    user = relationship("User")
