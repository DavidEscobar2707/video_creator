"""
Veo3 Video Generator
Handles video generation using Google Veo3 API
"""
import os
import time
import requests
from google import genai
from google.genai import types
from .config import Config


class Veo3Generator:
    """Generates videos using Veo3 API"""
    
    def __init__(self, api_key=None):
        """
        Initialize Veo3 generator
        
        Args:
            api_key: Gemini API key (optional, uses Config if not provided)
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.client = genai.Client(api_key=self.api_key)
    
    def generate_video(
        self,
        prompt,
        scene_image_path=None,
        reference_images=None,
        output_file="output/generated_video.mp4",
        aspect_ratio="9:16",
        duration_seconds=8
    ):
        """
        Generate video using Veo3
        
        Args:
            prompt: Text description of desired video
            scene_image_path: Path to scene/base image (optional)
            reference_images: List of paths to character reference images (optional)
            output_file: Path to save generated video
            aspect_ratio: Video aspect ratio (default: 9:16 for vertical)
            duration_seconds: Video duration in seconds (max 8)
            
        Returns:
            Path to generated video or None if failed
        """
        print("=" * 60)
        print("🎬 GENERATING VIDEO WITH VEO3")
        print("=" * 60)
        
        print(f"\n📝 Prompt: {prompt}")
        print(f"📐 Aspect Ratio: {aspect_ratio}")
        print(f"⏱️  Duration: {duration_seconds}s")
        
        try:
            # Prepare image inputs
            image_input = None
            if scene_image_path and os.path.exists(scene_image_path):
                with open(scene_image_path, "rb") as f:
                    image_bytes = f.read()
                
                image_input = types.Image(
                    image_bytes=image_bytes,
                    mime_type="image/jpeg"
                )
                print(f"📸 Scene image: {scene_image_path}")
            
            # Prepare reference images
            ref_images = []
            if reference_images:
                for ref_path in reference_images:
                    if os.path.exists(ref_path):
                        with open(ref_path, "rb") as f:
                            ref_bytes = f.read()
                        
                        ref_images.append(types.Image(
                            image_bytes=ref_bytes,
                            mime_type="image/jpeg"
                        ))
                        print(f"👤 Reference: {ref_path}")
            
            print("\n📤 Sending request to Veo3...")
            
            # Generate video
            operation = self.client.models.generate_videos(
                model=Config.VEO_MODEL,
                prompt=prompt,
                image=image_input,
                config=types.GenerateVideosConfig(
                    aspect_ratio=aspect_ratio,
                    duration_seconds=duration_seconds,
                ),
                # Note: reference_images support may vary by API version
                # reference_images=ref_images if ref_images else None
            )
            
            print("⏳ Waiting for generation (30-60 seconds)...")
            
            # Polling
            max_wait = 120
            elapsed = 0
            
            while not operation.done and elapsed < max_wait:
                time.sleep(5)
                elapsed += 5
                print(f"   ... {elapsed}s")
                operation = self.client.operations.get(operation)
            
            if not operation.done:
                print("⚠️  Timeout: Generation taking longer than expected")
                return None
            
            print("\n✅ Generation completed!")
            
            # Download video
            for video in operation.response.generated_videos:
                video_uri = video.video.uri
                print(f"⬇️  Downloading from: {video_uri}")
                
                # Download with authentication
                headers = {'x-goog-api-key': self.api_key}
                response = requests.get(video_uri, headers=headers)
                
                if response.status_code == 200:
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    
                    with open(output_file, "wb") as f:
                        f.write(response.content)
                    
                    size = os.path.getsize(output_file)
                    print(f"✅ Video saved: {output_file} ({size:,} bytes)")
                    return output_file
                else:
                    print(f"❌ Download failed: HTTP {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def generate_influencer_video(
        self,
        character_references,
        product_description,
        output_file="output/influencer_video.mp4"
    ):
        """
        Generate influencer video showing product
        
        Args:
            character_references: Dict with paths to character reference images
            product_description: Description of the product to show
            output_file: Path to save video
            
        Returns:
            Path to generated video or None if failed
        """
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
        
        # Use face reference as main image
        scene_image = character_references.get("face")
        
        # Use all references for consistency
        ref_images = [
            character_references.get("face"),
            character_references.get("body"),
            character_references.get("side")
        ]
        ref_images = [img for img in ref_images if img and os.path.exists(img)]
        
        return self.generate_video(
            prompt=prompt,
            scene_image_path=scene_image,
            reference_images=ref_images,
            output_file=output_file
        )
