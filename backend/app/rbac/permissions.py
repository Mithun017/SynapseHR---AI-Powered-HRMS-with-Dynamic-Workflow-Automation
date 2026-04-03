from app.rbac.roles import Role, ROLE_HIERARCHY
from app.core.exceptions import RBACException

def can_invoke(user_role: str, skill_name: str) -> bool:
    """Check if a role can invoke a specific skill."""
    # Ensure user_role is a string and handle Enum conversion if needed
    role_str = str(user_role).lower().split('.')[-1]
    
    permissions = {
        "ticket.manage": [Role.EMPLOYEE, Role.MANAGER, Role.HR_OPS, Role.ADMIN],
        "payroll.query": [Role.EMPLOYEE, Role.MANAGER, Role.HR_OPS, Role.ADMIN],
        "onboarding.initiate": [Role.HR_OPS, Role.ADMIN],
        "analytics.stats": [Role.MANAGER, Role.HR_OPS, Role.ADMIN],
        "employee.list": [Role.EMPLOYEE, Role.MANAGER, Role.HR_OPS, Role.ADMIN],
        "employee.add": [Role.HR_OPS, Role.ADMIN],
        "reports.generate": [Role.MANAGER, Role.HR_OPS, Role.ADMIN],
        "conversation.review": [Role.EMPLOYEE, Role.MANAGER, Role.HR_OPS, Role.ADMIN],
    }
    
    allowed_roles = [str(r).lower().split('.')[-1] for r in permissions.get(skill_name, [])]
    
    if role_str not in allowed_roles:
        raise RBACException(f"Role '{role_str}' cannot execute skill '{skill_name}'")
    return True

def can_manage_user(user_role: str, target_user_role: str):
    """
    Hierarchical oversight check.
    Managers/Admins can review Employees.
    """
    if user_role in [Role.MANAGER, Role.HR_OPS, Role.ADMIN] and target_user_role == Role.EMPLOYEE:
        return True
    return False

def can_access_employee(user_role: str, user_id: int, target_user_id: int) -> bool:
    """Data-scope permission check."""
    if user_role in [Role.HR_OPS, Role.ADMIN]:
        return True
    if user_id == target_user_id:
        return True
    
    if user_role == Role.MANAGER:
        return True
    
    raise RBACException(f"User {user_id} cannot access data for user {target_user_id}")
