# backend/app/services/stt_service.py
# =================================================================
#
#                   Speech-to-Text (STT) Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service acts as a factory and proxy for STT model operations.
#  It uses an adapter-based design to abstract the specifics of the
#  STT provider (e.g., OpenAI, Hugging Face).
#
#  Key Features:
#  -------------
#  - Dynamically selects the STT adapter based on configuration.
#  - Provides a single entry point (`transcribe_audio`) for the app.
#
# =================================================================

from app.core.config import settings
from app.services.adapters.hf_stt_adapter import HuggingFaceSTTAdapter
from app.services.adapters.openai_stt_adapter import OpenAISTTAdapter  # Updated name
from app.services.base.stt_adapter import BaseSTTAdapter


class STTService:
    """
    Service to perform Speech-to-Text transcription.
    It uses a specific adapter based on the configuration.
    """

    def __init__(self, provider: str | None = None):
        """
        Initializes the service.

        Args:
            provider: The specific provider to use. If None, defaults
                      to the one specified in the global settings.
        """
        final_provider = provider or settings.DEFAULT_STT_PROVIDER
        self.adapter: BaseSTTAdapter = self._get_adapter(final_provider)

    def _get_adapter(self, provider: str) -> BaseSTTAdapter:
        """Factory method to get the appropriate STT adapter."""
        if provider == "openai" and settings.OPENAI_API_KEY:
            return OpenAISTTAdapter()  # Updated name
        elif provider == "huggingface" and settings.HF_API_TOKEN:
            return HuggingFaceSTTAdapter()
        else:
            # Fallback logic
            if settings.OPENAI_API_KEY:
                print(
                    f"Warning: STT provider '{provider}' not available, falling back to 'openai'."
                )
                return OpenAISTTAdapter()  # Updated name
            if settings.HF_API_TOKEN:
                print(
                    f"Warning: STT provider '{provider}' not available, falling back to 'huggingface'."
                )
                return HuggingFaceSTTAdapter()
            raise ValueError("No valid STT provider is configured.")

    async def transcribe_audio(self, audio_base64: str) -> str:
        """
        Transcribes audio using the selected STT adapter.

        Args:
            audio_base64: The base64-encoded audio data.

        Returns:
            The transcribed text.
        """
        return await self.adapter.transcribe_audio(audio_base64)
