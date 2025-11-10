# backend/tests/adapters/test_openai_stt_adapter.py
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.services.adapters.openai_stt_adapter import OpenAISTTAdapter


@pytest.mark.asyncio
@patch("app.services.adapters.openai_stt_adapter.AsyncOpenAI")
async def test_transcribe_audio_success(MockAsyncOpenAI):
    # Arrange
    mock_client = MockAsyncOpenAI.return_value
    mock_transcription = MagicMock()
    mock_transcription.text = "This is a test transcription."

    mock_client.audio.transcriptions.create = AsyncMock(return_value=mock_transcription)

    adapter = OpenAISTTAdapter()
    # A minimal valid wav file in base64
    test_audio_base64 = (
        "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAAABkYXRhAAAAAA=="
    )

    # Act
    result = await adapter.transcribe_audio(test_audio_base64)

    # Assert
    assert result == "This is a test transcription."
    mock_client.audio.transcriptions.create.assert_awaited_once()


@pytest.mark.asyncio
@patch("app.services.adapters.openai_stt_adapter.AsyncOpenAI")
async def test_transcribe_audio_failure(MockAsyncOpenAI):
    # Arrange
    mock_client = MockAsyncOpenAI.return_value
    mock_client.audio.transcriptions.create = AsyncMock(
        side_effect=Exception("API Error")
    )

    adapter = OpenAISTTAdapter()
    # Use a valid base64 string so the decoding doesn't fail first
    test_audio_base64 = (
        "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAAABkYXRhAAAAAA=="
    )

    # Act
    result = await adapter.transcribe_audio(test_audio_base64)

    # Assert
    assert result == ""
    mock_client.audio.transcriptions.create.assert_awaited_once()
