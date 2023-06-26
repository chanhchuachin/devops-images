from celery import Celery
from src.core.config import settings

celery = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

celery.autodiscover_tasks(["src.api.background_removal"])
