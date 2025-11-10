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

import json

import redis
from app.core.config import settings
from app.tasks import long_llm_generation_task, multimodal_pipeline_task
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
        """
        task = long_llm_generation_task.delay(prompt)
        return task.id

    def submit_multimodal_pipeline(self, image_base64: str) -> str:
        """
        Submits a multimodal pipeline task to the background worker.
        """
        task = multimodal_pipeline_task.delay(image_base64)
        return task.id

    def get_task_status_and_result(self, task_id: str) -> dict:
        """
        Checks the status of a Celery task and retrieves its result if available.
        It handles both plain text and JSON string results from Redis.
        """
        # Check for cached result in Redis first
        cached_result = self.redis_client.get(task_id)
        if cached_result:
            try:
                # Try to parse as JSON for multimodal task results
                result_data = json.loads(cached_result)
                return {"task_id": task_id, "status": "SUCCESS", "result": result_data}
            except json.JSONDecodeError:
                # Fallback for plain text results
                return {
                    "task_id": task_id,
                    "status": "SUCCESS",
                    "result": cached_result,
                }

        # If not in cache, check Celery backend
        task_result = AsyncResult(task_id)

        if not task_result.ready():
            return {"task_id": task_id, "status": "PENDING", "result": None}

        if task_result.successful():
            result = task_result.get().get("result")
            # The result from the task is already a dict or string,
            # so we serialize it for Redis if it's a dict.
            if isinstance(result, dict):
                redis_val = json.dumps(result)
            else:
                redis_val = result

            self.redis_client.set(task_id, redis_val, ex=1200)
            return {"task_id": task_id, "status": "SUCCESS", "result": result}
        else:
            return {
                "task_id": task_id,
                "status": "FAILURE",
                "result": str(task_result.info),
            }
