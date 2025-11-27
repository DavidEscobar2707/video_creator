"""
Check available models in Gemini API
"""
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

print("=" * 70)
print("📋 AVAILABLE MODELS IN GEMINI API")
print("=" * 70)

try:
    models = client.models.list()
    
    print("\n🎨 Image Generation Models:")
    image_models = []
    
    print("\n🎬 Video Generation Models:")
    video_models = []
    
    print("\n💬 Text Generation Models:")
    text_models = []
    
    for model in models:
        name = model.name
        
        if "imagen" in name.lower() or "image" in name.lower():
            image_models.append(name)
            print(f"   - {name}")
        elif "veo" in name.lower() or "video" in name.lower():
            video_models.append(name)
            print(f"   - {name}")
        elif "gemini" in name.lower():
            text_models.append(name)
            print(f"   - {name}")
    
    if not image_models:
        print("   ❌ No image generation models found")
    
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Image models: {len(image_models)}")
    print(f"Video models: {len(video_models)}")
    print(f"Text models: {len(text_models)}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
