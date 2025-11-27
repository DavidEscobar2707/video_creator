"""
Configuration module for AI Influencer Video Generator
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Veo3 Settings
    VEO_MODEL = "veo-3.1-fast-generate-preview"
    VEO_ASPECT_RATIO = "9:16"  # Vertical for social media
    VEO_DURATION = 8  # seconds
    
    # Paths
    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"
    REFERENCE_DIR = "references"
    
    # Video Settings
    VIDEO_WIDTH = 1080
    VIDEO_HEIGHT = 1920
    VIDEO_FPS = 30
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Create directories if they don't exist
        for directory in [cls.OUTPUT_DIR, cls.TEMP_DIR, cls.REFERENCE_DIR]:
            os.makedirs(directory, exist_ok=True)
        
        return True
