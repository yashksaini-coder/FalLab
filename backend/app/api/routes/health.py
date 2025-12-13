from fastapi import APIRouter, Depends, Request
from app.services.redis import RedisService
from app.services.queue_service import QueueService
from app.core.config import get_settings
import httpx

router = APIRouter()
settings = get_settings()

@router.get("/health")
async def health_check(request: Request):
    """
    Comprehensive health check endpoint
    """
    health_status = {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "checks": {}
    }

    # Check Redis
    try:
        redis: RedisService = request.app.state.redis
        await redis.redis.ping()
        health_status["checks"]["redis"] = "healthy"

        # Get queue metrics
        queue_service = QueueService(redis)
        metrics = await queue_service.get_metrics()
        health_status["checks"]["queue"] = metrics

    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"

    # Check Fal.ai API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.FAL_API_BASE_URL}/",
                timeout=5.0
            )
            health_status["checks"]["fal_api"] = "reachable" if response.status_code < 500 else "degraded"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["fal_api"] = f"unreachable: {str(e)}"

    return health_status

@router.get("/metrics")
async def get_metrics(request: Request):
    """Get detailed queue and system metrics"""
    from fastapi import HTTPException
    from datetime import datetime
    
    try:
        redis: RedisService = request.app.state.redis
        queue_service = QueueService(redis)

        metrics = await queue_service.get_metrics()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "queue": metrics,
            "system": {
                "max_concurrent": settings.MAX_CONCURRENT_REQUESTS,
                "rate_limit": settings.RATE_LIMIT_PER_MINUTE
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health/ready")
async def readiness_check(request: Request):
    """Kubernetes readiness probe"""
    try:
        redis: RedisService = request.app.state.redis
        await redis.redis.ping()
        return {"ready": True}
    except:
        return {"ready": False}, 503

@router.get("/health/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"alive": True}
