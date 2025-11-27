"""
Airtable Integration Module
Saves generated videos and character references to Airtable
"""
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

# Airtable Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "AI_Influencer_Videos")


class AirtableManager:
    """Manages Airtable operations for AI Influencer Video Generator"""
    
    def __init__(self):
        """Initialize Airtable connection"""
        if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
            raise ValueError(
                "AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set in .env file"
            )
        
        self.api = Api(AIRTABLE_API_KEY)
        self.table = self.api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    
    def upload_attachment(self, file_path: str) -> Dict[str, str]:
        """
        Upload file as Airtable attachment
        
        Args:
            file_path: Path to file to upload
            
        Returns:
            Dict with url and filename
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Airtable accepts attachments as URLs or base64
        # For now, we'll return the local path and let Airtable handle it
        filename = os.path.basename(file_path)
        
        # Read file as bytes for upload
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Return attachment format for Airtable
        return {
            "filename": filename,
            "url": file_path  # In production, upload to cloud storage first
        }
    
    def create_character_record(
        self,
        job_id: str,
        description: str,
        face_image_path: Optional[str] = None,
        body_image_path: Optional[str] = None,
        side_image_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create character record in Airtable
        
        Args:
            job_id: Unique job identifier
            description: Character description
            face_image_path: Path to face reference image
            body_image_path: Path to body reference image
            side_image_path: Path to side reference image
            metadata: Additional metadata
            
        Returns:
            Airtable record ID
        """
        record_data = {
            "Job ID": job_id,
            "Type": "Character",
            "Description": description,
            "Created At": datetime.now().isoformat(),
            "Status": "Completed"
        }
        
        # Add images as attachments
        attachments = []
        
        if face_image_path and os.path.exists(face_image_path):
            attachments.append({
                "url": f"file://{os.path.abspath(face_image_path)}"
            })
        
        if body_image_path and os.path.exists(body_image_path):
            attachments.append({
                "url": f"file://{os.path.abspath(body_image_path)}"
            })
        
        if side_image_path and os.path.exists(side_image_path):
            attachments.append({
                "url": f"file://{os.path.abspath(side_image_path)}"
            })
        
        if attachments:
            record_data["Reference Images"] = attachments
        
        # Add metadata
        if metadata:
            record_data["Metadata"] = str(metadata)
        
        # Create record
        record = self.table.create(record_data)
        
        return record["id"]
    
    def create_video_record(
        self,
        job_id: str,
        prompt: str,
        product_description: str,
        video_path: Optional[str] = None,
        character_face_path: Optional[str] = None,
        aspect_ratio: str = "9:16",
        duration_seconds: int = 8,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create video record in Airtable
        
        Args:
            job_id: Unique job identifier
            prompt: Video generation prompt
            product_description: Product description
            video_path: Path to generated video
            character_face_path: Path to character reference
            aspect_ratio: Video aspect ratio
            duration_seconds: Video duration
            metadata: Additional metadata
            
        Returns:
            Airtable record ID
        """
        record_data = {
            "Job ID": job_id,
            "Type": "Video",
            "Prompt": prompt,
            "Product Description": product_description,
            "Aspect Ratio": aspect_ratio,
            "Duration (seconds)": duration_seconds,
            "Created At": datetime.now().isoformat(),
            "Status": "Completed"
        }
        
        # Add video as attachment
        attachments = []
        
        if video_path and os.path.exists(video_path):
            attachments.append({
                "url": f"file://{os.path.abspath(video_path)}"
            })
        
        if character_face_path and os.path.exists(character_face_path):
            attachments.append({
                "url": f"file://{os.path.abspath(character_face_path)}"
            })
        
        if attachments:
            record_data["Files"] = attachments
        
        # Add metadata
        if metadata:
            record_data["Metadata"] = str(metadata)
        
        # Create record
        record = self.table.create(record_data)
        
        return record["id"]
    
    def create_voiceover_record(
        self,
        job_id: str,
        script: str,
        language: str,
        audio_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create voiceover record in Airtable
        
        Args:
            job_id: Unique job identifier
            script: Voiceover script
            language: Language code
            audio_path: Path to generated audio
            metadata: Additional metadata
            
        Returns:
            Airtable record ID
        """
        record_data = {
            "Job ID": job_id,
            "Type": "Voiceover",
            "Script": script,
            "Language": language,
            "Created At": datetime.now().isoformat(),
            "Status": "Completed"
        }
        
        # Add audio as attachment
        if audio_path and os.path.exists(audio_path):
            record_data["Files"] = [{
                "url": f"file://{os.path.abspath(audio_path)}"
            }]
        
        # Add metadata
        if metadata:
            record_data["Metadata"] = str(metadata)
        
        # Create record
        record = self.table.create(record_data)
        
        return record["id"]
    
    def update_record_status(
        self,
        record_id: str,
        status: str,
        error: Optional[str] = None
    ):
        """
        Update record status
        
        Args:
            record_id: Airtable record ID
            status: New status
            error: Error message if failed
        """
        update_data = {
            "Status": status,
            "Updated At": datetime.now().isoformat()
        }
        
        if error:
            update_data["Error"] = error
        
        self.table.update(record_id, update_data)
    
    def get_record(self, record_id: str) -> Dict[str, Any]:
        """
        Get record by ID
        
        Args:
            record_id: Airtable record ID
            
        Returns:
            Record data
        """
        return self.table.get(record_id)
    
    def list_records(
        self,
        filter_by_type: Optional[str] = None,
        max_records: int = 100
    ) -> list:
        """
        List records
        
        Args:
            filter_by_type: Filter by type (Character, Video, Voiceover)
            max_records: Maximum number of records to return
            
        Returns:
            List of records
        """
        formula = None
        if filter_by_type:
            formula = f"{{Type}} = '{filter_by_type}'"
        
        return self.table.all(formula=formula, max_records=max_records)


# Example usage
if __name__ == "__main__":
    # Test Airtable connection
    try:
        manager = AirtableManager()
        print("✅ Airtable connection successful!")
        
        # List recent records
        records = manager.list_records(max_records=5)
        print(f"\n📋 Recent records: {len(records)}")
        
        for record in records:
            print(f"  - {record['fields'].get('Job ID')}: {record['fields'].get('Type')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure to set in .env:")
        print("   AIRTABLE_API_KEY=your_api_key")
        print("   AIRTABLE_BASE_ID=your_base_id")
        print("   AIRTABLE_TABLE_NAME=AI_Influencer_Videos")
