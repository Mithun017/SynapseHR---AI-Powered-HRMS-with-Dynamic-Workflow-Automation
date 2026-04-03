from enum import Enum

class Role(str, Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    HR_OPS = "hr_ops"
    ADMIN = "admin"

ROLE_HIERARCHY = {
    Role.EMPLOYEE: 1,
    Role.MANAGER: 2,
    Role.HR_OPS: 3,
    Role.ADMIN: 4,
}
