def create_plan(intent: str, entities: dict) -> list:
    """Takes an intent and maps it to a sequence of skills to execute."""
    if intent == "leave_request":
        return ["leave.request"]
    if intent == "leave_approval":
        return ["leave.approve"]
    if intent == "payroll_query":
        return ["payroll.query"]
    if intent == "onboarding_initiate":
        return ["onboarding.initiate", "docs.generate"]
        
    return []
