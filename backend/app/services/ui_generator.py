import json
from enum import Enum

class UIType(str, Enum):
    LEAVE_CARD = "LEAVE_CARD"
    PAYROLL_CARD = "PAYROLL_CARD"
    ONBOARDING_CARD = "ONBOARDING_CARD"
    TICKET_CARD = "TICKET_CARD"
    FORM_CARD = "FORM_CARD"
    ERROR_CARD = "ERROR_CARD"
    TABLE_CARD = "TABLE_CARD"
    CHART_CARD = "CHART_CARD"
    TEXT = "TEXT"

def generate_ui(ui_type: UIType, title: str, data: dict, actions: list = None):
    return {
        "type": ui_type.value,
        "title": title,
        "data": data,
        "actions": actions or []
    }
