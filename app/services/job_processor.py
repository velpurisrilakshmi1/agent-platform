"""Job processor that orchestrates the full pipeline."""

import logging
from uuid import UUID

from app.models import Job, JobResult, JobStatus
from app.storage.job_store import JobStore
from app.storage.task_store import TaskStore
from app.services.orchestrator import OrchestratorService
from app.services.worker import WorkerAgent

logger = logging.getLogger(__name__)


class JobProcessor:
    """
    Processes jobs through the complete pipeline:
    1. Create task plan (orchestrator)
    2. Execute tasks (worker + MCP)
    3. Validate output (RAI)
    4. Store result
    """
    
    def __init__(
        self, 
        job_store: JobStore, 
        task_store: TaskStore,
        use_mcp: bool = True
    ):
        self.job_store = job_store
        self.task_store = task_store
        self.use_mcp = use_mcp
        self.orchestrator = OrchestratorService(job_store, task_store)
    
    def process(self, job_id: UUID) -> JobResult:
        """
        Process a job through the full pipeline.
        
        Args:
            job_id: ID of the job to process
            
        Returns:
            JobResult with the validated output
        """
        logger.info(f"Processing job {job_id}")
        
        # Get the job
        job = self.job_store.get(job_id)
        if not job:
            logger.error(f"Job not found: {job_id}")
            raise ValueError(f"Job not found: {job_id}")
        
        try:
            # Step 1: Create task plan
            logger.info(f"Creating task plan for job {job_id}")
            plan = self.orchestrator.create_plan(job)
            logger.info(f"Created plan with {len(plan.tasks)} tasks")
            
            # Step 2: Execute all tasks
            logger.info(f"Executing tasks for job {job_id}")
            worker = WorkerAgent(self.task_store, use_mcp=self.use_mcp)
            results = worker.execute_all(plan.tasks)
            
            # Check if any task failed
            failed_tasks = [r for r in results if not r.success]
            if failed_tasks:
                logger.error(f"Job {job_id} failed: {failed_tasks[0].error}")
                self.job_store.update_status(job_id, JobStatus.FAILED)
                return JobResult(
                    job_id=job_id,
                    output={"error": failed_tasks[0].error},
                    validated=False,
                    validation_notes="Task execution failed"
                )
            
            # Step 3: Get final validated output
            final_output = worker.get_final_output()
            logger.info(f"Job {job_id} validated: {final_output.get('validated')}")
            
            # Step 4: Create and store result
            result = JobResult(
                job_id=job_id,
                output=final_output,
                validated=final_output.get("validated", False),
                validation_notes=final_output.get("validation_notes", "")
            )
            
            # Update job with result and status
            self.job_store.set_result(job_id, result)
            self.job_store.update_status(job_id, JobStatus.COMPLETED)
            
            logger.info(f"Job {job_id} completed successfully")
            return result
            
        except Exception as e:
            logger.exception(f"Job {job_id} failed with error: {e}")
            self.job_store.update_status(job_id, JobStatus.FAILED)
            return JobResult(
                job_id=job_id,
                output={"error": str(e)},
                validated=False,
                validation_notes=f"Processing failed: {str(e)}"
            )


# Singleton instance
_job_processor: JobProcessor | None = None


def get_job_processor(
    job_store: JobStore, 
    task_store: TaskStore
) -> JobProcessor:
    """Get or create the job processor."""
    global _job_processor
    if _job_processor is None:
        _job_processor = JobProcessor(job_store, task_store)
    return _job_processor
