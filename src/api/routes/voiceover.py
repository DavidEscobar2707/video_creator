"""Voiceover generation routes."""
import uuid
from fastapi import APIRouter, BackgroundTasks, Form

from src.core import AudioGenerator, settings
from src.api.schemas import JobStatus
from src.api.jobs import job_manager

router = APIRouter(prefix="/api/v1/voiceover", tags=["Voiceover"])


@router.post("/generate", response_model=JobStatus)
async def generate_voiceover(
    background_tasks: BackgroundTasks,
    script: str = Form(...),
    language: str = Form("en")
):
    """
    Generate voiceover audio.
    
    - **script**: Voiceover script text
    - **language**: Language code (en, es, fr, etc.)
    
    Returns job_id to track progress.
    """
    job_id = str(uuid.uuid4())
    job_manager.create(job_id)
    
    background_tasks.add_task(_generate_voiceover_task, job_id, script, language)
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        message="Voiceover generation started"
    )


def _generate_voiceover_task(job_id: str, script: str, language: str):
    """Background task to generate voiceover."""
    try:
        job_manager.update(job_id, status="processing", progress=50, message="Generating voiceover...")
        
        generator = AudioGenerator()
        output_path = settings.output_dir / f"{job_id}_voiceover.mp3"
        
        result = generator.generate_voiceover(script, output_path, language)
        
        if result:
            job_manager.complete(job_id, f"/api/v1/download/{job_id}_voiceover.mp3", "Voiceover generated successfully")
        else:
            raise Exception("Failed to generate voiceover")
        
    except Exception as e:
        job_manager.fail(job_id, str(e))
