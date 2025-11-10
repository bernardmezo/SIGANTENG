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

import logging.config

from app.core.config import settings
from celery import Celery

# Define logging configuration
CELERY_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "celery_task": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - [Task: %(task_id)s] - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "celery_console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "celery_task",
        },
    },
    "loggers": {
        "celery": {
            "handlers": ["celery_console"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.task": {
            "handlers": ["celery_console"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {  # For general application logging
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_track_started=True,
    # Global time limits for tasks
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=360,  # 6 minutes (hard limit)
    # Basic dead-letter queue setup (requires broker support, e.g., RabbitMQ or specific Redis configurations)
    # For Redis, this often means relying on broker-level message expiry and custom error handling.
    # A more robust DLQ for Redis might involve a separate queue and a consumer.
    # For now, we'll rely on retries and logging.
    task_acks_late=True,  # Acknowledge task after it's done, not before
    task_reject_on_worker_timeout=True,  # Requeue task if worker times out
)

# Apply logging configuration
logging.config.dictConfig(CELERY_LOGGING_CONFIG)
