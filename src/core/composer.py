"""Video composition using FFmpeg."""
import subprocess
from pathlib import Path
from typing import Optional

from .config import settings


class VideoComposer:
    """Composes final videos using FFmpeg."""
    
    def compose(
        self,
        video_path: Path,
        audio_path: Optional[Path] = None,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Compose final video with optional audio.
        
        Args:
            video_path: Path to input video
            audio_path: Path to audio file (optional)
            output_path: Path to save final video
            
        Returns:
            Path to final video or None
        """
        if not video_path.exists():
            return None
        
        output_path = output_path or settings.output_dir / "final_video.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if audio_path and audio_path.exists():
            return self._add_audio(video_path, audio_path, output_path)
        else:
            return self._copy_video(video_path, output_path)
    
    def concatenate(
        self,
        video1: Path,
        video2: Path,
        output_path: Optional[Path] = None,
        audio_path: Optional[Path] = None
    ) -> Optional[Path]:
        """Concatenate two videos with optional audio."""
        output_path = output_path or settings.output_dir / "concatenated.mp4"
        
        try:
            cmd = [
                "ffmpeg",
                "-i", str(video1),
                "-i", str(video2),
                "-filter_complex",
                f"[0:v]scale={settings.video_width}:{settings.video_height}:force_original_aspect_ratio=decrease,"
                f"pad={settings.video_width}:{settings.video_height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={settings.video_fps}[v0];"
                f"[1:v]scale={settings.video_width}:{settings.video_height}:force_original_aspect_ratio=decrease,"
                f"pad={settings.video_width}:{settings.video_height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={settings.video_fps}[v1];"
                "[v0][v1]concat=n=2:v=1:a=0[vout]",
                "-map", "[vout]",
            ]
            
            if audio_path and audio_path.exists():
                cmd.extend(["-i", str(audio_path), "-map", "2:a"])
            
            cmd.extend([
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",
                str(output_path)
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return output_path if result.returncode == 0 else None
            
        except Exception as e:
            print(f"Error concatenating videos: {e}")
            return None
    
    def _add_audio(self, video: Path, audio: Path, output: Path) -> Optional[Path]:
        """Add audio to video."""
        try:
            cmd = [
                "ffmpeg",
                "-i", str(video),
                "-i", str(audio),
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                "-y",
                str(output)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return output if result.returncode == 0 else None
            
        except Exception as e:
            print(f"Error adding audio: {e}")
            return None
    
    def _copy_video(self, input_path: Path, output: Path) -> Optional[Path]:
        """Copy video to output location."""
        try:
            cmd = ["ffmpeg", "-i", str(input_path), "-c", "copy", "-y", str(output)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return output if result.returncode == 0 else None
            
        except Exception as e:
            print(f"Error copying video: {e}")
            return None
