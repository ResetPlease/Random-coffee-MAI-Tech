from enum import StrEnum, auto




class IncrbyConditionType(StrEnum):
    ALWAYS = auto()
    NEVER = auto()
    SUCCESS = auto()
    ERROR = auto()
    
    
class UnblockConditionType(StrEnum):
    SUCCESS = auto()
    NEVER = auto()