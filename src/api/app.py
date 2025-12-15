"""FastAPI application setup."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api.routes import health_router, character_router, video_router, voiceover_router


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="AI Influencer Video Generator API",
        description="Generate professional influencer videos using Veo3 and Imagen 4.0",
        version="2.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_router)
    app.include_router(character_router)
    app.include_router(video_router)
    app.include_router(voiceover_router)
    
    return app


app = create_app()
