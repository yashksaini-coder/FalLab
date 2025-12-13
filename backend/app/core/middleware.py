"""
Custom middleware for the application
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.services.redis import RedisService
from app.core.config import get_settings
import time
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis
    Limits requests per minute per IP address
    """
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/health/live", "/health/ready", "/metrics", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        rate_limit_key = f"rate_limit:{client_ip}"
        
        try:
            redis: RedisService = request.app.state.redis
            
            # Check current count
            current_count = await redis.increment(rate_limit_key)
            
            # Set expiration on first request
            if current_count == 1:
                await redis.expire(rate_limit_key, 60)  # 60 seconds window
            
            # Check if limit exceeded
            if current_count > settings.RATE_LIMIT_PER_MINUTE:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return Response(
                    content='{"error": "Rate limit exceeded", "message": "Too many requests. Please try again later."}',
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    media_type="application/json",
                    headers={"Retry-After": "60"}
                )
            
            # Add rate limit headers
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
            response.headers["X-RateLimit-Remaining"] = str(max(0, settings.RATE_LIMIT_PER_MINUTE - current_count))
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
            
            return response
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            # On error, allow request but log it
            return await call_next(request)

