#!/bin/bash

# Start Celery worker
celery -A app.workers.celery_app worker \
    --loglevel=info \
    --concurrency=5 \
    --max-tasks-per-child=50 \
    --task-events
