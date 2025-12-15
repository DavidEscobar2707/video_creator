"""API routes."""
from .health import router as health_router
from .character import router as character_router
from .video import router as video_router
from .voiceover import router as voiceover_router

__all__ = [
    "health_router",
    "character_router",
    "video_router",
    "voiceover_router",
]
