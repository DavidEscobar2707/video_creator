"""Audio/voiceover generation using TTS."""
from pathlib import Path
from typing import Optional
from gtts import gTTS

from .config import settings


class AudioGenerator:
    """Generates voiceover audio using TTS."""
    
    def generate_voiceover(
        self,
        text: str,
        output_path: Optional[Path] = None,
        language: str = "en",
        slow: bool = False
    ) -> Optional[Path]:
        """
        Generate voiceover audio from text.
        
        Args:
            text: Script text to convert to speech
            output_path: Path to save audio file
            language: Language code (en, es, etc.)
            slow: Whether to use slow speech
            
        Returns:
            Path to generated audio or None
        """
        output_path = output_path or settings.temp_dir / "voiceover.mp3"
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(str(output_path))
            return output_path
            
        except Exception as e:
            print(f"Error generating voiceover: {e}")
            return None
    
    @staticmethod
    def generate_script(product_name: str, features: list[str]) -> str:
        """Generate professional influencer script."""
        features_text = ", ".join(features[:3])
        
        return f"""
        Hey everyone! I'm so excited to show you {product_name}.
        
        This is a game-changer. It has {features_text}, 
        and it's made my life so much easier.
        
        If you're looking for something that actually works, 
        you need to check this out. Link in bio!
        """.strip()
