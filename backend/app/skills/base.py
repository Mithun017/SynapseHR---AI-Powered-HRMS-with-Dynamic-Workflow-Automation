from abc import ABC, abstractmethod

class BaseSkill(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the skill."""
        pass
        
    @abstractmethod
    def execute(self, user_id: int, user_role: str, inputs: dict) -> dict:
        """Execute the skill."""
        pass
