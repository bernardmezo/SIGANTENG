# backend/app/tasks.py
# =================================================================
#
#                       Celery Background Tasks
#
# =================================================================
#
#  Purpose:
#  --------
#  Defines the background tasks that are executed by Celery workers.
#  These tasks are designed for long-running or heavy computations
#  that should not block the main application thread.
#
#  Key Tasks:
#  ----------
#  - long_llm_generation_task: A task for generating text from an LLM,
#    which can be time-consuming. It stores the result in Redis.
#
# =================================================================

import asyncio

import redis
from app.core.celery_app import celery_app
from app.core.config import settings
from app.services.llm_service import LLMService

# Initialize a Redis client for caching results
redis_client = redis.from_url(settings.REDIS_URL)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def long_llm_generation_task(self, prompt: str):
    """
    Celery task to generate a response from an LLM in the background.
    The result is stored in Redis with the task ID as the key.
    """
    try:
        # Service instantiation within the task ensures it runs in the worker's process.
        # It now uses the default provider from the settings file.
        llm_service = LLMService()

        # Run the async service method within the synchronous Celery task.
        response = asyncio.run(llm_service.generate_response(prompt))

        # Store the result in Redis, expiring after 10 minutes
        redis_client.set(self.request.id, response, ex=600)

        return {"status": "SUCCESS", "result": response}
    except Exception as e:
        # Log the exception and retry the task if applicable
        print(f"Task {self.request.id} failed: {e}")
        raise self.retry(exc=e)


# Placeholder for the embeddings task
@celery_app.task(bind=True)
def generate_embeddings_and_upsert_task(self, content_id: str, text: str):
    # This task will be implemented more fully later.
    # 1. Create embedding from text.
    # 2. Upsert vector to Pinecone using vector_db_service.
    print(f"Processing content_id: {content_id}")
    return {"status": "PENDING", "message": "Not yet implemented."}
