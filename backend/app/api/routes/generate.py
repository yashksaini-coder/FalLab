from fastapi import APIRouter, HTTPException, Request
from app.models.schema import GenerationRequest, GenerationResponse, GenerationStatus, ErrorResponse
from app.services.redis import RedisService
from app.services.fal_client import FalAIClient
from app.services.queue_service import QueueService
from app.core.config import get_settings
from datetime import datetime
import uuid
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


def serialize_for_redis(data):
    """Convert data to JSON-serializable format"""
    return json.loads(json.dumps(data, default=str))


@router.post(
    "/generate",
    response_model=GenerationResponse,
    summary="Submit generation request (async)",
    description="Submit a new content generation request to Fal.ai queue"
)
async def generate_content_async(
    request: Request,
    gen_request: GenerationRequest
):
    """
    Submit content generation request (queued/async)

    This endpoint queues the request and returns immediately with a request_id.
    Use the request_id to check status via /status/{request_id}

    - **model_id**: Fal.ai model endpoint_id (e.g., fal-ai/flux/dev)
    - **prompt**: Generation prompt
    - **parameters**: Model-specific parameters (optional)

    Response includes:
    - **request_id**: Unique identifier for polling status
    - **status**: "queued" initially
    - **queue_position**: Current position in queue
    """
    try:
        # Generate unique request ID
        request_id = f"req_{uuid.uuid4().hex[:12]}"

        # Get services
        redis: RedisService = request.app.state.redis
        fal_client = FalAIClient(api_key=settings.FAL_API_KEY)

        # Get all models to validate
        cache_key = "fal:models:all"
        cached_models = await redis.get(cache_key)

        if not cached_models:
            # Fetch models if not cached
            models = await fal_client._get_models_list()
            if not models:
                raise HTTPException(status_code=500, detail="Unable to fetch models from Fal.ai")
            await redis.set(cache_key, serialize_for_redis(models), ttl=settings.CACHE_TTL_MODELS)
        else:
            models = cached_models

        # Validate model exists
        model_info = fal_client.get_model_info(gen_request.model_id, models)
        if not model_info:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{gen_request.model_id}' not found in Fal.ai catalog"
            )

        logger.info(f"Submitting async generation to {gen_request.model_id}")

        # Submit to Fal.ai Queue API
        try:
            fal_response = await fal_client.submit_request(
                model_id=gen_request.model_id,
                input_data={
                    "prompt": gen_request.prompt,
                    **gen_request.parameters
                }
            )

            # Store request metadata in Redis
            request_data = {
                "request_id": request_id,
                "model_id": gen_request.model_id,
                "prompt": gen_request.prompt,
                "parameters": gen_request.parameters,
                "status": GenerationStatus.QUEUED.value,
                "created_at": datetime.utcnow().isoformat(),
                "completed_at": None,
                "result": None,
                "error": None,
                "fal_request_id": fal_response.get("request_id"),
                "queue_position": fal_response.get("queue_position")
            }

            await redis.set(
                f"generation:{request_id}",
                serialize_for_redis(request_data),
                ttl=86400  # 24 hours
            )

            logger.info(
                f"Generation request {request_id} submitted to Fal.ai "
                f"(fal_id: {fal_response.get('request_id')})"
            )

            return GenerationResponse(
                request_id=request_id,
                status=GenerationStatus.QUEUED,
                model_id=gen_request.model_id,
                created_at=datetime.utcnow(),
                queue_position=fal_response.get("queue_position")
            )

        except Exception as fal_error:
            logger.error(f"Fal.ai submission error: {str(fal_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to submit to Fal.ai: {str(fal_error)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting generation request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit generation request: {str(e)}"
        )


@router.post(
    "/generate/sync",
    response_model=GenerationResponse,
    summary="Generate synchronously (blocking)",
    description="Submit a generation request and wait for completion"
)
async def generate_content_sync(
    request: Request,
    gen_request: GenerationRequest
):
    """
    Submit content generation request (sync/blocking)

    This endpoint waits for completion and returns the result.
    WARNING: May timeout for long-running models (>5 minutes).

    Use async generation (/generate) for large models.

    - **model_id**: Fal.ai model endpoint_id
    - **prompt**: Generation prompt
    - **parameters**: Model-specific parameters (optional)
    """
    try:
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        redis: RedisService = request.app.state.redis
        fal_client = FalAIClient(api_key=settings.FAL_API_KEY)

        # Get models for validation
        cache_key = "fal:models:all"
        cached_models = await redis.get(cache_key)

        if not cached_models:
            models = await fal_client._get_models_list()
            if not models:
                raise HTTPException(status_code=500, detail="Unable to fetch models")
            await redis.set(cache_key, serialize_for_redis(models), ttl=settings.CACHE_TTL_MODELS)
        else:
            models = cached_models

        # Validate model exists
        model_info = fal_client.get_model_info(gen_request.model_id, models)
        if not model_info:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{gen_request.model_id}' not found"
            )

        logger.info(f"Submitting sync generation request for {gen_request.model_id}")

        # Call Fal.ai synchronously
        try:
            result = await fal_client.generate_sync(
                model_id=gen_request.model_id,
                input_data={
                    "prompt": gen_request.prompt,
                    **gen_request.parameters
                }
            )

            # Store result in Redis
            request_data = {
                "request_id": request_id,
                "model_id": gen_request.model_id,
                "prompt": gen_request.prompt,
                "parameters": gen_request.parameters,
                "status": GenerationStatus.COMPLETED.value,
                "created_at": datetime.utcnow().isoformat(),
                "completed_at": datetime.utcnow().isoformat(),
                "result": result,
                "error": None,
                "fal_request_id": None,
                "queue_position": None
            }

            await redis.set(
                f"generation:{request_id}",
                serialize_for_redis(request_data),
                ttl=86400
            )

            logger.info(f"Sync generation completed: {request_id}")

            return GenerationResponse(
                request_id=request_id,
                status=GenerationStatus.COMPLETED,
                model_id=gen_request.model_id,
                created_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                result=result
            )

        except Exception as fal_error:
            error_msg = str(fal_error)
            logger.error(f"Fal.ai generation error: {error_msg}")

            # Store error in Redis
            request_data = {
                "request_id": request_id,
                "model_id": gen_request.model_id,
                "prompt": gen_request.prompt,
                "parameters": gen_request.parameters,
                "status": GenerationStatus.FAILED.value,
                "created_at": datetime.utcnow().isoformat(),
                "completed_at": datetime.utcnow().isoformat(),
                "result": None,
                "error": error_msg,
                "fal_request_id": None,
                "queue_position": None
            }

            await redis.set(
                f"generation:{request_id}",
                serialize_for_redis(request_data),
                ttl=86400
            )

            raise HTTPException(
                status_code=500,
                detail=f"Generation failed: {error_msg}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in sync generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process generation: {str(e)}"
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

    Poll this endpoint to get updates on:
    - status: queued → processing → completed/failed
    - result: Generation output (if completed)
    - error: Error message (if failed)
    - queue_position: Current position (if queued)

    - **request_id**: Request ID from /generate endpoint
    """
    try:
        redis: RedisService = request.app.state.redis

        # Get request data from Redis
        request_data = await redis.get(f"generation:{request_id}")

        if not request_data:
            # Check with Fal.ai directly if stored
            raise HTTPException(
                status_code=404,
                detail=f"Request '{request_id}' not found"
            )

        # Ensure status is properly set
        status_str = request_data.get("status", "queued")
        if isinstance(status_str, str):
            try:
                request_data["status"] = GenerationStatus(status_str)
            except ValueError:
                request_data["status"] = GenerationStatus.QUEUED

        # Parse datetime strings
        if isinstance(request_data.get("created_at"), str):
            try:
                request_data["created_at"] = datetime.fromisoformat(
                    request_data["created_at"].replace("Z", "+00:00")
                )
            except:
                request_data["created_at"] = datetime.utcnow()

        if request_data.get("completed_at") and isinstance(request_data["completed_at"], str):
            try:
                request_data["completed_at"] = datetime.fromisoformat(
                    request_data["completed_at"].replace("Z", "+00:00")
                )
            except:
                request_data["completed_at"] = None

        logger.debug(f"Status check for {request_id}: {request_data['status']}")

        return GenerationResponse(**request_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to check status: {str(e)}")
