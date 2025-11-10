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

from app.core.config import settings
from app.services.adapters.gtts_tts_adapter import GTTSTransformer
from app.services.adapters.openai_tts_adapter import OpenAITTSAdapter
from app.services.base.tts_adapter import BaseTTSAdapter


class TTSService:
    """
    Service to perform Text-to-Speech conversion.
    It uses a specific adapter based on the configuration.
    """

    def __init__(self, provider: str | None = None):
        """
        Initializes the service.

        Args:
            provider: The specific provider to use. If None, defaults
                      to the one specified in the global settings.
        """
        final_provider = provider or settings.DEFAULT_TTS_PROVIDER
        self.adapter: BaseTTSAdapter = self._get_adapter(final_provider)

    def _get_adapter(self, provider: str) -> BaseTTSAdapter:
        """Factory method to get the appropriate TTS adapter."""
        if provider == "openai" and settings.OPENAI_API_KEY:
            return OpenAITTSAdapter()
        elif provider == "gtts":
            return GTTSTransformer()
        else:
            # Default to gTTS as it has no key requirements
            print(
                f"Warning: TTS provider '{provider}' not available, falling back to 'gtts'."
            )
            return GTTSTransformer()

    async def generate_audio(self, text: str) -> str:
        """
        Generates audio from text using the selected TTS adapter.

        Args:
            text: The text to convert to speech.

        Returns:
            A base64-encoded string of the generated audio.
        """
        return await self.adapter.generate_audio(text)
