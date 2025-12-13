from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

class ModelCategory(str, Enum):
    TEXT_TO_IMAGE = "text-to-image"
    IMAGE_TO_IMAGE = "image-to-image"
    TEXT_TO_VIDEO = "text-to-video"
    TEXT_GENERATION = "text-generation"
    AUDIO_GENERATION = "audio-generation"
    OTHER = "other"

class ModelInfo(BaseModel):
    model_id: str = Field(..., description="Unique model identifier", alias="id")
    name: str = Field(..., description="Human-readable model name")
    description: Optional[str] = Field(None, description="Model description")
    category: ModelCategory = Field(..., description="Model category")
    pricing: Optional[Dict[str, Any]] = Field(None, description="Pricing information")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Available parameters")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "fal-ai/flux/dev",
                "name": "FLUX.1 [dev]",
                "description": "High-quality image generation model",
                "category": "text-to-image",
                "pricing": {"per_image": 0.025},
                "parameters": {
                    "prompt": {"type": "string", "required": True},
                    "width": {"type": "integer", "default": 1024},
                    "height": {"type": "integer", "default": 1024}
                }
            }
        }

class GenerationRequest(BaseModel):
    model_id: str = Field(..., description="Fal.ai model ID", min_length=1, alias="model_id")
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
        protected_namespaces = ()  # Fix Pydantic warning about model_id
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
                "created_at": "2024-12-13T10:30:00Z",
                "completed_at": "2024-12-13T10:30:15Z",
                "result": {
                    "images": [
                        {"url": "https://fal.media/files/abc.jpg", "content_type": "image/jpeg"}
                    ]
                },
                "error": None,
                "queue_position": None
            }
        }

class ModelSearchResponse(BaseModel):
    models: List[ModelInfo] = Field(..., description="List of models")
    total: int = Field(..., description="Total number of results")
    query: Optional[str] = Field(None, description="Search query used")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")
