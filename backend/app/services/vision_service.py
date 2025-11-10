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

from app.core.config import settings
from app.services.adapters.hf_vision_adapter import HuggingFaceVisionAdapter
from app.services.adapters.openai_vision_adapter import OpenAIVisionAdapter
from app.services.base.vision_adapter import BaseVisionAdapter


class VisionService:
    """
    Service to interact with a computer vision model.
    It uses a specific adapter based on the configuration.
    """

    def __init__(self, provider: str | None = None):
        """
        Initializes the service.

        Args:
            provider: The specific provider to use. If None, defaults
                      to the one specified in the global settings.
        """
        final_provider = provider or settings.DEFAULT_VISION_PROVIDER
        self.adapter: BaseVisionAdapter = self._get_adapter(final_provider)

    def _get_adapter(self, provider: str) -> BaseVisionAdapter:
        """Factory method to get the appropriate vision adapter."""
        if provider == "openai" and settings.OPENAI_API_KEY:
            return OpenAIVisionAdapter()
        elif provider == "huggingface" and settings.HF_API_TOKEN:
            return HuggingFaceVisionAdapter()
        else:
            # Fallback logic
            if settings.OPENAI_API_KEY:
                print(
                    f"Warning: Vision provider '{provider}' not available, falling back to 'openai'."
                )
                return OpenAIVisionAdapter()
            if settings.HF_API_TOKEN:
                print(
                    f"Warning: Vision provider '{provider}' not available, falling back to 'huggingface'."
                )
                return HuggingFaceVisionAdapter()
            raise ValueError("No valid vision provider is configured.")

    async def get_image_description(self, image_base64: str) -> str:
        """
        Generates a description for an image using the selected adapter.

        Args:
            image_base64: The base64-encoded image string.

        Returns:
            A textual description of the image.
        """
        return await self.adapter.get_image_description(image_base64)
