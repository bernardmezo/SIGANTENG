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

from app.services.base.stt_adapter import BaseSTTAdapter
from app.services.model_registry import get_model_registry


class STTService:
    """
    Service to perform Speech-to-Text transcription.
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
        self.adapter: BaseSTTAdapter = model_registry.get_stt_adapter(provider)

    async def transcribe_audio(self, audio_base64: str) -> str:
        """
        Transcribes audio using the selected STT adapter.

        Args:
            audio_base64: The base64-encoded audio data.

        Returns:
            The transcribed text.
        """
        return await self.adapter.transcribe_audio(audio_base64)
