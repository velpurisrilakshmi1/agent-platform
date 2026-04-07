"""Orchestrator service for creating task plans."""

from app.models import Job, Task, TaskPlan, TaskType, JobStatus
from app.storage.job_store import JobStore
from app.storage.task_store import TaskStore


class OrchestratorService:
    """Creates fixed task plans from jobs."""
    
    def __init__(self, job_store: JobStore, task_store: TaskStore):
        self.job_store = job_store
        self.task_store = task_store
    
    def create_plan(self, job: Job) -> TaskPlan:
        """
        Create a fixed task plan for a job.
        
        The MVP plan is always:
        1. fetch_context - Get context from MCP server
        2. process - Process the input with context
        3. validate - Validate the output with RAI service
        """
        tasks = [
            Task(
                job_id=job.id,
                type=TaskType.FETCH_CONTEXT,
                input={"query": job.input_data.get("query", "")},
            ),
            Task(
                job_id=job.id,
                type=TaskType.PROCESS,
                input={},  # Will receive context from previous task
            ),
            Task(
                job_id=job.id,
                type=TaskType.VALIDATE,
                input={},  # Will receive output from previous task
            ),
        ]
        
        plan = TaskPlan(job_id=job.id, tasks=tasks)
        
        # Store the plan and tasks
        self.task_store.create_plan(plan)
        
        # Update job status to running
        self.job_store.update_status(job.id, JobStatus.RUNNING)
        
        return plan
    
    def get_plan(self, job_id) -> TaskPlan | None:
        """Retrieve the task plan for a job."""
        return self.task_store.get_plan(job_id)
