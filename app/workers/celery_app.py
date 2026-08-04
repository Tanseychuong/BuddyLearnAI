from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "buddylearn",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    # A single failed extraction/embedding shouldn't loop forever.
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)