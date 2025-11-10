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
        Generates audio for a single text input.
        """
        pass

    async def generate_audios_batch(self, texts: list[str]) -> list[str]:
        """
        Generates audio for a batch of text inputs.

        NOTE: This is a non-optimized default implementation.
        Subclasses should override this method to leverage true batch
        inference capabilities of the underlying model if available.
        """
        return [await self.generate_audio(text) for text in texts]
