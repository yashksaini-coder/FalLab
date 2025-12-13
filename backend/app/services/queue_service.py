from app.services.redis import RedisService
from app.core.config import get_settings
import asyncio
import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)
settings = get_settings()

class QueueService:
    """
    Manages request queuing and concurrent execution limits
    """

    def __init__(self, redis: RedisService):
        self.redis = redis
        self.queue_key = "generation_queue"
        self.active_key = "active_tasks"
        self.max_concurrent = settings.MAX_CONCURRENT_REQUESTS

    async def enqueue(self, request_id: str) -> int:
        """
        Add request to queue

        Returns queue position
        """
        await self.redis.lpush(self.queue_key, request_id)
        queue_length = await self.redis.llen(self.queue_key)
        logger.info(f"Request {request_id} added to queue. Queue length: {queue_length}")
        return queue_length

    async def dequeue(self) -> Optional[str]:
        """
        Get next request from queue if capacity available

        Returns request_id or None
        """
        # Check if we have capacity
        active_count = await self.redis.scard(self.active_key)

        if active_count >= self.max_concurrent:
            logger.debug(f"At capacity ({active_count}/{self.max_concurrent}). Not dequeuing.")
            return None

        # Pop from queue
        request_id = await self.redis.rpop(self.queue_key)

        if request_id:
            # Add to active set
            await self.redis.sadd(self.active_key, request_id)
            logger.info(f"Request {request_id} dequeued. Active: {active_count + 1}/{self.max_concurrent}")

        return request_id

    async def mark_complete(self, request_id: str):
        """
        Mark request as complete and remove from active set
        """
        await self.redis.srem(self.active_key, request_id)
        active_count = await self.redis.scard(self.active_key)
        logger.info(f"Request {request_id} completed. Active: {active_count}/{self.max_concurrent}")

    async def get_queue_position(self, request_id: str) -> Optional[int]:
        """
        Get position of request in queue (1-indexed)
        Returns None if not in queue
        """
        try:
            queue_length = await self.redis.llen(self.queue_key)

            for i in range(queue_length):
                item = await self.redis.lindex(self.queue_key, i)
                if item:
                    # Handle both string and dict responses
                    queued_id = item if isinstance(item, str) else item
                    if queued_id == request_id:
                        return queue_length - i

            return None
        except Exception as e:
            logger.error(f"Error getting queue position: {e}")
            return None

    async def get_metrics(self) -> dict:
        """Get current queue metrics"""
        return {
            "queued": await self.redis.llen(self.queue_key),
            "active": await self.redis.scard(self.active_key),
            "capacity": self.max_concurrent,
            "available_slots": self.max_concurrent - await self.redis.scard(self.active_key)
        }
