"""Pydantic schemas for API request/response models."""
from typing import Optional
from pydantic import BaseModel, Field


class CharacterRequest(BaseModel):
    """Request to generate character reference images."""
    description: str = Field(
        ...,
        description="Detailed description of the character",
        example="Professional female influencer in her late 20s, warm smile, white sweater"
    )


class VideoRequest(BaseModel):
    """Request to generate influencer video."""
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
    aspect_ratio: str = Field(
        default="9:16",
        description="Video aspect ratio"
    )
    duration_seconds: int = Field(
        default=8,
        ge=1,
        le=8,
        description="Video duration in seconds (max 8)"
    )


class VoiceoverRequest(BaseModel):
    """Request to generate voiceover."""
    script: str = Field(
        ...,
        description="Voiceover script text",
        example="Hey everyone! Check out this amazing app..."
    )
    language: str = Field(
        default="en",
        description="Language code (en, es, fr, etc.)"
    )


class JobStatus(BaseModel):
    """Job status response."""
    job_id: str
    status: str  # pending, processing, completed, failed
    progress: int = Field(ge=0, le=100)
    message: str
    result_url: Optional[str] = None
    result_urls: Optional[dict[str, str]] = None  # For multiple results (e.g., character images)
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    api_key_configured: bool
    airtable_enabled: bool
    timestamp: float
