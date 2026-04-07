"""FastAPI application entry point."""

from fastapi import FastAPI

from app.config import settings
from app.api.jobs import router as jobs_router

app = FastAPI(
    title=settings.app_name,
    description="Autonomous Agent Orchestration Platform MVP",
    version="0.1.0",
)

# Include routers
app.include_router(jobs_router)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {"message": "Agent Platform is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.app_name}
