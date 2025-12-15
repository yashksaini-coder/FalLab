from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.redis import RedisService
from app.core.config import get_settings
import time

settings = get_settings()

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis
    """


    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path.startswith("/health") or request.url.path == "/":
            return await call_next(request)

        # Support custom user header for per-user rate limiting (for stress tests)
        user_id = request.headers.get("X-User-ID")
        if user_id:
            rate_key = f"user:{user_id}"
        else:
            # Fallback to client IP
            rate_key = f"ip:{request.client.host}"

        # Rate limit key (per minute)
        now = int(time.time() / 60)
        key = f"rate_limit:{rate_key}:{now}"

        try:
            redis: RedisService = request.app.state.redis

            # Increment counter
            count = await redis.increment(key)

            # Set expiry on first request
            if count == 1:
                await redis.expire(key, 60)

            # Check limit
            if count > settings.RATE_LIMIT_PER_MINUTE:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )

            # Add headers
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
            response.headers["X-RateLimit-Remaining"] = str(max(0, settings.RATE_LIMIT_PER_MINUTE - count))
            response.headers["X-RateLimit-Reset"] = str((now + 1) * 60)

            return response

        except HTTPException:
            raise
        except Exception as e:
            # Don't block requests if rate limiting fails
            print(f"Rate limiting error: {e}")
            return await call_next(request)
