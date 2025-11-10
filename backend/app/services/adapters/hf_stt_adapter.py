# backend/app/services/adapters/hf_stt_adapter.py
# =================================================================
#
#              Hugging Face Speech-to-Text (STT) Adapter
#
# =================================================================
#
#  Purpose:
#  --------
#  Concrete implementation of the BaseSTTAdapter for Hugging Face
#  models, specifically targeting Whisper.
#
#  Key Features:
#  -------------
#  - Initializes a Hugging Face automatic-speech-recognition pipeline.
#  - Implements `transcribe_audio` to convert audio to text.
#  - Runs the synchronous pipeline in a thread for async safety.
#
# =================================================================

import asyncio
import base64
from io import BytesIO

from app.core.config import settings
from app.services.base.stt_adapter import BaseSTTAdapter
from transformers import pipeline


class HuggingFaceSTTAdapter(BaseSTTAdapter):
    """Adapter for Hugging Face speech-recognition models."""

    def __init__(self, model_name: str = "openai/whisper-tiny"):
        self.pipeline = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            token=settings.HF_API_TOKEN,
        )

    async def transcribe_audio(self, audio_base64: str) -> str:
        """
        Transcribes audio from a base64-encoded string.

        Args:
            audio_base64: The base64-encoded audio data.

        Returns:
            The transcribed text.
        """
        try:
            audio_bytes = base64.b64decode(audio_base64)
            audio_file = BytesIO(audio_bytes)

            # Run the synchronous pipeline in a separate thread
            result = await asyncio.to_thread(self.pipeline, audio_file)
            return result["text"]
        except Exception as e:
            print(f"Error transcribing audio with HuggingFace: {e}")
            return ""
