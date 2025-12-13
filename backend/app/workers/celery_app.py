from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "fal_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes
    task_soft_time_limit=540,  # 9 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    broker_connection_retry_on_startup=True,  # Fix deprecation warning
    include=["app.workers.tasks"],  # Explicitly include tasks module
)

# Import tasks to register them with Celery
from app.workers import tasks  # noqa: E402, F401
