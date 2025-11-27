"""
FastAPI REST API for AI Influencer Video Generator
Allows frontend/Postman to generate videos with custom parameters
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import time
import uuid
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
from gtts import gTTS
from src.airtable_integration import AirtableManager

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Airtable (optional - will skip if not configured)
try:
    airtable = AirtableManager()
    AIRTABLE_ENABLED = True
    print("✅ Airtable integration enabled")
except Exception as e:
    airtable = None
    AIRTABLE_ENABLED = False
    print(f"⚠️  Airtable integration disabled: {e}")

# Initialize FastAPI
app = FastAPI(
    title="AI Influencer Video Generator API",
    description="Generate professional influencer videos using Veo3 and Imagen 4.0",
    version="1.0.0"
)

# CORS - Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
os.makedirs("output", exist_ok=True)
os.makedirs("temp", exist_ok=True)
os.makedirs("references", exist_ok=True)

# Store job status
jobs = {}


# ============================================================================
# MODELS (Request/Response schemas)
# ============================================================================

class CharacterDescription(BaseModel):
    """Character description for image generation"""
    description: str = Field(
        ...,
        description="Detailed description of the character",
        example="Professional female influencer in her late 20s, warm smile, white sweater"
    )


class VideoGenerationRequest(BaseModel):
    """Request to generate influencer video"""
    prompt: str = Field(
        ...,
        description="Video generation prompt",
        example="Professional influencer showing phone to camera with engaging smile"
    )
    product_description: str = Field(
        ...,
        description="Description of product/content to show",
        example="TinyHeroes.ai app - Transform photos with AI magic"
    )
    character_face_url: Optional[str] = Field(
        None,
        description="URL to character face reference image"
    )
    aspect_ratio: str = Field(
        "9:16",
        description="Video aspect ratio",
        example="9:16"
    )
    duration_seconds: int = Field(
        8,
        description="Video duration in seconds (max 8)",
        ge=1,
        le=8
    )


class VoiceoverRequest(BaseModel):
    """Request to generate voiceover"""
    script: str = Field(
        ...,
        description="Voiceover script text",
        example="Hey everyone! Check out this amazing app..."
    )
    language: str = Field(
        "en",
        description="Language code (en, es, fr, etc.)",
        example="en"
    )


class JobStatus(BaseModel):
    """Job status response"""
    job_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: int  # 0-100
    message: str
    result_url: Optional[str] = None
    error: Optional[str] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "AI Influencer Video Generator API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_character": "/api/v1/character/generate",
            "generate_video": "/api/v1/video/generate",
            "generate_voiceover": "/api/v1/voiceover/generate",
            "job_status": "/api/v1/job/{job_id}",
            "download": "/api/v1/download/{filename}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api_key_configured": bool(API_KEY),
        "timestamp": time.time()
    }


@app.post("/api/v1/character/generate", response_model=JobStatus)
async def generate_character(
    background_tasks: BackgroundTasks,
    description: str = Form(...),
):
    """
    Generate character reference images
    
    - **description**: Detailed character description
    
    Returns job_id to track progress
    """
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Job queued",
        "result_url": None,
        "error": None
    }
    
    # Run in background
    background_tasks.add_task(
        _generate_character_task,
        job_id,
        description
    )
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        message="Character generation started"
    )


@app.post("/api/v1/video/generate", response_model=JobStatus)
async def generate_video(
    background_tasks: BackgroundTasks,
    prompt: str = Form(...),
    product_description: str = Form(...),
    character_face: UploadFile = File(...),
    aspect_ratio: str = Form("9:16"),
    duration_seconds: int = Form(8)
):
    """
    Generate influencer video
    
    - **prompt**: Video generation prompt
    - **product_description**: Product/content description
    - **character_face**: Character face reference image (upload)
    - **aspect_ratio**: Video aspect ratio (default: 9:16)
    - **duration_seconds**: Video duration (default: 8, max: 8)
    
    Returns job_id to track progress
    """
    job_id = str(uuid.uuid4())
    
    # Save uploaded image
    face_path = f"temp/{job_id}_face.jpg"
    with open(face_path, "wb") as f:
        f.write(await character_face.read())
    
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Job queued",
        "result_url": None,
        "error": None
    }
    
    # Run in background
    background_tasks.add_task(
        _generate_video_task,
        job_id,
        prompt,
        product_description,
        face_path,
        aspect_ratio,
        duration_seconds
    )
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        message="Video generation started"
    )


@app.post("/api/v1/voiceover/generate", response_model=JobStatus)
async def generate_voiceover(
    background_tasks: BackgroundTasks,
    script: str = Form(...),
    language: str = Form("en")
):
    """
    Generate voiceover audio
    
    - **script**: Voiceover script text
    - **language**: Language code (en, es, fr, etc.)
    
    Returns job_id to track progress
    """
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Job queued",
        "result_url": None,
        "error": None
    }
    
    # Run in background
    background_tasks.add_task(
        _generate_voiceover_task,
        job_id,
        script,
        language
    )
    
    return JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        message="Voiceover generation started"
    )


@app.get("/api/v1/job/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """
    Get job status
    
    - **job_id**: Job ID returned from generation endpoint
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return JobStatus(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        result_url=job.get("result_url"),
        error=job.get("error")
    )


@app.get("/api/v1/download/{filename}")
async def download_file(filename: str):
    """
    Download generated file
    
    - **filename**: Filename to download
    """
    file_path = f"output/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=filename
    )


# ============================================================================
# BACKGROUND TASKS
# ============================================================================

def _generate_character_task(job_id: str, description: str):
    """Background task to generate character images"""
    airtable_record_id = None
    
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 10
        jobs[job_id]["message"] = "Generating character images..."
        
        client = genai.Client(api_key=API_KEY)
        
        # Generate face
        jobs[job_id]["progress"] = 30
        face_prompt = f"Professional headshot portrait. {description}. Studio lighting, 4K, photorealistic."
        
        response = client.models.generate_images(
            model="imagen-4.0-fast-generate-001",
            prompt=face_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="9:16",
                person_generation="allow_adult"
            )
        )
        
        if response.generated_images:
            face_path = f"output/{job_id}_face.jpg"
            with open(face_path, "wb") as f:
                f.write(response.generated_images[0].image.image_bytes)
            
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["progress"] = 100
            jobs[job_id]["message"] = "Character generated successfully"
            jobs[job_id]["result_url"] = f"/api/v1/download/{job_id}_face.jpg"
            
            # Save to Airtable
            if AIRTABLE_ENABLED:
                try:
                    airtable_record_id = airtable.create_character_record(
                        job_id=job_id,
                        description=description,
                        face_image_path=face_path,
                        metadata={"prompt": face_prompt}
                    )
                    jobs[job_id]["airtable_record_id"] = airtable_record_id
                    print(f"✅ Saved to Airtable: {airtable_record_id}")
                except Exception as e:
                    print(f"⚠️  Airtable save failed: {e}")
        else:
            raise Exception("No images generated")
            
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Failed: {str(e)}"
        
        # Update Airtable if record was created
        if AIRTABLE_ENABLED and airtable_record_id:
            try:
                airtable.update_record_status(airtable_record_id, "Failed", str(e))
            except:
                pass


def _generate_video_task(
    job_id: str,
    prompt: str,
    product_description: str,
    face_path: str,
    aspect_ratio: str,
    duration_seconds: int
):
    """Background task to generate video"""
    airtable_record_id = None
    
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 10
        jobs[job_id]["message"] = "Preparing video generation..."
        
        client = genai.Client(api_key=API_KEY)
        
        # Load image
        with open(face_path, "rb") as f:
            image_bytes = f.read()
        
        image = types.Image(
            image_bytes=image_bytes,
            mime_type="image/jpeg"
        )
        
        # Full prompt
        full_prompt = f"{prompt}\n\nShowing: {product_description}"
        
        jobs[job_id]["progress"] = 20
        jobs[job_id]["message"] = "Sending request to Veo3..."
        
        # Generate video
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=full_prompt,
            image=image,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                duration_seconds=duration_seconds
            )
        )
        
        # Polling
        jobs[job_id]["progress"] = 30
        jobs[job_id]["message"] = "Generating video (30-90 seconds)..."
        
        max_wait = 120
        elapsed = 0
        
        while not operation.done and elapsed < max_wait:
            time.sleep(5)
            elapsed += 5
            operation = client.operations.get(operation)
            
            # Update progress
            progress = 30 + int((elapsed / max_wait) * 60)
            jobs[job_id]["progress"] = min(progress, 90)
        
        if not operation.done:
            raise Exception("Video generation timeout")
        
        jobs[job_id]["progress"] = 90
        jobs[job_id]["message"] = "Downloading video..."
        
        # Download
        for video in operation.response.generated_videos:
            video_uri = video.video.uri
            
            headers = {'x-goog-api-key': API_KEY}
            response = requests.get(video_uri, headers=headers)
            
            if response.status_code == 200:
                output_path = f"output/{job_id}_video.mp4"
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                jobs[job_id]["status"] = "completed"
                jobs[job_id]["progress"] = 100
                jobs[job_id]["message"] = "Video generated successfully"
                jobs[job_id]["result_url"] = f"/api/v1/download/{job_id}_video.mp4"
                
                # Save to Airtable
                if AIRTABLE_ENABLED:
                    try:
                        airtable_record_id = airtable.create_video_record(
                            job_id=job_id,
                            prompt=prompt,
                            product_description=product_description,
                            video_path=output_path,
                            character_face_path=face_path,
                            aspect_ratio=aspect_ratio,
                            duration_seconds=duration_seconds,
                            metadata={"full_prompt": full_prompt}
                        )
                        jobs[job_id]["airtable_record_id"] = airtable_record_id
                        print(f"✅ Saved to Airtable: {airtable_record_id}")
                    except Exception as e:
                        print(f"⚠️  Airtable save failed: {e}")
            else:
                raise Exception(f"Download failed: HTTP {response.status_code}")
                
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Failed: {str(e)}"
        
        # Update Airtable if record was created
        if AIRTABLE_ENABLED and airtable_record_id:
            try:
                airtable.update_record_status(airtable_record_id, "Failed", str(e))
            except:
                pass


def _generate_voiceover_task(job_id: str, script: str, language: str):
    """Background task to generate voiceover"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 50
        jobs[job_id]["message"] = "Generating voiceover..."
        
        output_path = f"output/{job_id}_voiceover.mp3"
        
        tts = gTTS(text=script, lang=language, slow=False)
        tts.save(output_path)
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Voiceover generated successfully"
        jobs[job_id]["result_url"] = f"/api/v1/download/{job_id}_voiceover.mp3"
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Failed: {str(e)}"


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print(" " * 15 + "AI INFLUENCER VIDEO GENERATOR API")
    print("=" * 70)
    print("\n🚀 Starting server...")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🔧 Alternative docs: http://localhost:8000/redoc")
    print("\n" + "=" * 70)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
