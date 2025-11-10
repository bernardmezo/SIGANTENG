# backend/app/services/model_registry.py
# =================================================================
#
#                       Unified Model Registry
#
# =================================================================
#
#  Purpose:
#  --------
#  This service acts as a central registry for all AI model adapters
#  (LLM, Vision, TTS, STT). It allows for dynamic selection, configuration,
#  and potential fallback mechanisms for different AI providers.
#
#  Key Features:
#  -------------
#  - Registers available adapters for each AI service type.
#  - Provides a method to retrieve an adapter instance based on type and provider.
#  - Supports setting a default provider for each service type.
#  - Implemented as a singleton using lru_cache for efficiency.
#
# =================================================================

from functools import lru_cache
from typing import Dict, Type

from app.core.config import settings
from app.services.adapters.gtts_tts_adapter import GTTSTTSAdapter
from app.services.adapters.hf_llm_adapter import HFLLMAdapter
from app.services.adapters.hf_stt_adapter import HFSTTAdapter
from app.services.adapters.hf_vision_adapter import HFVisionAdapter
from app.services.adapters.openai_llm_adapter import OpenAILLMAdapter
from app.services.adapters.openai_stt_adapter import OpenAISTTAdapter
from app.services.adapters.openai_tts_adapter import OpenAITTSAdapter
from app.services.adapters.openai_vision_adapter import OpenAIVisionAdapter
from app.services.base.llm_adapter import BaseLLMAdapter
from app.services.base.stt_adapter import BaseSTTAdapter
from app.services.base.tts_adapter import BaseTTSAdapter
from app.services.base.vision_adapter import BaseVisionAdapter


class ModelRegistry:
    """
    Central registry for managing AI model adapters.
    """

    def __init__(self):
        self._llm_adapters: Dict[str, Type[BaseLLMAdapter]] = {}
        self._vision_adapters: Dict[str, Type[BaseVisionAdapter]] = {}
        self._stt_adapters: Dict[str, Type[BaseSTTAdapter]] = {}
        self._tts_adapters: Dict[str, Type[BaseTTSAdapter]] = {}

        self._register_default_adapters()

    def _register_default_adapters(self):
        """Registers the default set of adapters."""
        self.register_llm_adapter("openai", OpenAILLMAdapter)
        self.register_llm_adapter("huggingface", HFLLMAdapter)

        self.register_vision_adapter("openai", OpenAIVisionAdapter)
        self.register_vision_adapter("huggingface", HFVisionAdapter)

        self.register_stt_adapter("openai", OpenAISTTAdapter)
        self.register_stt_adapter("huggingface", HFSTTAdapter)

        self.register_tts_adapter("openai", OpenAITTSAdapter)
        self.register_tts_adapter("gtts", GTTSTTSAdapter)

    def register_llm_adapter(self, name: str, adapter: Type[BaseLLMAdapter]):
        self._llm_adapters[name] = adapter

    def register_vision_adapter(self, name: str, adapter: Type[BaseVisionAdapter]):
        self._vision_adapters[name] = adapter

    def register_stt_adapter(self, name: str, adapter: Type[BaseSTTAdapter]):
        self._stt_adapters[name] = adapter

    def register_tts_adapter(self, name: str, adapter: Type[BaseTTSAdapter]):
        self._tts_adapters[name] = adapter

    def get_llm_adapter(self, provider: str = None) -> BaseLLMAdapter:
        provider = provider or settings.DEFAULT_LLM_PROVIDER
        adapter_class = self._llm_adapters.get(provider)
        if not adapter_class:
            raise ValueError(f"LLM adapter for provider '{provider}' not found.")
        return adapter_class()

    def get_vision_adapter(self, provider: str = None) -> BaseVisionAdapter:
        provider = provider or settings.DEFAULT_VISION_PROVIDER
        adapter_class = self._vision_adapters.get(provider)
        if not adapter_class:
            raise ValueError(f"Vision adapter for provider '{provider}' not found.")
        return adapter_class()

    def get_stt_adapter(self, provider: str = None) -> BaseSTTAdapter:
        provider = provider or settings.DEFAULT_STT_PROVIDER
        adapter_class = self._stt_adapters.get(provider)
        if not adapter_class:
            raise ValueError(f"STT adapter for provider '{provider}' not found.")
        return adapter_class()

    def get_tts_adapter(self, provider: str = None) -> BaseTTSAdapter:
        provider = provider or settings.DEFAULT_TTS_PROVIDER
        adapter_class = self._tts_adapters.get(provider)
        if not adapter_class:
            raise ValueError(f"TTS adapter for provider '{provider}' not found.")
        return adapter_class()


@lru_cache
def get_model_registry() -> ModelRegistry:
    """Singleton instance of the ModelRegistry."""
    return ModelRegistry()
