from fastapi import APIRouter, HTTPException, Request
from app.models.schema import GenerationRequest, GenerationResponse, GenerationStatus, ErrorResponse
from app.services.redis import RedisService
from app.services.queue_service import QueueService
from datetime import datetime
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/generate",
    response_model=GenerationResponse,
    summary="Submit generation request",
    description="Submit a new content generation request"
)
async def generate_content(
    request: Request,
    gen_request: GenerationRequest
):
    """
    Submit content generation request

    This endpoint queues the request and returns immediately.
    Use the request_id to check status via /status/{request_id}

    - **model_id**: Fal.ai model identifier
    - **prompt**: Generation prompt
    - **parameters**: Model-specific parameters
    """
    try:
        # Generate unique request ID
        request_id = f"req_{uuid.uuid4().hex[:12]}"

        # Get services
        redis: RedisService = request.app.state.redis
        queue_service = QueueService(redis)

        # Prepare request data
        request_data = {
            "request_id": request_id,
            "model_id": gen_request.model_id,
            "prompt": gen_request.prompt,
            "parameters": gen_request.parameters,
            "status": GenerationStatus.QUEUED.value,
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "result": None,
            "error": None
        }

        # Store request metadata in Redis
        await redis.set(f"generation:{request_id}", request_data)

        # Add to processing queue
        queue_position = await queue_service.enqueue(request_id)

        logger.info(f"Generation request {request_id} queued at position {queue_position}")

        return GenerationResponse(
            request_id=request_id,
            status=GenerationStatus.QUEUED,
            model_id=gen_request.model_id,
            created_at=datetime.utcnow(),
            queue_position=queue_position
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting generation request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit generation request: {str(e)}"
        )

@router.get(
    "/status/{request_id}",
    response_model=GenerationResponse,
    summary="Check generation status",
    description="Get the current status and result of a generation request"
)
async def check_status(request: Request, request_id: str):
    """
    Check generation request status

    - **request_id**: Request ID from /generate endpoint
    """
    try:
        redis: RedisService = request.app.state.redis

        # Get request data
        request_data = await redis.get(f"generation:{request_id}")

        if not request_data:
            raise HTTPException(
                status_code=404,
                detail=f"Request {request_id} not found"
            )

        # Ensure status is a string (from enum)
        if isinstance(request_data.get("status"), str):
            request_data["status"] = GenerationStatus(request_data["status"])

        # Parse datetime strings
        if isinstance(request_data.get("created_at"), str):
            request_data["created_at"] = datetime.fromisoformat(request_data["created_at"].replace("Z", "+00:00"))
        if request_data.get("completed_at") and isinstance(request_data["completed_at"], str):
            request_data["completed_at"] = datetime.fromisoformat(request_data["completed_at"].replace("Z", "+00:00"))

        return GenerationResponse(**request_data)

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Invalid request data format: {e}")
        raise HTTPException(status_code=500, detail="Invalid request data format")
    except Exception as e:
        logger.error(f"Error checking status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to check status: {str(e)}")
