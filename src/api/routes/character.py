"""Character generation routes."""
import uuid
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Form

from src.core import CharacterGenerator, settings
from src.api.schemas import JobStatus
from src.api.jobs import job_manager
from src.integrations.airtable import get_airtable_manager

router = APIRouter(prefix="/api/v1/character", tags=["Character"])


@router.post("/generate", response_model=JobStatus)
async def generate_character(
    background_tasks: BackgroundTasks,
    description: str = Form(...),
):
    """
    Generate character reference images.
    
    - **description**: Detailed character description
    
    Returns job_id to track progress.
    """
    job_id = str(uuid.uuid4())
    job_manager.create(job_id)
    
    background_tasks.add_task(_generate_character_task, job_id, description)
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        message="Character generation started"
    )


def _generate_character_task(job_id: str, description: str):
    """Background task to generate character images."""
    airtable = get_airtable_manager()
    airtable_record_id = None
    
    try:
        job_manager.update(job_id, status="processing", progress=30, message="Generating character face image...")
        
        generator = CharacterGenerator()
        
        # Generate only face image (most important for video generation)
        face_path = settings.output_dir / f"{job_id}_face.jpg"
        face_result = generator.generate_face(description, face_path)
        
        if not face_result:
            raise Exception("Failed to generate face reference image")
        
        # Complete with face URL
        job_manager.complete(
            job_id, 
            f"/api/v1/download/{job_id}_face.jpg",
            "Character face generated successfully"
        )
        
        if airtable:
            try:
                airtable_record_id = airtable.create_character_record(
                    job_id=job_id,
                    description=description,
                    face_image_path=str(face_result),
                    metadata={"generator": "Imagen 4.0 Fast"}
                )
            except Exception as e:
                print(f"Airtable save failed: {e}")
            
    except Exception as e:
        job_manager.fail(job_id, str(e))
        
        if airtable and airtable_record_id:
            try:
                airtable.update_record_status(airtable_record_id, "Failed", str(e))
            except:
                pass
