from app.workers.celery_app import celery_app
from app.services.fal_client import FalAIClient
from app.services.redis import RedisService
from app.services.queue_service import QueueService
from app.models.schema import GenerationStatus
from app.core.config import get_settings
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

@celery_app.task(name="app.workers.tasks.process_generation", bind=True, max_retries=3)
def process_generation(self, request_id: str):
    """
    Celery task to process generation request

    This runs in a separate worker process
    """
    try:
        logger.info(f"Processing generation request: {request_id}")

        # Run async code in sync context
        return asyncio.run(_process_generation_async(request_id))

    except Exception as e:
        logger.error(f"Error processing {request_id}: {e}", exc_info=True)
        # Update status to failed
        asyncio.run(_mark_failed(request_id, str(e)))
        # Retry on certain errors
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60)
        raise

async def _process_generation_async(request_id: str) -> dict:
    """Async implementation of generation processing"""
    redis = RedisService()
    await redis.connect()

    try:
        # Get request data
        request_data = await redis.get(f"generation:{request_id}")
        if not request_data:
            raise Exception(f"Request {request_id} not found in Redis")

        # Update status to processing
        request_data["status"] = GenerationStatus.PROCESSING.value
        await redis.set(f"generation:{request_id}", request_data)

        # Call Fal.ai API
        fal_client = FalAIClient()

        # Prepare input data - prompt is required, merge with parameters
        input_data = {
            "prompt": request_data["prompt"],
            **request_data.get("parameters", {})
        }

        logger.info(f"Calling Fal.ai for {request_id} with model {request_data['model_id']}")
        result = await fal_client.generate_sync(
            model_id=request_data["model_id"],
            input_data=input_data
        )

        # Update with results
        request_data["status"] = GenerationStatus.COMPLETED.value
        request_data["completed_at"] = datetime.utcnow().isoformat()
        request_data["result"] = result
        request_data["error"] = None

        # Store updated data with TTL
        await redis.set(
            f"generation:{request_id}",
            request_data,
            ttl=settings.CACHE_TTL_GENERATION
        )

        # Mark as complete in queue service
        queue_service = QueueService(redis)
        await queue_service.mark_complete(request_id)

        logger.info(f"Generation {request_id} completed successfully")
        return request_data

    except Exception as e:
        logger.error(f"Error in generation processing for {request_id}: {e}", exc_info=True)
        raise
    finally:
        await redis.disconnect()

async def _mark_failed(request_id: str, error: str):
    """Mark request as failed"""
    redis = RedisService()
    await redis.connect()

    try:
        request_data = await redis.get(f"generation:{request_id}")
        if request_data:
            request_data["status"] = GenerationStatus.FAILED.value
            request_data["completed_at"] = datetime.utcnow().isoformat()
            request_data["error"] = error
            await redis.set(f"generation:{request_id}", request_data)
            
            # Mark as complete in queue service (even if failed)
            queue_service = QueueService(redis)
            await queue_service.mark_complete(request_id)
    except Exception as e:
        logger.error(f"Error marking request as failed: {e}", exc_info=True)
    finally:
        await redis.disconnect()
