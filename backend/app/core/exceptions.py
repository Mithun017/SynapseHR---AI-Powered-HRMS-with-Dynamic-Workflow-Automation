from fastapi import HTTPException

class SynapseException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class RBACException(SynapseException):
    def __init__(self, detail: str = "You do not have permission to access this resource."):
        super().__init__(status_code=403, detail=detail)

class ValidationException(SynapseException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class LLMException(SynapseException):
    def __init__(self, detail: str = "Error connecting to AI service."):
        super().__init__(status_code=502, detail=detail)

class DatabaseException(SynapseException):
    def __init__(self, detail: str = "Database operation failed."):
        super().__init__(status_code=500, detail=detail)
