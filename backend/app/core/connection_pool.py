"""
Connection pooling for external APIs
"""
import httpx
from app.core.config import get_settings

settings = get_settings()

# Global HTTP client with connection pooling
http_client = None

def get_http_client() -> httpx.AsyncClient:
    """Get or create HTTP client with connection pooling"""
    global http_client
    if http_client is None:
        limits = httpx.Limits(
            max_keepalive_connections=20,
            max_connections=100,
            keepalive_expiry=30
        )
        http_client = httpx.AsyncClient(
            limits=limits,
            timeout=httpx.Timeout(settings.FAL_API_TIMEOUT)
        )
    return http_client

async def close_http_client():
    """Close HTTP client"""
    global http_client
    if http_client:
        await http_client.aclose()
        http_client = None
