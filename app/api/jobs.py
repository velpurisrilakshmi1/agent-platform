"""Job API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.models import Job, JobInput, JobResponse, JobCreateResponse, JobStatus
from app.storage.job_store import JobStore, get_job_store

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobCreateResponse, status_code=201)
async def create_job(
    job_input: JobInput,
    store: JobStore = Depends(get_job_store),
) -> JobCreateResponse:
    """Submit a new job for processing."""
    job = Job(input_data=job_input.data)
    store.create(job)
    
    return JobCreateResponse(
        id=job.id,
        status=job.status,
        message="Job created successfully"
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
