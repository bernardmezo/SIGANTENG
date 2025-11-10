# backend/tests/adapters/test_hf_vision_adapter.py
from unittest.mock import MagicMock, patch

import pytest
from app.services.adapters.hf_vision_adapter import HuggingFaceVisionAdapter


@pytest.mark.asyncio
@patch("app.services.adapters.hf_vision_adapter.pipeline")
async def test_hf_vision_get_description_success(mock_pipeline):
    # Arrange
    mock_captioner = MagicMock(return_value=[{"generated_text": "a test caption"}])
    mock_pipeline.return_value = mock_captioner

    adapter = HuggingFaceVisionAdapter(model_name="test-vision-model")
    test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/epv2AAAAABJRU5ErkJggg=="

    # Act
    description = await adapter.get_image_description(test_image_base64)

    # Assert
    assert description == "a test caption"
    mock_pipeline.assert_called_once_with(
        "image-to-text",
        model="test-vision-model",
        token="",
    )
    # We can't easily assert the content of the BytesIO object,
    # but we can confirm the mock was called.
    mock_captioner.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.adapters.hf_vision_adapter.pipeline")
async def test_hf_vision_get_description_failure(mock_pipeline):
    # Arrange
    mock_captioner = MagicMock(side_effect=Exception("Pipeline error"))
    mock_pipeline.return_value = mock_captioner

    adapter = HuggingFaceVisionAdapter(model_name="test-vision-model")

    # Act
    description = await adapter.get_image_description("bad-base64")

    # Assert
    assert "Could not generate a description" in description
