"""
Step 1: Create Character Reference Images
Generates 3 professional photos using Gemini image generation
"""
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def generate_character_image(prompt, output_file):
    """
    Generate a single character reference image using Nano Banana Pro
    
    Args:
        prompt: Description of the image to generate
        output_file: Path to save the image
        
    Returns:
        Path to saved image or None if failed
    """
    try:
        client = genai.Client(api_key=API_KEY)
        
        print(f"\n📝 Generating: {os.path.basename(output_file)}")
        print(f"   Prompt: {prompt[:80]}...")
        print("   📤 Sending request to Nano Banana Pro...")
        
        # Generate image using Imagen 4.0 Fast (Nano Banana Pro)
        response = client.models.generate_images(
            model="imagen-4.0-fast-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="9:16",
                person_generation="allow_adult"
            )
        )
        
        print("   ⏳ Generating...")
        
        # Get generated image
        if response.generated_images and len(response.generated_images) > 0:
            image = response.generated_images[0]
            
            # Get image bytes
            image_bytes = image.image.image_bytes
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save image
            with open(output_file, "wb") as f:
                f.write(image_bytes)
            
            size = os.path.getsize(output_file)
            print(f"   ✅ Saved: {output_file} ({size:,} bytes)")
            return output_file
        else:
            print(f"   ❌ No image generated")
            return None
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


def create_character_references_with_ai(character_description):
    """
    Create all 3 character references using Nano Banana Pro
    
    Args:
        character_description: Base description of the character
        
    Returns:
        Dict with paths to generated images
    """
    print("=" * 70)
    print(" " * 15 + "CHARACTER REFERENCE GENERATOR")
    print(" " * 20 + "(Nano Banana Pro)")
    print("=" * 70)
    
    print(f"\n📝 Character: {character_description}\n")
    
    # Create references directory
    os.makedirs("references", exist_ok=True)
    
    results = {}
    
    # 1. Face Reference
    face_prompt = f"""
    Professional headshot portrait photograph.
    {character_description}
    Close-up of face, direct eye contact with camera.
    Studio lighting, soft shadows, professional photography.
    Clean background, sharp focus on face.
    High quality, 4K, photorealistic, vertical format.
    """
    
    results["face"] = generate_character_image(
        prompt=face_prompt,
        output_file="references/character_face.jpg"
    )
    
    # 2. Body Reference
    body_prompt = f"""
    Professional full body portrait photograph.
    {character_description}
    Standing pose, confident posture, looking at camera.
    Full body visible from head to toe.
    Studio lighting, clean background.
    High quality, 4K, photorealistic, vertical format.
    """
    
    results["body"] = generate_character_image(
        prompt=body_prompt,
        output_file="references/character_body.jpg"
    )
    
    # 3. Side Reference
    side_prompt = f"""
    Professional side profile portrait photograph.
    {character_description}
    90 degree side view, profile shot.
    Studio lighting, clean background.
    High quality, 4K, photorealistic, vertical format.
    """
    
    results["side"] = generate_character_image(
        prompt=side_prompt,
        output_file="references/character_side.jpg"
    )
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 GENERATION SUMMARY")
    print("=" * 70)
    
    success_count = sum(1 for v in results.values() if v is not None)
    
    for ref_type, path in results.items():
        if path:
            print(f"✅ {ref_type.capitalize()}: {path}")
        else:
            print(f"❌ {ref_type.capitalize()}: Failed")
    
    print(f"\n✅ Successfully generated {success_count}/3 references")
    
    if success_count == 3:
        print("\n🎉 All character references created!")
        print("✅ Ready to create video! Run: python create_video.py")
    elif success_count > 0:
        print(f"\n⚠️  Only {success_count}/3 images generated successfully")
        print("   You may need to regenerate the failed ones")
    else:
        print("\n❌ No images generated. Check your API key and permissions")
    
    return results


def create_character_references_manual():
    """
    Guide user to create character references manually
    """
    print("=" * 70)
    print(" " * 20 + "CHARACTER REFERENCE CREATOR")
    print("=" * 70)
    
    print("\n📸 You need to create 3 professional photos of your character:")
    print("\n1️⃣  FACE REFERENCE (Close-up)")
    print("   - Headshot, looking at camera")
    print("   - Clear view of facial features")
    print("   - Professional lighting")
    print("   - Save as: references/character_face.jpg")
    
    print("\n2️⃣  BODY REFERENCE (Full body)")
    print("   - Full body shot, head to toe")
    print("   - Standing pose, confident")
    print("   - Shows clothing style")
    print("   - Save as: references/character_body.jpg")
    
    print("\n3️⃣  SIDE REFERENCE (Profile)")
    print("   - 90-degree side view")
    print("   - Profile shot")
    print("   - Same lighting as other photos")
    print("   - Save as: references/character_side.jpg")
    
    print("\n" + "=" * 70)
    print("💡 OPTIONS TO CREATE THESE PHOTOS:")
    print("=" * 70)
    
    print("\n🎨 Option 1: AI Image Generation (Recommended)")
    print("   - Use Midjourney: https://midjourney.com")
    print("   - Use DALL-E: https://openai.com/dall-e")
    print("   - Use Leonardo.ai: https://leonardo.ai")
    
    print("\n📷 Option 2: Real Photos")
    print("   - Hire a photographer")
    print("   - Use stock photos (with license)")
    print("   - Take your own photos")
    
    print("\n🎬 Option 3: Extract from existing video")
    print("   - If you have a video, extract 3 frames")
    print("   - Use: python extract_frames.py <video_file>")
    
    print("\n" + "=" * 70)
    print("📋 EXAMPLE PROMPTS FOR AI GENERATION:")
    print("=" * 70)
    
    print("\n🎨 For Midjourney/DALL-E:")
    
    print("\n   Face Reference:")
    print("   'Professional headshot portrait of a female influencer in her late 20s,")
    print("   warm smile, looking at camera, studio lighting, white sweater,")
    print("   natural makeup, 4K, photorealistic --ar 9:16'")
    
    print("\n   Body Reference:")
    print("   'Full body portrait of a female influencer, standing confidently,")
    print("   white sweater and jeans, modern casual style, studio lighting,")
    print("   clean background, 4K, photorealistic --ar 9:16'")
    
    print("\n   Side Reference:")
    print("   'Side profile portrait of a female influencer, 90 degree angle,")
    print("   white sweater, professional lighting, clean background,")
    print("   4K, photorealistic --ar 9:16'")
    
    print("\n" + "=" * 70)
    print("✅ NEXT STEPS:")
    print("=" * 70)
    
    print("\n1. Create the 3 photos using one of the options above")
    print("2. Save them in the 'references/' folder with these names:")
    print("   - references/character_face.jpg")
    print("   - references/character_body.jpg")
    print("   - references/character_side.jpg")
    print("\n3. Run: python create_video.py")
    
    print("\n" + "=" * 70)
    
    # Create references directory
    os.makedirs("references", exist_ok=True)
    print("\n✅ Created 'references/' directory")
    
    # Check if files already exist
    print("\n📁 Checking for existing reference images...")
    
    files = {
        "Face": "references/character_face.jpg",
        "Body": "references/character_body.jpg",
        "Side": "references/character_side.jpg"
    }
    
    found = 0
    for name, path in files.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"   ✅ {name}: {path} ({size:,} bytes)")
            found += 1
        else:
            print(f"   ❌ {name}: Not found")
    
    if found == 3:
        print("\n🎉 All 3 reference images found!")
        print("✅ Ready to create video! Run: python create_video.py")
    elif found > 0:
        print(f"\n⚠️  Found {found}/3 images. Create the missing ones.")
    else:
        print("\n📝 No reference images found yet. Create them using the options above.")
    
    return found == 3


if __name__ == "__main__":
    import sys
    
    # Default character description
    DEFAULT_CHARACTER = """
    A hyper-realistic close-up portrait of a professional female influencer in her late 20s, Caucasian, with a warm and confident expression. She has sleek dark blonde hair pulled back with loose strands framing her face, and piercing hazel eyes looking directly at the camera. 

SKIN & TEXTURE details: 
Visible skin pores, natural imperfections, slight peach fuzz, ultra-detailed skin texture, no plastic smoothing, moist lips, hyper-detailed iris.

LIGHTING & ATMOSPHERE: 
Cinematic lighting with "gobo" shadow patterns (striped shadows from window blinds) cast across her face, golden hour glow, soft natural fill light. 

OUTFIT: 
She is wearing a high-quality white knitted sweater, minimalist gold necklace. 

PHOTOGRAPHY SPECS: 
Shot on Sony A7R IV, 85mm portrait lens, f/1.8 aperture for shallow depth of field (creamy bokeh background), 8k resolution, raw style, sharp focus on eyes, professional color grading, high-end editorial photography.

    """
    
    print("\n" + "=" * 70)
    print(" " * 20 + "AI CHARACTER CREATOR")
    print(" " * 18 + "Using Nano Banana Pro")
    print("=" * 70)
    
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("\nUsage: python create_character.py [--manual]")
        print("\nOptions:")
        print("  (no args)  - Generate images with AI (Nano Banana Pro)")
        print("  --manual   - Show manual creation guide")
        print("  --help     - Show this help message")
        sys.exit(0)
    
    # Check for manual flag
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        create_character_references_manual()
    else:
        # Use AI generation (default)
        print("\n🤖 Generating character references with AI...")
        print("   (Use --manual flag for manual creation guide)\n")
        
        results = create_character_references_with_ai(DEFAULT_CHARACTER)
        
        if sum(1 for v in results.values() if v) == 3:
            print("\n" + "=" * 70)
            print("🎉 SUCCESS! All character references created!")
            print("=" * 70)
            print("\n📁 Files created:")
            for ref_type, path in results.items():
                if path:
                    print(f"   - {path}")
            print("\n🎬 Next step: python create_video.py")
