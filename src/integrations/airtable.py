"""Airtable integration for storing generated content."""
import os
from datetime import datetime
from typing import Optional, Any
from functools import lru_cache
from pyairtable import Api

from src.core.config import settings


class AirtableManager:
    """Manages Airtable operations for AI Influencer Video Generator."""
    
    def __init__(self):
        if not settings.airtable_api_key or not settings.airtable_base_id:
            raise ValueError("AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")
        
        self.api = Api(settings.airtable_api_key)
        self.table = self.api.table(settings.airtable_base_id, settings.airtable_table_name)
    
    def create_character_record(
        self,
        job_id: str,
        description: str,
        face_image_path: Optional[str] = None,
        body_image_path: Optional[str] = None,
        side_image_path: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None
    ) -> str:
        """Create character record in Airtable."""
        record_data = {
            "Job ID": job_id,
            "Type": "Character",
            "Description": description,
            "Created At": datetime.now().isoformat(),
            "Status": "Completed"
        }
        
        attachments = []
        for path in [face_image_path, body_image_path, side_image_path]:
            if path and os.path.exists(path):
                attachments.append({"url": f"file://{os.path.abspath(path)}"})
        
        if attachments:
            record_data["Reference Images"] = attachments
        
        if metadata:
            record_data["Metadata"] = str(metadata)
        
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
        metadata: Optional[dict[str, Any]] = None
    ) -> str:
        """Create video record in Airtable."""
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
        
        attachments = []
        for path in [video_path, character_face_path]:
            if path and os.path.exists(path):
                attachments.append({"url": f"file://{os.path.abspath(path)}"})
        
        if attachments:
            record_data["Files"] = attachments
        
        if metadata:
            record_data["Metadata"] = str(metadata)
        
        record = self.table.create(record_data)
        return record["id"]
    
    def create_voiceover_record(
        self,
        job_id: str,
        script: str,
        language: str,
        audio_path: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None
    ) -> str:
        """Create voiceover record in Airtable."""
        record_data = {
            "Job ID": job_id,
            "Type": "Voiceover",
            "Script": script,
            "Language": language,
            "Created At": datetime.now().isoformat(),
            "Status": "Completed"
        }
        
        if audio_path and os.path.exists(audio_path):
            record_data["Files"] = [{"url": f"file://{os.path.abspath(audio_path)}"}]
        
        if metadata:
            record_data["Metadata"] = str(metadata)
        
        record = self.table.create(record_data)
        return record["id"]
    
    def update_record_status(
        self,
        record_id: str,
        status: str,
        error: Optional[str] = None
    ):
        """Update record status."""
        update_data = {
            "Status": status,
            "Updated At": datetime.now().isoformat()
        }
        
        if error:
            update_data["Error"] = error
        
        self.table.update(record_id, update_data)
    
    def get_record(self, record_id: str) -> dict[str, Any]:
        """Get record by ID."""
        return self.table.get(record_id)
    
    def list_records(
        self,
        filter_by_type: Optional[str] = None,
        max_records: int = 100
    ) -> list:
        """List records with optional type filter."""
        formula = f"{{Type}} = '{filter_by_type}'" if filter_by_type else None
        return self.table.all(formula=formula, max_records=max_records)


@lru_cache
def get_airtable_manager() -> Optional[AirtableManager]:
    """Get Airtable manager instance (cached)."""
    if not settings.airtable_enabled:
        return None
    
    try:
        return AirtableManager()
    except Exception as e:
        print(f"Airtable integration disabled: {e}")
        return None
