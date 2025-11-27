"""
Audio/Voice Generator
Handles text-to-speech generation
"""
import os
from gtts import gTTS
from .config import Config


class AudioGenerator:
    """Generates voiceover audio using TTS"""
    
    def __init__(self):
        """Initialize audio generator"""
        pass
    
    def generate_voiceover(
        self,
        text,
        output_file="temp/voiceover.mp3",
        language="en",
        slow=False
    ):
        """
        Generate voiceover audio from text
        
        Args:
            text: Script text to convert to speech
            output_file: Path to save audio file
            language: Language code (en, es, etc.)
            slow: Whether to use slow speech
            
        Returns:
            Path to generated audio or None if failed
        """
        print("=" * 60)
        print("🎤 GENERATING VOICEOVER")
        print("=" * 60)
        
        print(f"\n📝 Script: {text[:100]}...")
        print(f"🗣️  Language: {language}")
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            print("📤 Generating audio with gTTS...")
            
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(output_file)
            
            size = os.path.getsize(output_file)
            print(f"✅ Audio saved: {output_file} ({size:,} bytes)")
            
            return output_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def generate_professional_script(self, product_name, key_features):
        """
        Generate professional influencer script
        
        Args:
            product_name: Name of the product
            key_features: List of key features to highlight
            
        Returns:
            Professional script text
        """
        features_text = ", ".join(key_features[:3])  # Top 3 features
        
        script = f"""
        Hey everyone! I'm so excited to show you {product_name}.
        
        This is a game-changer. It has {features_text}, 
        and it's made my life so much easier.
        
        If you're looking for something that actually works, 
        you need to check this out. Link in bio!
        """
        
        return script.strip()
