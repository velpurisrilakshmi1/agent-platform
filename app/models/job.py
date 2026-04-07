"""Job-related data models."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.models.enums import JobStatus


class JobInput(BaseModel):
    """Input data for creating a new job."""
    
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Input data for the job to process"
    )


class JobResult(BaseModel):
    """Result of a completed job."""
    
    job_id: UUID
    output: dict[str, Any] = Field(default_factory=dict)
    validated: bool = False
    validation_notes: str | None = None


class Job(BaseModel):
    """A job submitted to the orchestration platform."""
    
    id: UUID = Field(default_factory=uuid4)
    input_data: dict[str, Any] = Field(default_factory=dict)
    status: JobStatus = Field(default=JobStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    result: JobResult | None = None


class JobResponse(BaseModel):
    """API response for job information."""
    
    id: UUID
    status: JobStatus
    created_at: datetime
    input_data: dict[str, Any]
    result: JobResult | None = None


class JobCreateResponse(BaseModel):
    """API response when creating a new job."""
    
    id: UUID
    status: JobStatus
    message: str = "Job created successfully"
