"""Application configuration using Pydantic settings."""
import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    """Application configuration."""
    
    # API Keys
    gemini_api_key: str = ""
    airtable_api_key: str = ""
    airtable_base_id: str = ""
    airtable_table_name: str = "AI_Influencer_Videos"
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"
    output_dir: Path = data_dir / "output"
    temp_dir: Path = data_dir / "temp"
    references_dir: Path = data_dir / "references"
    
    # Video Settings
    veo_model: str = "veo-3.1-fast-generate-preview"
    imagen_model: str = "imagen-4.0-fast-generate-001"
    default_aspect_ratio: str = "9:16"
    default_duration: int = 8
    video_width: int = 1080
    video_height: int = 1920
    video_fps: int = 30
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    def __init__(self, **data):
        """Initialize configuration and setup directories."""
        super().__init__(**data)
        self.setup_directories()
    
    def setup_directories(self) -> None:
        """Create required directories."""
        for directory in [self.output_dir, self.temp_dir, self.references_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @property
    def airtable_enabled(self) -> bool:
        """Check if Airtable integration is configured."""
        return bool(self.airtable_api_key and self.airtable_base_id)


@lru_cache
def get_settings() -> Config:
    """Get cached settings instance."""
    config = Config()
    config.setup_directories()
    return config


settings = get_settings()
