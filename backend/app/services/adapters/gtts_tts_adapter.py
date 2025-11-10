# backend/app/services/adapters/gtts_tts_adapter.py
# =================================================================
#
#                 gTTS Text-to-Speech (TTS) Adapter
#
# =================================================================
#
#  Purpose:
#  --------
#  Concrete implementation of the BaseTTSAdapter using Google's
#  Text-to-Speech library (gTTS).
#
#  Key Features:
#  -------------
#  - Uses the `gtts` library to generate speech.
#  - Implements `generate_audio` to convert text to a base64-encoded
#    audio string.
#  - Runs the synchronous gTTS operations in a thread for async safety.
#
# =================================================================

import asyncio
import base64
from io import BytesIO

from app.services.base.tts_adapter import BaseTTSAdapter
from gtts import gTTS


class GTTSTransformer(BaseTTSAdapter):
    """Adapter for Google Text-to-Speech (gTTS)."""

    async def generate_audio(self, text: str) -> str:
        """
        Generates audio from text using gTTS.

        Args:
            text: The text to convert to speech.

        Returns:
            A base64-encoded string of the generated audio.
        """
        try:

            def _generate():
                tts = gTTS(text=text, lang="en")
                audio_buffer = BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                return audio_buffer.read()

            # Run the synchronous gTTS code in a separate thread
            audio_bytes = await asyncio.to_thread(_generate)

            # Encode audio to base64
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            return audio_base64
        except Exception as e:
            print(f"Error generating audio with gTTS: {e}")
            return ""
