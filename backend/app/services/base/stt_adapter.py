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
        Transcribes a single audio input.
        """
        pass

    async def transcribe_audios_batch(self, audios_base64: list[str]) -> list[str]:
        """
        Transcribes a batch of audio inputs.

        NOTE: This is a non-optimized default implementation.
        Subclasses should override this method to leverage true batch
        inference capabilities of the underlying model if available.
        """
        return [await self.transcribe_audio(audio) for audio in audios_base64]
