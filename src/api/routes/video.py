"""Video generation routes."""
import uuid
import time
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import requests
import google.generativeai as genai
from google.generativeai import types

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


@router.post("/video/add-subtitles", response_model=JobStatus)
async def add_subtitles_to_video(
    background_tasks: BackgroundTasks,
    video_job_id: str = Form(...),
    subtitle_text: str = Form(...),
    subtitle_language: str = Form("en"),
    font_size: int = Form(24),
    font_color: str = Form("white")
):
    """
    Add subtitles to a generated video.
    
    - **video_job_id**: ID of the generated video
    - **subtitle_text**: Text for the subtitles
    - **subtitle_language**: Language code (en, es, fr, etc.)
    - **font_size**: Font size for subtitles (default: 24)
    - **font_color**: Font color (white, yellow, etc.)
    
    Returns job_id to track progress.
    """
    job_id = str(uuid.uuid4())
    job_manager.create(job_id)
    
    background_tasks.add_task(
        _add_subtitles_task,
        job_id, video_job_id, subtitle_text, subtitle_language, font_size, font_color
    )
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        message="Adding subtitles to video..."
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



def _add_subtitles_task(
    job_id: str,
    video_job_id: str,
    subtitle_text: str,
    subtitle_language: str,
    font_size: int,
    font_color: str
):
    """Background task to add subtitles to video."""
    import subprocess
    
    airtable = get_airtable_manager()
    airtable_record_id = None
    
    try:
        job_manager.update(job_id, status="processing", progress=10, message="Preparing subtitle addition...")
        
        # Paths
        video_path = settings.output_dir / f"{video_job_id}_video.mp4"
        subtitle_path = settings.temp_dir / f"{job_id}_subtitles.srt"
        output_path = settings.output_dir / f"{job_id}_video_with_subtitles.mp4"
        
        if not video_path.exists():
            raise Exception(f"Video not found: {video_job_id}")
        
        # Create SRT subtitle file
        job_manager.update(job_id, progress=20, message="Creating subtitle file...")
        _create_srt_file(subtitle_path, subtitle_text)
        
        # Add subtitles using FFmpeg
        job_manager.update(job_id, progress=50, message="Adding subtitles with FFmpeg...")
        _add_subtitles_with_ffmpeg(
            str(video_path), 
            str(subtitle_path), 
            str(output_path),
            font_size,
            font_color
        )
        
        job_manager.complete(
            job_id,
            f"/api/v1/download/{job_id}_video_with_subtitles.mp4",
            "Subtitles added successfully"
        )
        
        if airtable:
            try:
                airtable_record_id = airtable.create_video_record(
                    job_id=job_id,
                    prompt=f"Subtitled video from {video_job_id}",
                    product_description=subtitle_text,
                    video_path=str(output_path),
                    character_face_path="",
                    aspect_ratio="9:16",
                    duration_seconds=8,
                    metadata={
                        "original_video_job_id": video_job_id,
                        "subtitle_language": subtitle_language,
                        "subtitle_text": subtitle_text
                    }
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


def _create_srt_file(output_path: Path, subtitle_text: str):
    """Create SRT subtitle file."""
    # Simple SRT format: one subtitle for the entire video duration
    srt_content = f"""1
00:00:00,000 --> 00:00:08,000
{subtitle_text}
"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(srt_content, encoding='utf-8')


def _add_subtitles_with_ffmpeg(
    video_path: str, 
    subtitle_path: str, 
    output_path: str,
    font_size: int = 24,
    font_color: str = "white"
):
    """Add subtitles to video using FFmpeg."""
    import subprocess
    
    # Map color names to hex values for FFmpeg
    color_map = {
        "white": "&H00FFFFFF&",
        "yellow": "&H0000FFFF&",
        "red": "&H000000FF&",
        "green": "&H0000FF00&",
        "blue": "&H00FF0000&",
        "black": "&H00000000&"
    }
    
    color_hex = color_map.get(font_color.lower(), "&H00FFFFFF&")
    
    # Escape the subtitle path for Windows
    subtitle_path_escaped = subtitle_path.replace('\\', '\\\\').replace(':', '\\:')
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={subtitle_path_escaped}:force_style='FontSize={font_size},PrimaryColour={color_hex},Alignment=2'",
        '-c:a', 'copy',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-y',  # Overwrite output file if exists
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg error: {result.stderr}")
