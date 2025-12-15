#!/usr/bin/env python
"""Main entry point for AI Influencer Video Generator API."""
import uvicorn

from src.core.config import settings


if __name__ == "__main__":
    print("=" * 70)
    print(" " * 15 + "AI INFLUENCER VIDEO GENERATOR API")
    print("=" * 70)
    print("\n🚀 Starting server...")
    print(f"📝 API Documentation: http://localhost:{settings.api_port}/docs")
    print(f"🔧 Alternative docs: http://localhost:{settings.api_port}/redoc")
    print("\n" + "=" * 70)
    
    uvicorn.run(
        "src.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
