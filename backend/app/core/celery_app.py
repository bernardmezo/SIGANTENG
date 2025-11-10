# backend/app/core/celery_app.py
# =================================================================
#
#                       Celery Application Factory
#
# =================================================================
#
#  Purpose:
#  --------
#  This module initializes and configures the Celery application
#  instance. It connects Celery to the Redis broker defined in the
#  application's settings.
#
#  Key Features:
#  -------------
#  - Creates a Celery app instance.
#  - Configures the broker and result backend using the Redis URL
#    from the global settings.
#  - Autodiscovers tasks from the `app.tasks` module.
#
# =================================================================

from app.core.config import settings
from celery import Celery

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_track_started=True,
)
