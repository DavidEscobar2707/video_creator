"""
Step 2: Create Influencer Video using Character References
Uses the 3 character photos to generate video with Veo3
"""
import os
import time
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def check_character_references():
    """Check if all 3 character reference images exist"""
    print("=" * 70)
    print("📋 CHECKING CHARACTER REFERENCES")
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
            print(f"❌ {name}: NOT FOUND - {path}")
            all_found = False
    
    if not all_found:
        print("\n❌ Missing character references!")
        print("   Run: python create_character.py")
        return None
    
    print("\n✅ All character references found!")
    return files


def generate_video_with_veo3(
    character_refs,
    prompt,
    product_description,
    output_file="output/influencer_video.mp4"
):
    """
    Generate video using Veo3 with character references
    
    Args:
        character_refs: Dict with paths to character images
        prompt: Video generation prompt
        product_description: Description of product to show
        output_file: Path to save video
        
    Returns:
        Path to generated video or None
    """
    print("\n" + "=" * 70)
    print("🎬 GENERATING VIDEO WITH VEO3")
    print("=" * 70)
    
    try:
        client = genai.Client(api_key=API_KEY)
        
        # Load face reference as main image
        face_path = character_refs["Face"]
        with open(face_path, "rb") as f:
            face_bytes = f.read()
        
        print(f"\n📸 Using face reference: {face_path}")
        print(f"📝 Prompt: {prompt}")
        print(f"📱 Product: {product_description}")
        
        # Full prompt combining character and product
        full_prompt = f"""
        {prompt}
        
        The person is showing: {product_description}
        
        Professional quality, cinematic lighting, smooth movement.
        Vertical format for social media, 4K quality.
        """
        
        print("\n📤 Sending request to Veo3...")
        
        # Generate video
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=full_prompt,
            image=types.Image(
                image_bytes=face_bytes,
                mime_type="image/jpeg"
            ),
            config=types.GenerateVideosConfig(
                aspect_ratio="9:16",
                duration_seconds=8,
            ),
        )
        
        print("⏳ Waiting for generation (30-90 seconds)...")
        
        # Polling
        max_wait = 120
        elapsed = 0
        
        while not operation.done and elapsed < max_wait:
            time.sleep(5)
            elapsed += 5
            print(f"   ... {elapsed}s")
            operation = client.operations.get(operation)
        
        if not operation.done:
            print("⚠️  Timeout: Generation taking longer than expected")
            return None
        
        print("\n✅ Generation completed!")
        
        # Download video
        for video in operation.response.generated_videos:
            video_uri = video.video.uri
            print(f"⬇️  Downloading video...")
            
            headers = {'x-goog-api-key': API_KEY}
            response = requests.get(video_uri, headers=headers)
            
            if response.status_code == 200:
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


def generate_voiceover(script, output_file="temp/voiceover.mp3", language="en"):
    """Generate voiceover audio"""
    print("\n" + "=" * 70)
    print("🎤 GENERATING VOICEOVER")
    print("=" * 70)
    
    print(f"\n📝 Script: {script[:100]}...")
    
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        tts = gTTS(text=script, lang=language, slow=False)
        tts.save(output_file)
        
        size = os.path.getsize(output_file)
        print(f"✅ Audio saved: {output_file} ({size:,} bytes)")
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_influencer_video():
    """Main function to create complete influencer video"""
    print("\n" + "=" * 70)
    print(" " * 15 + "AI INFLUENCER VIDEO GENERATOR")
    print("=" * 70)
    
    # Step 1: Check character references
    character_refs = check_character_references()
    if not character_refs:
        return None
    
    # Configuration
    PROMPT = """
    A hyper-realistic close-up portrait of a professional female influencer in her late 20s, Caucasian, with a warm and confident expression. She has sleek dark blonde hair pulled back with loose strands framing her face, and piercing hazel eyes looking directly at the camera. 

SKIN & TEXTURE details: 
Visible skin pores, natural imperfections, slight peach fuzz, ultra-detailed skin texture, no plastic smoothing, moist lips, hyper-detailed iris.

LIGHTING & ATMOSPHERE: 
Cinematic lighting with "gobo" shadow patterns (striped shadows from window blinds) cast across her face, golden hour glow, soft natural fill light. 

OUTFIT: 
She is wearing a high-quality white knitted sweater, minimalist gold necklace. 

PHOTOGRAPHY SPECS: 
Shot on Sony A7R IV, 85mm portrait lens, f/1.8 aperture for shallow depth of field (creamy bokeh background), 8k resolution, raw style, sharp focus on eyes, professional color grading, high-end editorial photography.

She is holding a smartphone and showing it to the camera with a warm, engaging smile.
        The phone screen displays the TinyHeroes.ai app interface:
        - Colorful gradient background (blue to teal)
        - Large text: "Turn Your Child Into a Magical Character"
        - Subtitle about transforming photos with AI magic
        - Images of children dressed as superheroes and princesses
        - Blue "Create Magic Photos" button
        - "View Examples" button
        - 5-star rating with "Loved by 10,000+ families"
        
        Natural hand gestures showing the phone screen clearly to viewer.
        Professional lighting with soft shadows.
        Modern casual style - white sweater.
        Confident, friendly, and engaging demeanor.
        Smooth, natural movement.
        Cinematic quality, 4K.

    """
    
    PRODUCT_DESC = """
    Satirical social media app powered by generative AI.
    Interface: Slick, neon-cyberpunk aesthetic with a "Reality Filter" slider (0% to 100% Fake).
    Key Features: 
    - "Instant Travel": Generates selfies in Paris/Bali/Mars without leaving your couch.
    - "Glow Up Button": Instantly turns pajamas into haute couture.
    - "Foodie Mode": Turns your instant noodles into Michelin-star AI dishes.
    Vibe: Unapologetically artificial, glitch art elements, fun and ironic.
    """
    
    SCRIPT = """
    (Whispering to camera, confessional style)
    Guys, let's be honest... who actually wants to "be real" these days? Reality is boring.
    
    (Excited influencer voice, energy goes up)
    That's why I switched to BE FAKE!
    
    See that photo of me in the Maldives? (Laughs) I was literally in my pajamas eating cereal!
    BE FAKE uses AI to create the life you *should* have, not the one you actually have.
    
    Stop trying to find the perfect lighting. Just hit the button and... BAM! 
    You're a millionaire, you're tanned, and your cat is now a tiger.
    
    Download BE FAKE. Because honesty is overrated. Link in bio... (winks) if it's even real.
    """
    
    print("\n📋 Configuration:")
    print(f"   Prompt: {PROMPT[:60]}...")
    print(f"   Product: {PRODUCT_DESC[:60]}...")
    print(f"   Script: {SCRIPT[:60]}...")
    
    # Step 2: Generate video
    video = generate_video_with_veo3(
        character_refs=character_refs,
        prompt=PROMPT,
        product_description=PRODUCT_DESC,
        output_file="output/influencer_video.mp4"
    )
    
    if not video:
        print("\n❌ Video generation failed")
        return None
    
    # Step 3: Generate voiceover
    audio = generate_voiceover(
        script=SCRIPT,
        language="en"
    )
    
    # Step 4: Show results
    print("\n" + "=" * 70)
    print("🎉 VIDEO GENERATION COMPLETE!")
    print("=" * 70)
    
    print(f"\n📹 Video: {video}")
    if audio:
        print(f"🎤 Audio: {audio}")
    
    print("\n✅ Next steps:")
    print("   1. Review the generated video")
    print("   2. If you want to add voiceover, use video editing software")
    print("   3. Adjust prompt/script and regenerate if needed")
    
    return video


if __name__ == "__main__":
    # Allow customization via command line or edit here
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("\nUsage: python create_video.py")
        print("\nMake sure you have created character references first:")
        print("  python create_character.py")
        print("\nThe script will use references from:")
        print("  - references/character_face.jpg")
        print("  - references/character_body.jpg")
        print("  - references/character_side.jpg")
        sys.exit(0)
    
    create_influencer_video()
