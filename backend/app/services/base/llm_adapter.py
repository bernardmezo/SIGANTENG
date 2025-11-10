# backend/app/services/base/llm_adapter.py
# =================================================================
#
#                       LLM Adapter Base Class
#
# =================================================================
#
#  Purpose:
#  --------
#  Defines the abstract base class for all Large Language Model (LLM)
#  adapters. This ensures that any concrete LLM adapter implementation
#  (e.g., for OpenAI, HuggingFace, etc.) adheres to a consistent
#  interface for generating text responses.
#
#  Key Methods:
#  ------------
#  - generate_response: An asynchronous method that takes a text prompt
#    and returns a string response from the LLM.
#
# =================================================================

from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):
    """Abstract base class for LLM adapters."""

    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        """
        Generates a response from the LLM based on the given prompt.
        """
        pass

    async def generate_responses_batch(self, prompts: list[str]) -> list[str]:
        """
        Generates responses for a batch of prompts.

        NOTE: This is a non-optimized default implementation.
        Subclasses should override this method to leverage true batch
        inference capabilities of the underlying model if available.
        """
        # This is a simple, sequential implementation.
        # A slightly better default could use asyncio.gather for concurrency.
        return [await self.generate_response(prompt) for prompt in prompts]
