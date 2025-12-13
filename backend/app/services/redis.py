import redis.asyncio as aioredis
from redis.asyncio import Redis
from typing import Optional, Any
import json
import logging
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class RedisService:
    def __init__(self):
        self.redis: Optional[Redis] = None
        self.connection_pool: Optional[aioredis.ConnectionPool] = None

    async def connect(self):
        """Initialize Redis connection pool"""
        try:
            self.connection_pool = aioredis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                decode_responses=True
            )
            self.redis = aioredis.Redis(connection_pool=self.connection_pool)
            # Test connection
            await self.redis.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            await self.connection_pool.disconnect()
            logger.info("Redis connection closed")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in Redis with optional TTL"""
        try:
            serialized = json.dumps(value)
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)
            return True
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return await self.redis.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis EXISTS error for key {key}: {e}")
            return False

    async def increment(self, key: str) -> int:
        """Increment counter"""
        try:
            return await self.redis.incr(key)
        except Exception as e:
            logger.error(f"Redis INCR error for key {key}: {e}")
            return 0

    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration on key"""
        try:
            return await self.redis.expire(key, ttl)
        except Exception as e:
            logger.error(f"Redis EXPIRE error for key {key}: {e}")
            return False

    # Queue operations
    async def lpush(self, key: str, value: Any) -> int:
        """Push to left of list"""
        try:
            # If value is already a string, use it directly
            if isinstance(value, str):
                serialized = value
            else:
                serialized = json.dumps(value)
            return await self.redis.lpush(key, serialized)
        except Exception as e:
            logger.error(f"Redis LPUSH error for key {key}: {e}")
            return 0

    async def rpop(self, key: str) -> Optional[Any]:
        """Pop from right of list"""
        try:
            value = await self.redis.rpop(key)
            if value:
                # Try to parse as JSON, if fails return as string
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return None
        except Exception as e:
            logger.error(f"Redis RPOP error for key {key}: {e}")
            return None
    
    async def lindex(self, key: str, index: int) -> Optional[Any]:
        """Get element at index in list"""
        try:
            value = await self.redis.lindex(key, index)
            if value:
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return None
        except Exception as e:
            logger.error(f"Redis LINDEX error for key {key}: {e}")
            return None

    async def llen(self, key: str) -> int:
        """Get list length"""
        try:
            return await self.redis.llen(key)
        except Exception as e:
            logger.error(f"Redis LLEN error for key {key}: {e}")
            return 0

    # Set operations
    async def sadd(self, key: str, *values: Any) -> int:
        """Add to set"""
        try:
            serialized = [json.dumps(v) for v in values]
            return await self.redis.sadd(key, *serialized)
        except Exception as e:
            logger.error(f"Redis SADD error for key {key}: {e}")
            return 0

    async def srem(self, key: str, *values: Any) -> int:
        """Remove from set"""
        try:
            serialized = [json.dumps(v) for v in values]
            return await self.redis.srem(key, *serialized)
        except Exception as e:
            logger.error(f"Redis SREM error for key {key}: {e}")
            return 0

    async def scard(self, key: str) -> int:
        """Get set cardinality"""
        try:
            return await self.redis.scard(key)
        except Exception as e:
            logger.error(f"Redis SCARD error for key {key}: {e}")
            return 0

    async def smembers(self, key: str) -> set:
        """Get all set members"""
        try:
            members = await self.redis.smembers(key)
            return {json.loads(m) for m in members}
        except Exception as e:
            logger.error(f"Redis SMEMBERS error for key {key}: {e}")
            return set()

# Dependency for FastAPI
async def get_redis_service() -> RedisService:
    """Dependency to get Redis service from app state"""
    from fastapi import Request
    # This will be injected by FastAPI
    pass
