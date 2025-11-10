# backend/tests/adapters/test_hf_stt_adapter.py
from unittest.mock import MagicMock, patch

import pytest
from app.services.adapters.hf_stt_adapter import HuggingFaceSTTAdapter


@pytest.mark.asyncio
@patch("app.services.adapters.hf_stt_adapter.pipeline")
async def test_hf_stt_transcribe_audio_success(mock_pipeline):
    # Arrange
    mock_transcriber = MagicMock(return_value={"text": "This is a test."})
    mock_pipeline.return_value = mock_transcriber

    adapter = HuggingFaceSTTAdapter(model_name="test-stt-model")
    # A valid base64 string for a silent wav file
    test_audio_base64 = (
        "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAAABkYXRhAAAAAA=="
    )

    # Act
    text = await adapter.transcribe_audio(test_audio_base64)

    # Assert
    assert text == "This is a test."
    mock_pipeline.assert_called_once_with(
        "automatic-speech-recognition",
        model="test-stt-model",
        token="",
    )
    mock_transcriber.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.adapters.hf_stt_adapter.pipeline")
async def test_hf_stt_transcribe_audio_failure(mock_pipeline):
    # Arrange
    mock_transcriber = MagicMock(side_effect=Exception("Pipeline error"))
    mock_pipeline.return_value = mock_transcriber

    adapter = HuggingFaceSTTAdapter(model_name="test-stt-model")

    # Act
    text = await adapter.transcribe_audio("bad-base64")

    # Assert
    assert text == ""
