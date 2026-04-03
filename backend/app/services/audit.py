from app.db.session import SessionLocal
from app.db.models import AuditLog

def log_audit(user_id: int, skill: str, action: str, result: str):
    db = SessionLocal()
    try:
        log = AuditLog(user_id=user_id, skill=skill, action=action, result=result)
        db.add(log)
        db.commit()
    finally:
        db.close()
