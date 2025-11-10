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
# =================================================================

import json
import logging

import redis
from app.core.celery_app import celery_app
from app.core.config import settings
from app.services.langchain_orchestrator import LangChainOrchestrator
from app.services.llm_service import LLMService
from app.services.multimodal_pipeline import MultimodalPipeline
from app.services.tts_service import TTSService
from app.services.vision_service import VisionService

# Get logger for tasks
logger = logging.getLogger("celery.task")

# Initialize a Redis client for caching results
# Note: In a large-scale app, you might manage this client connection
# more carefully, e.g., using Celery signals.
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
    task_time_limit=300,
)
async def long_llm_generation_task(self, prompt: str, user_id: str = None):
    """
    Celery task to generate a response from an LLM in the background.
    The result is stored in Redis with the task ID as the key.
    This task is now fully asynchronous.
    """
    task_id = self.request.id
    logger.info(f"Starting async LLM generation task. Task ID: {task_id}")

    try:
        # In a real-world scenario, service instantiation should also be optimized.
        # For now, we instantiate it here for simplicity.
        llm_service = LLMService()
        response = await llm_service.generate_response(prompt)

        redis_client.set(task_id, response, ex=600)
        logger.info(f"Async LLM generation task completed. Task ID: {task_id}")

        return {"status": "SUCCESS", "result": response}
    except Exception as e:
        logger.error(
            f"Async LLM generation task failed. Task ID: {task_id}, Error: {e}",
            exc_info=True,
        )
        # The 'autoretry_for' will handle the retry logic.
        raise


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
    task_time_limit=600,  # Longer timeout for multi-step pipeline
)
async def multimodal_pipeline_task(self, image_base64: str, user_id: str = None):
    """
    Celery task to run the full image-to-speech pipeline in the background.
    The dictionary result is stored as a JSON string in Redis.
    """
    task_id = self.request.id
    logger.info(f"Starting async multimodal pipeline task. Task ID: {task_id}")

    try:
        # Instantiate the pipeline and its dependencies.
        # This could be optimized with a singleton pattern for workers.
        pipeline = MultimodalPipeline(
            vision_service=VisionService(),
            langchain_orchestrator=LangChainOrchestrator(),
            tts_service=TTSService(),
        )
        result_dict = await pipeline.process_image(image_base64)

        # Serialize dictionary to JSON string for Redis storage
        result_json = json.dumps(result_dict)
        redis_client.set(task_id, result_json, ex=1200)
        logger.info(f"Async multimodal pipeline task completed. Task ID: {task_id}")

        return {"status": "SUCCESS", "result": result_dict}
    except Exception as e:
        logger.error(
            f"Async multimodal pipeline task failed. Task ID: {task_id}, Error: {e}",
            exc_info=True,
        )
        raise


# Placeholder for the embeddings task
@celery_app.task(bind=True)
def generate_embeddings_and_upsert_task(
    self, content_id: str, text: str, user_id: str = None
):
    task_id = self.request.id
    logger.info(
        f"Processing embeddings task. Task ID: {task_id}, Content ID: {content_id}"
    )
    # This task will be implemented more fully later.
    # 1. Create embedding from text.
    # 2. Upsert vector to Pinecone using vector_db_service.
    return {"status": "PENDING", "message": "Not yet implemented."}
