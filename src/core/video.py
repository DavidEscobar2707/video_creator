"""Video generation using Veo3 API."""
import time
from pathlib import Path
from typing import Optional
import requests
from google import genai
from google.genai import types

from .config import settings


class VideoGenerator:
    """Generates videos using Veo3 API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = settings.veo_model
    
    def generate(
        self,
        prompt: str,
        image_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        aspect_ratio: str = None,
        duration_seconds: int = None,
        timeout: int = 120
    ) -> Optional[Path]:
        """
        Generate video using Veo3.
        
        Args:
            prompt: Video generation prompt
            image_path: Reference image path
            output_path: Output video path
            aspect_ratio: Video aspect ratio
            duration_seconds: Video duration
            timeout: Max wait time in seconds
            
        Returns:
            Path to generated video or None
        """
        output_path = output_path or settings.output_dir / "generated_video.mp4"
        aspect_ratio = aspect_ratio or settings.default_aspect_ratio
        duration_seconds = duration_seconds or settings.default_duration
        
        try:
            # Prepare image input
            image_input = None
            if image_path and image_path.exists():
                image_input = types.Image(
                    image_bytes=image_path.read_bytes(),
                    mime_type="image/jpeg"
                )
            
            # Generate video
            operation = self.client.models.generate_videos(
                model=self.model,
                prompt=prompt,
                image=image_input,
                config=types.GenerateVideosConfig(
                    aspect_ratio=aspect_ratio,
                    duration_seconds=duration_seconds,
                ),
            )
            
            # Poll for completion
            elapsed = 0
            while not operation.done and elapsed < timeout:
                time.sleep(5)
                elapsed += 5
                operation = self.client.operations.get(operation)
            
            if not operation.done:
                return None
            
            # Download video
            for video in operation.response.generated_videos:
                return self._download_video(video.video.uri, output_path)
            
            return None
            
        except Exception as e:
            print(f"Error generating video: {e}")
            return None
    
    def generate_influencer_video(
        self,
        character_face_path: Path,
        product_description: str,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """Generate influencer video showing product."""
        prompt = f"""
        Professional influencer video, vertical format for social media.
        The person looks directly at camera with warm, engaging smile.
        Natural hand gestures showing phone screen to viewer.
        Phone displays: {product_description}
        Cinematic lighting, professional quality.
        Smooth, natural movement.
        Modern, clean aesthetic.
        4K quality, engaging and authentic.
        """
        
        return self.generate(
            prompt=prompt,
            image_path=character_face_path,
            output_path=output_path
        )
    
    def _download_video(self, uri: str, output_path: Path) -> Optional[Path]:
        """Download video from URI."""
        try:
            headers = {"x-goog-api-key": self.api_key}
            response = requests.get(uri, headers=headers)
            
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(response.content)
                return output_path
            
            return None
            
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
