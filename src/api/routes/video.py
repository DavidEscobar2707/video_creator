"""Video generation routes."""
import uuid
import time
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import requests
from google import genai
from google.genai import types

from src.core import settings
from src.api.schemas import JobStatus
from src.api.jobs import job_manager
from src.integrations.airtable import get_airtable_manager

router = APIRouter(prefix="/api/v1", tags=["Video"])


@router.post("/video/generate", response_model=JobStatus)
async def generate_video(
    background_tasks: BackgroundTasks,
    prompt: str = Form(...),
    product_description: str = Form(...),
    character_face: UploadFile = File(None),
    character_job_id: str = Form(None),
    character_image_type: str = Form("face"),
    aspect_ratio: str = Form("9:16"),
    duration_seconds: int = Form(8)
):
    """
    Generate influencer video.
    
    - **prompt**: Video generation prompt
    - **product_description**: Product/content description
    - **character_face**: Character face reference image (upload) - optional if character_job_id provided
    - **character_job_id**: Job ID from character generation - optional if character_face provided
    - **character_image_type**: Which image to use from character job (face, body, side) - default: face
    - **aspect_ratio**: Video aspect ratio (default: 9:16)
    - **duration_seconds**: Video duration (default: 8, max: 8)
    
    Returns job_id to track progress.
    """
    job_id = str(uuid.uuid4())
    
    # Determine which image to use
    if character_job_id:
        # Use image from previous character generation
        face_path = settings.output_dir / f"{character_job_id}_{character_image_type}.jpg"
        if not face_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"Character image not found for job {character_job_id}"
            )
    elif character_face:
        # Save uploaded image
        face_path = settings.temp_dir / f"{job_id}_face.jpg"
        face_path.parent.mkdir(parents=True, exist_ok=True)
        face_path.write_bytes(await character_face.read())
    else:
        raise HTTPException(
            status_code=400,
            detail="Either character_face or character_job_id must be provided"
        )
    
    job_manager.create(job_id)
    
    background_tasks.add_task(
        _generate_video_task,
        job_id, prompt, product_description, face_path, aspect_ratio, duration_seconds
    )
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        message="Video generation started"
    )


@router.get("/job/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get job status."""
    job = job_manager.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatus(
        job_id=job_id,
        status=job.status,
        progress=job.progress,
        message=job.message,
        result_url=job.result_url,
        result_urls=job.result_urls,
        error=job.error
    )


@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated file."""
    file_path = settings.output_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        str(file_path),
        media_type="application/octet-stream",
        filename=filename
    )


def _generate_video_task(
    job_id: str,
    prompt: str,
    product_description: str,
    face_path: Path,
    aspect_ratio: str,
    duration_seconds: int
):
    """Background task to generate video."""
    airtable = get_airtable_manager()
    airtable_record_id = None
    
    try:
        job_manager.update(job_id, status="processing", progress=10, message="Preparing video generation...")
        
        client = genai.Client(api_key=settings.gemini_api_key)
        
        image = types.Image(
            image_bytes=face_path.read_bytes(),
            mime_type="image/jpeg"
        )
        
        full_prompt = f"{prompt}\n\nShowing: {product_description}"
        
        job_manager.update(job_id, progress=20, message="Sending request to Veo3...")
        
        operation = client.models.generate_videos(
            model=settings.veo_model,
            prompt=full_prompt,
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                duration_seconds=duration_seconds
            )
        )
        
        job_manager.update(job_id, progress=30, message="Generating video (30-90 seconds)...")
        
        max_wait = 120
        elapsed = 0
        
        while not operation.done and elapsed < max_wait:
            time.sleep(5)
            elapsed += 5
            operation = client.operations.get(operation)
            progress = 30 + int((elapsed / max_wait) * 60)
            job_manager.update(job_id, progress=min(progress, 90))
        
        if not operation.done:
            raise Exception("Video generation timeout")
        
        job_manager.update(job_id, progress=90, message="Downloading video...")
        
        for video in operation.response.generated_videos:
            headers = {"x-goog-api-key": settings.gemini_api_key}
            response = requests.get(video.video.uri, headers=headers)
            
            if response.status_code == 200:
                output_path = settings.output_dir / f"{job_id}_video.mp4"
                output_path.write_bytes(response.content)
                
                job_manager.complete(job_id, f"/api/v1/download/{job_id}_video.mp4", "Video generated successfully")
                
                if airtable:
                    try:
                        airtable_record_id = airtable.create_video_record(
                            job_id=job_id,
                            prompt=prompt,
                            product_description=product_description,
                            video_path=str(output_path),
                            character_face_path=str(face_path),
                            aspect_ratio=aspect_ratio,
                            duration_seconds=duration_seconds,
                            metadata={"full_prompt": full_prompt}
                        )
                    except Exception as e:
                        print(f"Airtable save failed: {e}")
            else:
                raise Exception(f"Download failed: HTTP {response.status_code}")
                
    except Exception as e:
        job_manager.fail(job_id, str(e))
        
        if airtable and airtable_record_id:
            try:
                airtable.update_record_status(airtable_record_id, "Failed", str(e))
            except:
                pass
