"""
AI Influencer Video Generator - Main Application
Professional video generation pipeline using Veo3
"""
from src.config import Config
from src.character_generator import CharacterReferenceGenerator
from src.veo_generator import Veo3Generator
from src.audio_generator import AudioGenerator
from src.video_composer import VideoComposer


class InfluencerVideoGenerator:
    """Main application class for generating influencer videos"""
    
    def __init__(self):
        """Initialize the video generator"""
        # Validate configuration
        Config.validate()
        
        # Initialize components
        self.character_gen = CharacterReferenceGenerator()
        self.veo_gen = Veo3Generator()
        self.audio_gen = AudioGenerator()
        self.video_composer = VideoComposer()
    
    def create_character_references(
        self,
        character_description,
        output_prefix="references/character"
    ):
        """
        Step 1: Create character reference images
        
        Args:
            character_description: Description of the influencer character
            output_prefix: Prefix for output files
            
        Returns:
            Dictionary with paths to reference images
        """
        print("\n" + "=" * 60)
        print("STEP 1: CREATING CHARACTER REFERENCES")
        print("=" * 60)
        
        return self.character_gen.generate_all_references(
            character_description=character_description,
            output_prefix=output_prefix
        )
    
    def generate_influencer_video(
        self,
        character_references,
        product_description,
        output_file="output/influencer_video.mp4"
    ):
        """
        Step 2: Generate influencer video with Veo3
        
        Args:
            character_references: Dict with character reference image paths
            product_description: Description of product to show
            output_file: Path to save video
            
        Returns:
            Path to generated video
        """
        print("\n" + "=" * 60)
        print("STEP 2: GENERATING INFLUENCER VIDEO")
        print("=" * 60)
        
        return self.veo_gen.generate_influencer_video(
            character_references=character_references,
            product_description=product_description,
            output_file=output_file
        )
    
    def generate_voiceover(
        self,
        script,
        output_file="temp/voiceover.mp3",
        language="en"
    ):
        """
        Step 3: Generate voiceover audio
        
        Args:
            script: Text script for voiceover
            output_file: Path to save audio
            language: Language code
            
        Returns:
            Path to generated audio
        """
        print("\n" + "=" * 60)
        print("STEP 3: GENERATING VOICEOVER")
        print("=" * 60)
        
        return self.audio_gen.generate_voiceover(
            text=script,
            output_file=output_file,
            language=language
        )
    
    def compose_final_video(
        self,
        influencer_video,
        product_video=None,
        voiceover_audio=None,
        output_file="output/final_video.mp4"
    ):
        """
        Step 4: Compose final video
        
        Args:
            influencer_video: Path to influencer video
            product_video: Path to product demo (optional)
            voiceover_audio: Path to voiceover (optional)
            output_file: Path to save final video
            
        Returns:
            Path to final video
        """
        print("\n" + "=" * 60)
        print("STEP 4: COMPOSING FINAL VIDEO")
        print("=" * 60)
        
        return self.video_composer.compose_final_video(
            influencer_video=influencer_video,
            product_video=product_video,
            voiceover_audio=voiceover_audio,
            output_file=output_file
        )
    
    def create_complete_video(
        self,
        character_description,
        product_description,
        script,
        product_video=None
    ):
        """
        Complete pipeline: Create influencer video from scratch
        
        Args:
            character_description: Description of influencer character
            product_description: Description of product
            script: Voiceover script
            product_video: Optional product demo video
            
        Returns:
            Path to final video
        """
        print("\n" + "=" * 70)
        print(" " * 15 + "AI INFLUENCER VIDEO GENERATOR")
        print("=" * 70)
        
        # Step 1: Create character references
        character_refs = self.create_character_references(
            character_description=character_description
        )
        
        if not any(character_refs.values()):
            print("\n❌ Failed to create character references")
            return None
        
        # Step 2: Generate influencer video
        influencer_video = self.generate_influencer_video(
            character_references=character_refs,
            product_description=product_description
        )
        
        if not influencer_video:
            print("\n❌ Failed to generate influencer video")
            return None
        
        # Step 3: Generate voiceover
        voiceover = self.generate_voiceover(script=script)
        
        # Step 4: Compose final video
        final_video = self.compose_final_video(
            influencer_video=influencer_video,
            product_video=product_video,
            voiceover_audio=voiceover
        )
        
        if final_video:
            print("\n" + "=" * 70)
            print("🎉 SUCCESS! VIDEO GENERATION COMPLETE")
            print("=" * 70)
            print(f"\n📹 Final video: {final_video}")
            print("\n🎬 Ready to publish to social media!")
        
        return final_video


# Example usage
if __name__ == "__main__":
    # Configuration
    CHARACTER_DESC = """
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
    
    # Initialize generator
    generator = InfluencerVideoGenerator()
    
    # Option 1: Just create character references (RECOMMENDED TO START)
    print("\n🎯 Creating character references only...")
    print("   (Use these images with Veo3 later)\n")
    
    character_refs = generator.create_character_references(
        character_description=CHARACTER_DESC,
        output_prefix="references/my_influencer"
    )
    
    print("\n✅ Character references created!")
    print("\n📝 Next steps:")
    print("   1. Review the generated reference images")
    print("   2. Use them to generate videos with Veo3")
    print("   3. Run the complete pipeline if satisfied")
    
    # Option 2: Complete pipeline (uncomment to run full generation)
    # final_video = generator.create_complete_video(
    #     character_description=CHARACTER_DESC,
    #     product_description=PRODUCT_DESC,
    #     script=SCRIPT,
    #     product_video="WhatsApp Video 2025-11-24 at 2.49.58 PM.mp4"
    # )
