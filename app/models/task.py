"""Task-related data models."""

from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.models.enums import TaskStatus, TaskType


class Task(BaseModel):
    """An individual task within a job's task plan."""
    
    id: UUID = Field(default_factory=uuid4)
    job_id: UUID
    type: TaskType
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] | None = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    error: str | None = None


class TaskPlan(BaseModel):
    """A plan containing all tasks for a job."""
    
    job_id: UUID
    tasks: list[Task] = Field(default_factory=list)


class TaskResult(BaseModel):
    """Result of executing a task."""
    
    task_id: UUID
    success: bool
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
