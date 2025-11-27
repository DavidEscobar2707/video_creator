"""
Overlay TinyHeroes.ai image on phone screen in existing video
"""
import os
import subprocess


def overlay_tinyheroes_on_video(
    influencer_video="output/influencer_video.mp4",
    tinyheroes_image="assets/tinyheroes_screenshot.jpg",
    output_file="output/final_tinyheroes_video.mp4",
    # Adjust these coordinates based on phone position in video
    x=500,
    y=400,
    width=350,
    height=700
):
    """
    Overlay TinyHeroes.ai screenshot on phone screen
    
    Args:
        influencer_video: Video of influencer holding phone
        tinyheroes_image: Screenshot of TinyHeroes.ai interface
        output_file: Final video output
        x, y: Position of phone screen
        width, height: Size of phone screen
    """
    print("=" * 70)
    print("📱 OVERLAYING TINYHEROES.AI ON PHONE SCREEN")
    print("=" * 70)
    
    # Check files
    if not os.path.exists(influencer_video):
        print(f"❌ Video not found: {influencer_video}")
        return None
    
    if not os.path.exists(tinyheroes_image):
        print(f"❌ Image not found: {tinyheroes_image}")
        print("\n💡 Please save a screenshot of TinyHeroes.ai as:")
        print(f"   {tinyheroes_image}")
        return None
    
    print(f"\n📹 Video: {influencer_video}")
    print(f"📸 Image: {tinyheroes_image}")
    print(f"📐 Position: x={x}, y={y}, size={width}x{height}")
    
    try:
        print("\n🔧 Processing with FFmpeg...")
        
        cmd = [
            "ffmpeg",
            "-i", influencer_video,
            "-i", tinyheroes_image,
            "-filter_complex",
            f"[1:v]scale={width}:{height}[overlay];"
            f"[0:v][overlay]overlay={x}:{y}",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "copy",
            "-y",
            output_file
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            size = os.path.getsize(output_file)
            print(f"\n✅ Video created: {output_file} ({size:,} bytes)")
            print("\n🎬 Review the video and adjust x, y, width, height if needed")
            return output_file
        else:
            print(f"❌ FFmpeg error:")
            print(result.stderr[-500:])
            return None
            
    except FileNotFoundError:
        print("❌ FFmpeg not installed")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    print("\n💡 To use this script:")
    print("   1. Save a screenshot of TinyHeroes.ai interface")
    print("   2. Place it in: assets/tinyheroes_screenshot.jpg")
    print("   3. Run: python overlay_tinyheroes.py")
    print("\n   Or use Option 1: python create_video_tinyheroes.py")
    print("   (Regenerate video with TinyHeroes in the prompt)\n")
