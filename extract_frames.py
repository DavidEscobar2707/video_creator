"""
Extract Character Reference Frames from Existing Video
Useful if you already have a video and want to extract 3 reference images
"""
import os
import sys
import subprocess


def extract_frames_from_video(video_path, output_prefix="references/character"):
    """
    Extract 3 frames from video at different timestamps
    
    Args:
        video_path: Path to input video
        output_prefix: Prefix for output files
        
    Returns:
        Dict with paths to extracted frames
    """
    print("=" * 70)
    print("📹 EXTRACTING CHARACTER REFERENCES FROM VIDEO")
    print("=" * 70)
    
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return None
    
    print(f"\n📹 Input video: {video_path}")
    
    # Create output directory
    os.makedirs("references", exist_ok=True)
    
    # Extract 3 frames at different timestamps
    frames = {
        "face": f"{output_prefix}_face.jpg",
        "body": f"{output_prefix}_body.jpg",
        "side": f"{output_prefix}_side.jpg"
    }
    
    timestamps = ["00:00:01", "00:00:03", "00:00:05"]  # 1s, 3s, 5s
    
    try:
        for i, (frame_type, output_path) in enumerate(frames.items()):
            timestamp = timestamps[i]
            
            print(f"\n📸 Extracting {frame_type} at {timestamp}...")
            
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-ss", timestamp,
                "-vframes", "1",
                "-q:v", "2",  # High quality
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"   ✅ Saved: {output_path} ({size:,} bytes)")
            else:
                print(f"   ❌ Failed to extract frame")
                frames[frame_type] = None
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 EXTRACTION SUMMARY")
        print("=" * 70)
        
        success_count = sum(1 for v in frames.values() if v and os.path.exists(v))
        
        for frame_type, path in frames.items():
            if path and os.path.exists(path):
                print(f"✅ {frame_type.capitalize()}: {path}")
            else:
                print(f"❌ {frame_type.capitalize()}: Failed")
        
        print(f"\n✅ Successfully extracted {success_count}/3 frames")
        
        if success_count == 3:
            print("\n🎉 All frames extracted!")
            print("✅ Ready to create video! Run: python create_video.py")
        
        return frames
        
    except FileNotFoundError:
        print("\n❌ FFmpeg not found!")
        print("   Install FFmpeg: https://ffmpeg.org/download.html")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n📋 Usage: python extract_frames.py <video_file>")
        print("\nExample:")
        print("  python extract_frames.py temp_influencer.mp4")
        print("\nThis will extract 3 frames and save them as:")
        print("  - references/character_face.jpg")
        print("  - references/character_body.jpg")
        print("  - references/character_side.jpg")
        sys.exit(1)
    
    video_path = sys.argv[1]
    extract_frames_from_video(video_path)
