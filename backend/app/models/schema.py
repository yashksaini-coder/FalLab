from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

class ModelMetadata(BaseModel):
    """Fal.ai model metadata as returned from the API"""
    display_name: str = Field(..., description="Human-readable model name")
    category: str = Field(..., description="Model category (e.g., text-to-image, image-to-video)")
    description: Optional[str] = Field(None, description="Detailed model description")
    status: str = Field("active", description="Model status (active, deprecated, etc.)")
    tags: List[str] = Field(default_factory=list, description="Model tags for categorization")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    thumbnail_url: Optional[str] = Field(None, description="Model thumbnail image URL")
    thumbnail_animated_url: Optional[str] = Field(None, description="Animated thumbnail URL")
    model_url: Optional[str] = Field(None, description="URL to the model page")
    license_type: Optional[str] = Field(None, description="License type (e.g., commercial, open-source)")
    group: Optional[Dict[str, Any]] = Field(None, description="Model group information")
    pinned: Optional[bool] = Field(False, description="Whether model is pinned/featured")
    highlighted: Optional[bool] = Field(False, description="Whether model is highlighted")
    duration_estimate: Optional[int] = Field(None, description="Estimated execution time in seconds")

    class Config:
        populate_by_name = True
        extra = "allow"  # Allow additional fields from Fal.ai API

class ModelInfo(BaseModel):
    """Complete model information including endpoint and metadata"""
    endpoint_id: str = Field(..., description="Unique model endpoint identifier (e.g., fal-ai/flux/dev)")
    metadata: ModelMetadata = Field(..., description="Model metadata from Fal.ai")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "endpoint_id": "fal-ai/flux/dev",
                "metadata": {
                    "display_name": "FLUX.1 [dev]",
                    "category": "text-to-image",
                    "description": "High-quality text-to-image generation model",
                    "status": "active",
                    "tags": ["fast", "high-quality"],
                    "license_type": "commercial",
                    "pinned": True
                }
            }
        }

    @property
    def model_id(self) -> str:
        """Alias for endpoint_id for backward compatibility"""
        return self.endpoint_id

    @property
    def category(self) -> str:
        """Get model category"""
        return self.metadata.category

    @property
    def display_name(self) -> str:
        """Get display name"""
        return self.metadata.display_name

class GenerationRequest(BaseModel):
    model_id: str = Field(..., description="Fal.ai model ID (endpoint_id)", min_length=1)
    prompt: str = Field(..., description="Generation prompt", min_length=1, max_length=2000)
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Model-specific parameters")

    @validator('model_id')
    def validate_model_id(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Model ID cannot be empty")
        return v.strip()

    @validator('prompt')
    def validate_prompt(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Prompt cannot be empty")
        return v.strip()
    
    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "model_id": "fal-ai/flux/dev",
                "prompt": "A serene mountain landscape at sunset",
                "parameters": {
                    "width": 1024,
                    "height": 1024,
                    "num_images": 1
                }
            }
        }

class GenerationStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GenerationResponse(BaseModel):
    request_id: str = Field(..., description="Unique request identifier")
    status: GenerationStatus = Field(..., description="Current status")
    model_id: str = Field(..., description="Model used")
    created_at: datetime = Field(..., description="Request creation time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    result: Optional[Dict[str, Any]] = Field(None, description="Generation result")
    error: Optional[str] = Field(None, description="Error message if failed")
    queue_position: Optional[int] = Field(None, description="Position in queue")

    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_abc123",
                "status": "completed",
                "model_id": "fal-ai/flux/dev",
                "created_at": "2024-12-14T20:50:00Z",
                "completed_at": "2024-12-14T20:50:15Z",
                "result": {
                    "images": [
                        {"url": "https://fal.media/files/abc.jpg", "content_type": "image/jpeg"}
                    ]
                },
                "error": None,
                "queue_position": None
            }
        }

class ModelsListResponse(BaseModel):
    """Response from Fal.ai models list API"""
    models: List[ModelInfo] = Field(..., description="List of available models")
    total: int = Field(..., description="Total number of models")
    next_cursor: Optional[str] = Field(None, description="Cursor for pagination")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")

