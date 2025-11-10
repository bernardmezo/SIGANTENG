# backend/app/services/adapters/openai_tts_adapter.py
# =================================================================
#
#                 OpenAI Text-to-Speech (TTS) Adapter
#
# =================================================================
#
#  Purpose:
#  --------
#  Concrete implementation of the BaseTTSAdapter for OpenAI's
#  Text-to-Speech models.
#
#  Key Features:
#  -------------
#  - Uses `openai.AsyncOpenAI` for non-blocking API requests.
#  - Implements `generate_audio` to convert text to speech.
#  - Returns a base64-encoded audio string.
#
# =================================================================

import base64

from app.core.config import settings
from app.services.base.tts_adapter import BaseTTSAdapter
from openai import AsyncOpenAI


class OpenAITTSAdapter(BaseTTSAdapter):
    """Adapter for OpenAI's Text-to-Speech models."""

    def __init__(self, model_name: str = "tts-1", voice: str = "alloy"):
        self.model_name = model_name
        self.voice = voice
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_audio(self, text: str) -> str:
        """
        Generates audio from text using OpenAI's TTS API.

        Args:
            text: The text to convert to speech.

        Returns:
            A base64-encoded string of the generated audio.
        """
        try:
            response = await self.client.audio.speech.create(
                model=self.model_name,
                voice=self.voice,
                input=text,
            )

            # The response body is a stream. We read it and encode to base64.
            audio_bytes = await response.aread()
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            return audio_base64
        except Exception as e:
            print(f"Error generating audio with OpenAI: {e}")
            return ""
