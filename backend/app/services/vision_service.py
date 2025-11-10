# backend/app/services/vision_service.py
# =================================================================
#
#                       Vision Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service acts as a factory and proxy for computer vision
#  model operations. It uses an adapter-based design to abstract
#  the specifics of the vision provider (e.g., OpenAI, Hugging Face).
#
#  Key Features:
#  -------------
#  - Dynamically selects the vision adapter based on configuration.
#  - Provides a single entry point (`get_image_description`) for the app.
#
# =================================================================

import hashlib
import logging

import redis
from app.core.config import settings
from app.services.base.vision_adapter import BaseVisionAdapter
from app.services.model_registry import get_model_registry

logger = logging.getLogger(__name__)


class VisionService:
    """
    Service to interact with a computer vision model, with a Redis-based
    caching layer to optimize repeated requests.
    """

    def __init__(self, provider: str | None = None):
        """
        Initializes the service and the Redis client for caching.
        """
        model_registry = get_model_registry()
        self.adapter: BaseVisionAdapter = model_registry.get_vision_adapter(provider)
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
            logger.info("VisionService connected to Redis for caching.")
        except redis.exceptions.ConnectionError:
            logger.warning(
                "Could not connect to Redis for VisionService caching. Caching will be disabled."
            )
            self.redis_client = None

    def _get_image_hash(self, image_base64: str) -> str:
        """Computes a SHA256 hash of the base64 image string."""
        return hashlib.sha256(image_base64.encode()).hexdigest()

    async def get_image_description(self, image_base64: str) -> str:
        """
        Generates a description for an image, utilizing a cache to avoid
        re-processing identical images.
        """
        if not self.redis_client:
            # Fallback to direct call if Redis is not available
            return await self.adapter.get_image_description(image_base64)

        image_hash = self._get_image_hash(image_base64)
        cache_key = f"cache:vision:{image_hash}"

        # 1. Check cache first
        try:
            cached_description = self.redis_client.get(cache_key)
            if cached_description:
                logger.info(f"Cache hit for image hash: {image_hash}")
                return cached_description
        except redis.exceptions.RedisError as e:
            logger.error(f"Redis GET error: {e}. Bypassing cache.")

        logger.info(f"Cache miss for image hash: {image_hash}. Calling adapter.")

        # 2. If miss, call the adapter
        description = await self.adapter.get_image_description(image_base64)

        # 3. Store the new result in cache
        if description:
            try:
                # Cache result for 24 hours
                self.redis_client.set(cache_key, description, ex=86400)
            except redis.exceptions.RedisError as e:
                logger.error(f"Redis SET error: {e}. Failed to cache result.")

        return description
