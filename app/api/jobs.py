"""Job API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.models import Job, JobInput, JobResponse, JobCreateResponse, JobStatus
from app.storage.job_store import JobStore, get_job_store
from app.storage.task_store import TaskStore, get_task_store
from app.services.job_processor import JobProcessor

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_processor(
    job_store: JobStore = Depends(get_job_store),
    task_store: TaskStore = Depends(get_task_store),
) -> JobProcessor:
    """Dependency for job processor."""
    return JobProcessor(job_store, task_store)


@router.post("", response_model=JobResponse, status_code=201)
async def create_job(
    job_input: JobInput,
    store: JobStore = Depends(get_job_store),
    processor: JobProcessor = Depends(get_processor),
) -> JobResponse:
    """Submit a new job for processing. Runs the full pipeline synchronously."""
    # Create the job
    job = Job(input_data=job_input.data)
    store.create(job)
    
    # Process the job through the full pipeline
    processor.process(job.id)
    
    # Get updated job with result
    job = store.get(job.id)
    
    return JobResponse(
        id=job.id,
        status=job.status,
        created_at=job.created_at,
        input_data=job.input_data,
        result=job.result,
    )


@router.get("", response_model=list[JobResponse])
async def list_jobs(
    store: JobStore = Depends(get_job_store),
) -> list[JobResponse]:
    """List all jobs."""
    jobs = store.list_all()
    return [
        JobResponse(
            id=job.id,
            status=job.status,
            created_at=job.created_at,
            input_data=job.input_data,
            result=job.result,
        )
        for job in jobs
    ]


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    store: JobStore = Depends(get_job_store),
) -> JobResponse:
    """Get a specific job by ID."""
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResponse(
        id=job.id,
        status=job.status,
        created_at=job.created_at,
        input_data=job.input_data,
        result=job.result,
    )
