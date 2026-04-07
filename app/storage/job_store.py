"""In-memory storage for jobs."""

from uuid import UUID

from app.models.job import Job, JobResult
from app.models.enums import JobStatus


class JobStore:
    """In-memory storage for jobs using a dictionary."""
    
    def __init__(self):
        self._jobs: dict[UUID, Job] = {}
    
    def create(self, job: Job) -> Job:
        """Store a new job."""
        self._jobs[job.id] = job
        return job
    
    def get(self, job_id: UUID) -> Job | None:
        """Retrieve a job by ID."""
        return self._jobs.get(job_id)
    
    def update(self, job: Job) -> Job:
        """Update an existing job."""
        self._jobs[job.id] = job
        return job
    
    def update_status(self, job_id: UUID, status: JobStatus) -> Job | None:
        """Update only the status of a job."""
        job = self.get(job_id)
        if job:
            job.status = status
            self._jobs[job_id] = job
        return job
    
    def set_result(self, job_id: UUID, result: JobResult) -> Job | None:
        """Set the result of a job."""
        job = self.get(job_id)
        if job:
            job.result = result
            self._jobs[job_id] = job
        return job
    
    def list_all(self) -> list[Job]:
        """Return all jobs."""
        return list(self._jobs.values())
    
    def delete(self, job_id: UUID) -> bool:
        """Delete a job by ID."""
        if job_id in self._jobs:
            del self._jobs[job_id]
            return True
        return False


# Singleton instance for dependency injection
job_store = JobStore()


def get_job_store() -> JobStore:
    """Dependency injection function for JobStore."""
    return job_store
