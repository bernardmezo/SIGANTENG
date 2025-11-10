# backend/app/services/adapters/openai_stt_adapter.py
# =================================================================
#
#              OpenAI Speech-to-Text (STT) Adapter
#
# =================================================================
#
#  Purpose:
#  --------
#  Concrete implementation of the BaseSTTAdapter for OpenAI's
#  Whisper model via their API.
#
#  Key Features:
#  -------------
#  - Uses `openai.AsyncOpenAI` for non-blocking API requests.
#  - Implements `transcribe_audio` by sending audio data to the
#    transcriptions endpoint.
#
# =================================================================

import base64
from io import BytesIO

from app.core.config import settings
from app.services.base.stt_adapter import BaseSTTAdapter
from openai import AsyncOpenAI


class OpenAISTTAdapter(BaseSTTAdapter):  # Renamed class
    """Adapter for OpenAI's Whisper STT model."""

    def __init__(self, model_name: str = "whisper-1"):
        self.model_name = model_name
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe_audio(self, audio_base64: str) -> str:
        """
        Transcribes audio from a base64-encoded string using OpenAI.

        Args:
            audio_base64: The base64-encoded audio data.

        Returns:
            The transcribed text.
        """
        try:
            audio_bytes = base64.b64decode(audio_base64)
            audio_file = BytesIO(audio_bytes)
            audio_file.name = "input.wav"  # API requires a file name

            response = await self.client.audio.transcriptions.create(
                model=self.model_name,
                file=audio_file,
            )
            return response.text
        except Exception as e:
            print(f"Error transcribing audio with OpenAI: {e}")
            return ""
