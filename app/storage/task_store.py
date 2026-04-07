"""In-memory storage for tasks."""

from uuid import UUID

from app.models.task import Task, TaskPlan
from app.models.enums import TaskStatus


class TaskStore:
    """In-memory storage for tasks using a dictionary."""
    
    def __init__(self):
        self._tasks: dict[UUID, Task] = {}
        self._plans: dict[UUID, TaskPlan] = {}  # job_id -> TaskPlan
    
    def create_task(self, task: Task) -> Task:
        """Store a new task."""
        self._tasks[task.id] = task
        return task
    
    def get_task(self, task_id: UUID) -> Task | None:
        """Retrieve a task by ID."""
        return self._tasks.get(task_id)
    
    def update_task(self, task: Task) -> Task:
        """Update an existing task."""
        self._tasks[task.id] = task
        return task
    
    def update_task_status(self, task_id: UUID, status: TaskStatus) -> Task | None:
        """Update only the status of a task."""
        task = self.get_task(task_id)
        if task:
            task.status = status
            self._tasks[task_id] = task
        return task
    
    def get_tasks_by_job(self, job_id: UUID) -> list[Task]:
        """Get all tasks for a specific job."""
        return [t for t in self._tasks.values() if t.job_id == job_id]
    
    def create_plan(self, plan: TaskPlan) -> TaskPlan:
        """Store a task plan."""
        self._plans[plan.job_id] = plan
        # Also store individual tasks
        for task in plan.tasks:
            self._tasks[task.id] = task
        return plan
    
    def get_plan(self, job_id: UUID) -> TaskPlan | None:
        """Get the task plan for a job."""
        return self._plans.get(job_id)


# Singleton instance for dependency injection
task_store = TaskStore()


def get_task_store() -> TaskStore:
    """Dependency injection function for TaskStore."""
    return task_store
