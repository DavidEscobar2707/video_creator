"""Health check routes."""
import time
from fastapi import APIRouter

from src.core.config import settings
from src.api.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "AI Influencer Video Generator API",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "character": "/api/v1/character/generate",
            "video": "/api/v1/video/generate",
            "voiceover": "/api/v1/voiceover/generate",
            "job_status": "/api/v1/job/{job_id}",
            "download": "/api/v1/download/{filename}"
        }
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        api_key_configured=bool(settings.gemini_api_key),
        airtable_enabled=settings.airtable_enabled,
        timestamp=time.time()
    )
