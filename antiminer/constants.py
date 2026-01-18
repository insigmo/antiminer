from enum import Enum

class TaskType(Enum):
    IO = "IO"
    CPU = "CPU"

class IssueStatus(Enum):
    PENDING = "PENDING"
    FIXED = "FIXED"
    FAILED = "FAILED"
