# backend/app/services/base/stt_adapter.py
# =================================================================
#
#                   Speech-to-Text (STT) Adapter Base Class
#
# =================================================================
#
#  Purpose:
#  --------
#  Defines the abstract base class for all Speech-to-Text (STT)
#  adapters. This provides a consistent interface for converting
#  audio data into text.
#
#  Key Methods:
#  ------------
#  - transcribe_audio: An asynchronous method that takes a
#    base64-encoded audio string and returns the transcribed text.
#
# =================================================================

from abc import ABC, abstractmethod


class BaseSTTAdapter(ABC):
    """Abstract base class for Speech-to-Text (STT) adapters."""

    @abstractmethod
    async def transcribe_audio(self, audio_base64: str) -> str:
        """
        Transcribes audio from a base64-encoded string into text.

        Args:
            audio_base64: The base64-encoded string of the audio data.

        Returns:
            The transcribed text.
        """
        pass
