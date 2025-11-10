# backend/app/services/tts_service.py
# =================================================================
#
#                   Text-to-Speech (TTS) Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service acts as a factory and proxy for TTS model operations.
#  It uses an adapter-based design to abstract the specifics of the
#  TTS provider (e.g., OpenAI, gTTS).
#
#  Key Features:
#  -------------
#  - Dynamically selects the TTS adapter based on configuration.
#  - Provides a single entry point (`generate_audio`) for the app.
#
# =================================================================

from app.services.base.tts_adapter import BaseTTSAdapter
from app.services.model_registry import get_model_registry


class TTSService:
    """
    Service to perform Text-to-Speech conversion.
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
        self.adapter: BaseTTSAdapter = model_registry.get_tts_adapter(provider)

    async def generate_audio(self, text: str) -> str:
        """
        Generates audio from text using the selected TTS adapter.

        Args:
            text: The text to convert to speech.

        Returns:
            A base64-encoded string of the generated audio.
        """
        return await self.adapter.generate_audio(text)
