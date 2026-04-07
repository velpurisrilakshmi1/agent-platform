"""Status enums for jobs and tasks."""

from enum import Enum


class JobStatus(str, Enum):
    """Status of a job in the pipeline."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(str, Enum):
    """Status of an individual task."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskType(str, Enum):
    """Types of tasks that can be executed."""
    
    FETCH_CONTEXT = "fetch_context"
    PROCESS = "process"
    VALIDATE = "validate"
