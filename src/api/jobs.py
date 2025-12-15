"""Job management for background tasks."""
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Job:
    """Represents a background job."""
    status: str = "pending"
    progress: int = 0
    message: str = "Job queued"
    result_url: Optional[str] = None
    result_urls: Optional[dict[str, str]] = None
    error: Optional[str] = None
    airtable_record_id: Optional[str] = None


class JobManager:
    """Manages background job status."""
    
    def __init__(self):
        self._jobs: dict[str, Job] = {}
    
    def create(self, job_id: str) -> Job:
        """Create a new job."""
        job = Job()
        self._jobs[job_id] = job
        return job
    
    def get(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        return self._jobs.get(job_id)
    
    def update(
        self,
        job_id: str,
        status: Optional[str] = None,
        progress: Optional[int] = None,
        message: Optional[str] = None,
        result_url: Optional[str] = None,
        result_urls: Optional[dict[str, str]] = None,
        error: Optional[str] = None
    ) -> Optional[Job]:
        """Update job status."""
        job = self._jobs.get(job_id)
        if not job:
            return None
        
        if status is not None:
            job.status = status
        if progress is not None:
            job.progress = progress
        if message is not None:
            job.message = message
        if result_url is not None:
            job.result_url = result_url
        if result_urls is not None:
            job.result_urls = result_urls
        if error is not None:
            job.error = error
        
        return job
    
    def complete(
        self, 
        job_id: str, 
        result_url: str, 
        message: str = "Completed successfully",
        result_urls: Optional[dict[str, str]] = None
    ) -> Optional[Job]:
        """Mark job as completed."""
        return self.update(
            job_id,
            status="completed",
            progress=100,
            message=message,
            result_url=result_url,
            result_urls=result_urls
        )
    
    def fail(self, job_id: str, error: str) -> Optional[Job]:
        """Mark job as failed."""
        return self.update(
            job_id,
            status="failed",
            message=f"Failed: {error}",
            error=error
        )


# Global job manager instance
job_manager = JobManager()
