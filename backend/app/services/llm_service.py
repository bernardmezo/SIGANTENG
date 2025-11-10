# backend/app/services/llm_service.py
# =================================================================
#
#                       LLM Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service acts as a factory and proxy for Large Language Model
#  (LLM) operations. It uses an adapter-based design to abstract the
#  specifics of the LLM provider (e.g., OpenAI, Hugging Face).
#
#  Key Features:
#  -------------
#  - Dynamically selects the LLM adapter based on configuration.
#  - Provides a single entry point (`generate_response`) for the app.
#
# =================================================================

from app.services.base.llm_adapter import BaseLLMAdapter
from app.services.model_registry import get_model_registry


class LLMService:
    """
    Service to interact with a Large Language Model.
    It uses a specific adapter based on the configuration retrieved from the ModelRegistry.
    """

    def __init__(self, provider: str | None = None):
        """
        Initializes the service.

        Args:
            provider: The specific provider to use. If None, defaults
                      to the one specified in the global settings.
        """
        model_registry = get_model_registry()
        self.adapter: BaseLLMAdapter = model_registry.get_llm_adapter(provider)

    async def generate_response(self, prompt: str) -> str:
        """
        Generates a response using the selected LLM adapter.

        Args:
            prompt: The input text to send to the LLM.

        Returns:
            The text response from the LLM.
        """
        return await self.adapter.generate_response(prompt)
