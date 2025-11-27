"""
Video Composer
Handles video composition and editing using FFmpeg
"""
import os
import subprocess
from .config import Config


class VideoComposer:
    """Composes final videos using FFmpeg"""
    
    def __init__(self):
        """Initialize video composer"""
        pass
    
    def compose_final_video(
        self,
        influencer_video,
        product_video=None,
        voiceover_audio=None,
        output_file="output/final_video.mp4"
    ):
        """
        Compose final video from components
        
        Args:
            influencer_video: Path to influencer video
            product_video: Path to product demo video (optional)
            voiceover_audio: Path to voiceover audio (optional)
            output_file: Path to save final video
            
        Returns:
            Path to final video or None if failed
        """
        print("=" * 60)
        print("🎬 COMPOSING FINAL VIDEO")
        print("=" * 60)
        
        # Verify inputs
        if not os.path.exists(influencer_video):
            print(f"❌ Influencer video not found: {influencer_video}")
            return None
        
        print(f"\n📹 Influencer video: {influencer_video}")
        
        if product_video and os.path.exists(product_video):
            print(f"📱 Product video: {product_video}")
        
        if voiceover_audio and os.path.exists(voiceover_audio):
            print(f"🎤 Voiceover: {voiceover_audio}")
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            print("\n🔧 Processing with FFmpeg...")
            
            # Build FFmpeg command based on available inputs
            if product_video and os.path.exists(product_video):
                # Concatenate influencer + product videos
                result = self._concatenate_videos(
                    influencer_video,
                    product_video,
                    voiceover_audio,
                    output_file
                )
            elif voiceover_audio and os.path.exists(voiceover_audio):
                # Just add voiceover to influencer video
                result = self._add_audio(
                    influencer_video,
                    voiceover_audio,
                    output_file
                )
            else:
                # Just copy influencer video
                result = self._copy_video(influencer_video, output_file)
            
            if result:
                size = os.path.getsize(output_file)
                print(f"\n✅ Final video created: {output_file} ({size:,} bytes)")
                return output_file
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def _concatenate_videos(self, video1, video2, audio, output):
        """Concatenate two videos with optional audio"""
        try:
            cmd = [
                "ffmpeg",
                "-i", video1,
                "-i", video2,
                "-filter_complex",
                f"[0:v]scale={Config.VIDEO_WIDTH}:{Config.VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
                f"pad={Config.VIDEO_WIDTH}:{Config.VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={Config.VIDEO_FPS}[v0];"
                f"[1:v]scale={Config.VIDEO_WIDTH}:{Config.VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
                f"pad={Config.VIDEO_WIDTH}:{Config.VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={Config.VIDEO_FPS}[v1];"
                "[v0][v1]concat=n=2:v=1:a=0[vout]",
                "-map", "[vout]",
            ]
            
            if audio and os.path.exists(audio):
                cmd.extend(["-i", audio, "-map", "2:a"])
            
            cmd.extend([
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",
                output
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Concatenation error: {e}")
            return False
    
    def _add_audio(self, video, audio, output):
        """Add audio to video"""
        try:
            cmd = [
                "ffmpeg",
                "-i", video,
                "-i", audio,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                "-y",
                output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Audio addition error: {e}")
            return False
    
    def _copy_video(self, input_video, output):
        """Copy video to output location"""
        try:
            cmd = [
                "ffmpeg",
                "-i", input_video,
                "-c", "copy",
                "-y",
                output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Copy error: {e}")
            return False
