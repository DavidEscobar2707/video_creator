"""
Character Reference Image Generator
Creates professional reference images for Veo3 character consistency
"""
import os
import subprocess
from PIL import Image
from .config import Config


class CharacterReferenceGenerator:
    """Generates character reference images by extracting frames from video"""
    
    def __init__(self, api_key=None):
        """
        Initialize the character reference generator
        
        Args:
            api_key: Gemini API key (optional, not used for frame extraction)
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
    
    def generate_face_reference(
        self,
        character_description="Professional female influencer, warm smile, looking at camera",
        output_file="references/character_face.jpg"
    ):
        """
        Generate face/headshot reference image
        
        Args:
            character_description: Description of the character
            output_file: Path to save the image
            
        Returns:
            Path to saved image or None if failed
        """
        print("=" * 60)
        print("👤 GENERATING FACE REFERENCE")
        print("=" * 60)
        
        prompt = f"""
        Professional headshot portrait photograph.
        {character_description}
        Close-up of face, direct eye contact with camera.
        Studio lighting, soft shadows, professional photography.
        Clean background, sharp focus on face.
        High quality, 4K, photorealistic.
        """
        
        return self._generate_image(prompt, output_file, "Face Reference")
    
    def generate_body_reference(
        self,
        character_description="Professional female influencer in casual business attire",
        output_file="references/character_body.jpg"
    ):
        """
        Generate full body reference image
        
        Args:
            character_description: Description of the character
            output_file: Path to save the image
            
        Returns:
            Path to saved image or None if failed
        """
        print("\n" + "=" * 60)
        print("🧍 GENERATING FULL BODY REFERENCE")
        print("=" * 60)
        
        prompt = f"""
        Professional full body portrait photograph.
        {character_description}
        Standing pose, confident posture, looking at camera.
        Full body visible from head to toe.
        Studio lighting, clean background.
        High quality, 4K, photorealistic.
        """
        
        return self._generate_image(prompt, output_file, "Body Reference")
    
    def generate_side_reference(
        self,
        character_description="Professional female influencer",
        output_file="references/character_side.jpg"
    ):
        """
        Generate side profile reference image
        
        Args:
            character_description: Description of the character
            output_file: Path to save the image
            
        Returns:
            Path to saved image or None if failed
        """
        print("\n" + "=" * 60)
        print("📐 GENERATING SIDE PROFILE REFERENCE")
        print("=" * 60)
        
        prompt = f"""
        Professional side profile portrait photograph.
        {character_description}
        90 degree side view, profile shot.
        Studio lighting, clean background.
        High quality, 4K, photorealistic.
        """
        
        return self._generate_image(prompt, output_file, "Side Reference")
    
    def generate_all_references(
        self,
        character_description="Professional female influencer, warm personality, approachable",
        output_prefix="references/character"
    ):
        """
        Generate all three reference images
        
        Args:
            character_description: Base description of the character
            output_prefix: Prefix for output files
            
        Returns:
            Dictionary with paths to all generated images
        """
        print("\n" + "=" * 60)
        print("🎬 GENERATING COMPLETE CHARACTER REFERENCE SET")
        print("=" * 60)
        print(f"\n📝 Character: {character_description}\n")
        
        results = {
            "face": None,
            "body": None,
            "side": None
        }
        
        # Generate face reference
        results["face"] = self.generate_face_reference(
            character_description=character_description,
            output_file=f"{output_prefix}_face.jpg"
        )
        
        # Generate body reference
        results["body"] = self.generate_body_reference(
            character_description=character_description,
            output_file=f"{output_prefix}_body.jpg"
        )
        
        # Generate side reference
        results["side"] = self.generate_side_reference(
            character_description=character_description,
            output_file=f"{output_prefix}_side.jpg"
        )
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 GENERATION SUMMARY")
        print("=" * 60)
        
        success_count = sum(1 for v in results.values() if v is not None)
        
        for ref_type, path in results.items():
            status = "✅" if path else "❌"
            print(f"{status} {ref_type.capitalize()}: {path or 'Failed'}")
        
        print(f"\n✅ Successfully generated {success_count}/3 references")
        
        return results
    
    def _generate_image(self, prompt, output_file, image_type):
        """
        Internal method to generate image using Imagen 3
        
        Args:
            prompt: Image generation prompt
            output_file: Path to save the image
            image_type: Type of image for logging
            
        Returns:
            Path to saved image or None if failed
        """
        try:
            print(f"\n📝 Prompt: {prompt[:100]}...")
            print("📤 Sending request to Imagen 3...")
            
            # Generate image using Imagen 3
            response = self.client.models.generate_images(
                model="imagen-3.0-generate-001",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="9:16",  # Vertical format
                    safety_filter_level="block_some",
                    person_generation="allow_adult"
                )
            )
            
            print("⏳ Waiting for generation...")
            
            # Get the generated image
            if response.generated_images and len(response.generated_images) > 0:
                image = response.generated_images[0]
                
                # Download image
                print(f"⬇️  Downloading {image_type}...")
                
                # Imagen returns image data directly
                image_data = image.image.image_bytes
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                # Save image
                with open(output_file, "wb") as f:
                    f.write(image_data)
                
                size = os.path.getsize(output_file)
                print(f"✅ {image_type} saved: {output_file} ({size:,} bytes)")
                
                return output_file
            else:
                print(f"❌ No image generated for {image_type}")
                return None
                
        except Exception as e:
            print(f"❌ Error generating {image_type}: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Example character description
    CHARACTER_DESC = """
    Professional female influencer in her late 20s.
    Warm, friendly smile and approachable demeanor.
    Modern casual business style - white sweater, minimal jewelry.
    Natural makeup, professional appearance.
    Confident and engaging personality.
    """
    
    generator = CharacterReferenceGenerator()
    
    results = generator.generate_all_references(
        character_description=CHARACTER_DESC,
        output_prefix="references/my_character"
    )
    
    print("\n🎉 Character reference generation complete!")
    print("\n📁 Use these images as reference_images in Veo3 for consistent character")
