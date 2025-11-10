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

from app.core.config import settings
from app.services.adapters.hf_llm_adapter import HuggingFaceLLMAdapter
from app.services.adapters.openai_llm_adapter import OpenAILLMAdapter
from app.services.base.llm_adapter import BaseLLMAdapter


class LLMService:
    """
    Service to interact with a Large Language Model.
    It uses a specific adapter based on the configuration.
    """

    def __init__(self, provider: str | None = None):
        """
        Initializes the service.

        Args:
            provider: The specific provider to use. If None, defaults
                      to the one specified in the global settings.
        """
        final_provider = provider or settings.DEFAULT_LLM_PROVIDER
        self.adapter: BaseLLMAdapter = self._get_adapter(final_provider)

    def _get_adapter(self, provider: str) -> BaseLLMAdapter:
        """Factory method to get the appropriate LLM adapter."""
        if provider == "openai" and settings.OPENAI_API_KEY:
            return OpenAILLMAdapter()
        elif provider == "huggingface" and settings.HF_API_TOKEN:
            return HuggingFaceLLMAdapter()
        else:
            # Fallback logic
            if settings.OPENAI_API_KEY:
                print(
                    f"Warning: LLM provider '{provider}' not available, falling back to 'openai'."
                )
                return OpenAILLMAdapter()
            if settings.HF_API_TOKEN:
                print(
                    f"Warning: LLM provider '{provider}' not available, falling back to 'huggingface'."
                )
                return HuggingFaceLLMAdapter()
            raise ValueError("No valid LLM provider is configured.")

    async def generate_response(self, prompt: str) -> str:
        """
        Generates a response using the selected LLM adapter.

        Args:
            prompt: The input text to send to the LLM.

        Returns:
            The text response from the LLM.
        """
        return await self.adapter.generate_response(prompt)
