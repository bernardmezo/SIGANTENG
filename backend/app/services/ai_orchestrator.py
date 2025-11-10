# backend/app/services/ai_orchestrator.py
# =================================================================
#
#                       AI Orchestrator Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service is the central point for coordinating complex,
#  potentially long-running AI workflows that involve background tasks.
#
#  Key Features:
#  -------------
#  - Submits jobs to the Celery task queue.
#  - Provides methods to check the status and retrieve results of
#    background tasks.
#  - Interacts with the Redis cache for result storage.
#
# =================================================================

import redis
from app.core.config import settings
from app.tasks import long_llm_generation_task
from celery.result import AsyncResult


class AIOrchestratorService:
    """
    Service to orchestrate AI tasks, including submitting background jobs
    and retrieving their results.
    """

    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    def submit_long_llm_generation(self, prompt: str) -> str:
        """
        Submits a long LLM generation task to the background worker.

        Args:
            prompt: The prompt to send to the LLM.

        Returns:
            The ID of the submitted task.
        """
        task = long_llm_generation_task.delay(prompt)
        return task.id

    def get_task_status_and_result(self, task_id: str) -> dict:
        """
        Checks the status of a Celery task and retrieves its result if available.

        It first checks Redis for a cached result, then falls back to the
        Celery backend.

        Args:
            task_id: The ID of the task to check.

        Returns:
            A dictionary containing the task's status and result.
        """
        # Check for cached result in Redis first
        cached_result = self.redis_client.get(task_id)
        if cached_result:
            return {"task_id": task_id, "status": "SUCCESS", "result": cached_result}

        # If not in cache, check Celery backend
        task_result = AsyncResult(task_id)

        if task_result.ready():
            if task_result.successful():
                result = task_result.get()
                # Cache the final result
                self.redis_client.set(task_id, result.get("result"), ex=600)
                return {
                    "task_id": task_id,
                    "status": "SUCCESS",
                    "result": result.get("result"),
                }
            else:
                return {
                    "task_id": task_id,
                    "status": "FAILURE",
                    "result": str(task_result.info),
                }
        else:
            return {"task_id": task_id, "status": "PENDING"}
