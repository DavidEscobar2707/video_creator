"""Character reference image generation using Imagen 4.0."""
from pathlib import Path
from typing import Optional
import google.generativeai as genai
from google.generativeai import types

from .config import settings


class CharacterGenerator:
    """Generates character reference images using Imagen 4.0."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = settings.imagen_model
    
    def generate_face(
        self,
        description: str,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """Generate face/headshot reference image."""
        output_path = output_path or settings.references_dir / "character_face.jpg"
        
        prompt = f"""
        Professional headshot portrait photograph.
        {description}
        Close-up of face, direct eye contact with camera.
        Studio lighting, soft shadows, professional photography.
        Clean background, sharp focus on face.
        High quality, 4K, photorealistic.
        """
        
        return self._generate_image(prompt, output_path)
    
    def generate_body(
        self,
        description: str,
        reference_image_path: Optional[Path] = None,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """Generate full body reference image using face as reference."""
        output_path = output_path or settings.references_dir / "character_body.jpg"
        
        prompt = f"""
        Professional full body portrait photograph of the same person.
        {description}
        Standing pose, confident posture, looking at camera.
        Full body visible from head to toe.
        Studio lighting, clean background.
        High quality, 4K, photorealistic.
        Same person, same facial features, same appearance.
        """
        
        return self._generate_image_with_reference(prompt, reference_image_path, output_path)
    
    def generate_side(
        self,
        description: str,
        reference_image_path: Optional[Path] = None,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """Generate side profile reference image using face as reference."""
        output_path = output_path or settings.references_dir / "character_side.jpg"
        
        prompt = f"""
        Professional side profile portrait photograph of the same person.
        {description}
        90 degree side view, profile shot.
        Studio lighting, clean background.
        High quality, 4K, photorealistic.
        Same person, same facial features, same appearance.
        """
        
        return self._generate_image_with_reference(prompt, reference_image_path, output_path)
    
    def generate_all(self, description: str) -> dict[str, Optional[Path]]:
        """Generate all three reference images."""
        return {
            "face": self.generate_face(description),
            "body": self.generate_body(description),
            "side": self.generate_side(description),
        }
    
    def _generate_image(self, prompt: str, output_path: Path) -> Optional[Path]:
        """Generate image using Imagen 4.0 Fast."""
        try:
            response = self.client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio=settings.default_aspect_ratio,
                    person_generation="allow_adult"
                )
            )
            
            if response.generated_images:
                image_bytes = response.generated_images[0].image.image_bytes
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_bytes)
                return output_path
            
            return None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def _generate_image_with_reference(
        self, 
        prompt: str, 
        reference_image_path: Optional[Path],
        output_path: Path
    ) -> Optional[Path]:
        """Generate image using enhanced prompt for consistency."""
        # For now, Imagen 4.0 doesn't support reference images in the way we need
        # So we'll use the same generation method but with enhanced prompts
        # The prompts already include "same person" instructions
        return self._generate_image(prompt, output_path)
