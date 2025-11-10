# backend/tests/adapters/test_openai_tts_adapter.py
import base64
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.services.adapters.openai_tts_adapter import OpenAITTSAdapter


@pytest.mark.asyncio
@patch("app.services.adapters.openai_tts_adapter.AsyncOpenAI")
async def test_openai_tts_generate_audio_success(MockAsyncOpenAI):
    # Arrange
    mock_response = AsyncMock()
    mock_response.aread.return_value = b"fake_openai_audio"

    mock_client = MockAsyncOpenAI.return_value
    mock_client.audio.speech.create = AsyncMock(return_value=mock_response)

    adapter = OpenAITTSAdapter(model_name="test-tts", voice="echo")

    # Act
    audio_base64 = await adapter.generate_audio("Hello from OpenAI")

    # Assert
    expected_base64 = base64.b64encode(b"fake_openai_audio").decode("utf-8")
    assert audio_base64 == expected_base64
    mock_client.audio.speech.create.assert_awaited_once_with(
        model="test-tts",
        voice="echo",
        input="Hello from OpenAI",
    )


@pytest.mark.asyncio
@patch("app.services.adapters.openai_tts_adapter.AsyncOpenAI")
async def test_openai_tts_generate_audio_failure(MockAsyncOpenAI):
    # Arrange
    mock_client = MockAsyncOpenAI.return_value
    mock_client.audio.speech.create = AsyncMock(side_effect=Exception("API error"))

    adapter = OpenAITTSAdapter()

    # Act
    audio_base64 = await adapter.generate_audio("Test text")

    # Assert
    assert audio_base64 == ""
