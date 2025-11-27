"""
Regenerate only the body reference image
"""
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def regenerate_body_reference():
    """Regenerate body reference with simpler prompt"""
    print("=" * 70)
    print("🔄 REGENERATING BODY REFERENCE")
    print("=" * 70)
    
    # Simpler, safer prompt
    prompt = """
    Professional full body portrait photograph of a female influencer.
    Standing confidently, looking at camera with warm smile.
    White sweater and casual jeans, modern style.
    Studio lighting, clean neutral background.
    Full body visible from head to feet.
    Professional photography, high quality, vertical format.
    """
    
    try:
        client = genai.Client(api_key=API_KEY)
        
        print(f"\n📝 Prompt: {prompt[:80]}...")
        print("📤 Sending request to Imagen 4.0 Fast...")
        
        response = client.models.generate_images(
            model="imagen-4.0-fast-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="9:16",
                person_generation="allow_adult"
            )
        )
        
        print("⏳ Generating...")
        
        if response.generated_images and len(response.generated_images) > 0:
            image = response.generated_images[0]
            image_bytes = image.image.image_bytes
            
            output_file = "references/character_body.jpg"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, "wb") as f:
                f.write(image_bytes)
            
            size = os.path.getsize(output_file)
            print(f"✅ Saved: {output_file} ({size:,} bytes)")
            
            # Check all 3 references
            print("\n" + "=" * 70)
            print("📁 CHECKING ALL REFERENCES")
            print("=" * 70)
            
            files = {
                "Face": "references/character_face.jpg",
                "Body": "references/character_body.jpg",
                "Side": "references/character_side.jpg"
            }
            
            all_found = True
            for name, path in files.items():
                if os.path.exists(path):
                    size = os.path.getsize(path)
                    print(f"✅ {name}: {path} ({size:,} bytes)")
                else:
                    print(f"❌ {name}: NOT FOUND")
                    all_found = False
            
            if all_found:
                print("\n🎉 All 3 character references complete!")
                print("✅ Ready to create video! Run: python create_video.py")
            
            return output_file
        else:
            print("❌ No image generated")
            print("\n💡 Alternative: Use one of the existing images as body reference")
            print("   Or manually create/download a body shot image")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    regenerate_body_reference()
