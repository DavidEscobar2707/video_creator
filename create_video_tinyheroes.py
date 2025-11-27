"""
Generate influencer video showing TinyHeroes.ai on phone screen
"""
import os
import time
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def create_tinyheroes_video():
    """Create video with TinyHeroes.ai content on phone"""
    print("=" * 70)
    print("🎬 CREATING TINYHEROES.AI INFLUENCER VIDEO")
    print("=" * 70)
    
    # Check references
    face_path = "references/character_face.jpg"
    if not os.path.exists(face_path):
        print("❌ Character face reference not found")
        return None
    
    try:
        client = genai.Client(api_key=API_KEY)
        
        # Load face reference
        with open(face_path, "rb") as f:
            face_bytes = f.read()
        
        # Detailed prompt with TinyHeroes.ai content
        prompt = """
        Professional female influencer video, vertical format.
        
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
        
        print(f"\n📸 Using: {face_path}")
        print(f"📝 Prompt: TinyHeroes.ai app showcase")
        print("\n📤 Sending request to Veo3...")
        
        # Generate video
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=prompt,
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
            print("⚠️  Timeout")
            return None
        
        print("\n✅ Generation completed!")
        
        # Download
        for video in operation.response.generated_videos:
            video_uri = video.video.uri
            print(f"⬇️  Downloading...")
            
            headers = {'x-goog-api-key': API_KEY}
            response = requests.get(video_uri, headers=headers)
            
            if response.status_code == 200:
                output_file = "output/tinyheroes_influencer_video.mp4"
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
                size = os.path.getsize(output_file)
                print(f"✅ Video saved: {output_file} ({size:,} bytes)")
                
                print("\n" + "=" * 70)
                print("🎉 TINYHEROES VIDEO COMPLETE!")
                print("=" * 70)
                print(f"\n📹 Video: {output_file}")
                print("\n✅ The phone screen should show TinyHeroes.ai interface")
                
                return output_file
            else:
                print(f"❌ Download failed: HTTP {response.status_code}")
                return None
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    create_tinyheroes_video()
