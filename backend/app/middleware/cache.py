from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import hashlib
import json

class CacheMiddleware(BaseHTTPMiddleware):
    """
    Response caching middleware
    """

    def __init__(self, app, cacheable_paths: list):
        super().__init__(app)
        self.cacheable_paths = cacheable_paths

    async def dispatch(self, request: Request, call_next):
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)

        # Check if path is cacheable
        is_cacheable = any(
            request.url.path.startswith(path)
            for path in self.cacheable_paths
        )

        if not is_cacheable:
            return await call_next(request)

        # Generate cache key
        cache_key = self._generate_cache_key(request)

        try:
            redis = request.app.state.redis

            # Check cache
            cached = await redis.get(cache_key)
            if cached:
                return Response(
                    content=json.dumps(cached),
                    media_type="application/json",
                    headers={"X-Cache": "HIT"}
                )

            # Process request
            response = await call_next(request)

            # Cache successful responses
            if response.status_code == 200:
                # Read response body
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk

                # Cache it
                try:
                    data = json.loads(body)
                    await redis.set(cache_key, data, ttl=300)  # 5 minutes
                except:
                    pass

                # Return response
                return Response(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )

            return response

        except Exception as e:
            print(f"Cache error: {e}")
            return await call_next(request)

    def _generate_cache_key(self, request: Request) -> str:
        """Generate cache key from request"""
        key_parts = [
            request.url.path,
            str(request.url.query)
        ]
        key_string = "|".join(key_parts)
        return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"
