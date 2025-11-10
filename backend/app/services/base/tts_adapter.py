# backend/app/services/base/tts_adapter.py
# =================================================================
#
#                   Text-to-Speech (TTS) Adapter Base Class
#
# =================================================================
#
#  Purpose:
#  --------
#  Defines the abstract base class for all Text-to-Speech (TTS)
#  adapters. This provides a consistent interface for converting
#  text into audio data.
#
#  Key Methods:
#  ------------
#  - generate_audio: An asynchronous method that takes a text string
#    and returns a base64-encoded audio string.
#
# =================================================================

from abc import ABC, abstractmethod


class BaseTTSAdapter(ABC):
    """Abstract base class for Text-to-Speech (TTS) adapters."""

    @abstractmethod
    async def generate_audio(self, text: str) -> str:
        """
        Generates audio from a text string.

        Args:
            text: The input text to be converted to speech.

        Returns:
            A base64-encoded string representing the generated audio.
        """
        pass
