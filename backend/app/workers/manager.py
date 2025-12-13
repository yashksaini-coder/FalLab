import asyncio
from app.services.redis import RedisService
from app.services.queue_service import QueueService
from app.workers.tasks import process_generation
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class WorkerManager:
    """
    Manages worker pool and task distribution
    """

    def __init__(self):
        self.redis = None
        self.queue_service = None
        self.running = False

    async def start(self):
        """Start worker manager"""
        self.redis = RedisService()
        await self.redis.connect()
        self.queue_service = QueueService(self.redis)
        self.running = True

        logger.info("Worker manager started")

        # Start processing loop in background
        asyncio.create_task(self.process_queue())

    async def stop(self):
        """Stop worker manager"""
        self.running = False
        if self.redis:
            await self.redis.disconnect()
        logger.info("Worker manager stopped")

    async def process_queue(self):
        """
        Main processing loop

        Continuously checks queue and dispatches tasks to Celery workers
        """
        while self.running:
            try:
                # Try to dequeue next request
                request_id = await self.queue_service.dequeue()

                if request_id:
                    # Dispatch to Celery worker
                    logger.info(f"Dispatching {request_id} to Celery worker")
                    process_generation.apply_async(
                        args=[request_id],
                        countdown=0
                    )

                    # Wait a bit before checking again
                    await asyncio.sleep(1)
                else:
                    # No capacity or empty queue, wait longer
                    await asyncio.sleep(5)

            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                await asyncio.sleep(5)

# Global worker manager instance
worker_manager = None

async def start_worker_manager():
    """Start the worker manager"""
    global worker_manager
    worker_manager = WorkerManager()
    await worker_manager.start()

async def stop_worker_manager():
    """Stop the worker manager"""
    global worker_manager
    if worker_manager:
        await worker_manager.stop()
