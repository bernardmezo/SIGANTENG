# backend/tests/adapters/test_gtts_tts_adapter.py
import base64
from unittest.mock import MagicMock, patch

import pytest
from app.services.adapters.gtts_tts_adapter import GTTSTransformer


@pytest.mark.asyncio
@patch("app.services.adapters.gtts_tts_adapter.gTTS")
async def test_gtts_generate_audio_success(mock_gtts):
    # Arrange
    # Mock the gTTS object and its write_to_fp method
    mock_tts_instance = MagicMock()

    def write_to_fp_side_effect(fp):
        fp.write(b"fake_audio_bytes")

    mock_tts_instance.write_to_fp = MagicMock(side_effect=write_to_fp_side_effect)
    mock_gtts.return_value = mock_tts_instance

    adapter = GTTSTransformer()

    # Act
    audio_base64 = await adapter.generate_audio("Hello world")

    # Assert
    assert audio_base64 == base64.b64encode(b"fake_audio_bytes").decode("utf-8")
    mock_gtts.assert_called_once_with(text="Hello world", lang="en")
    mock_tts_instance.write_to_fp.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.adapters.gtts_tts_adapter.gTTS")
async def test_gtts_generate_audio_failure(mock_gtts):
    # Arrange
    mock_gtts.side_effect = Exception("gTTS error")

    adapter = GTTSTransformer()

    # Act
    audio_base64 = await adapter.generate_audio("Hello world")

    # Assert
    assert audio_base64 == ""
