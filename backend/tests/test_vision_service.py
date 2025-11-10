# backend/tests/test_vision_service.py
from unittest.mock import AsyncMock, patch

import pytest
from app.services.vision_service import VisionService


# The patch decorators are applied from the outside in.
# The @pytest.mark.asyncio must be the innermost decorator for async tests.
# The patch for settings.HF_API_TOKEN replaces the value directly and does NOT
# pass an argument to the test function.
@patch("app.services.vision_service.settings.HF_API_TOKEN", "fake-hf-token")
@patch("app.services.vision_service.HuggingFaceVisionAdapter")
@pytest.mark.asyncio
async def test_get_image_description_success(mock_adapter):  # Removed mock_token
    # Arrange
    mock_adapter_instance = mock_adapter.return_value
    mock_adapter_instance.get_image_description = AsyncMock(
        return_value="a test caption"
    )

    service = VisionService(provider="huggingface")
    test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/epv2AAAAABJRU5ErkJggg=="

    # Act
    result = await service.get_image_description(test_image_base64)

    # Assert
    assert result == "a test caption"
    mock_adapter_instance.get_image_description.assert_awaited_once_with(
        test_image_base64
    )


@patch("app.services.vision_service.settings.HF_API_TOKEN", "fake-hf-token")
@patch("app.services.vision_service.HuggingFaceVisionAdapter")
@pytest.mark.asyncio
async def test_get_image_description_failure_propagates_exception(
    mock_adapter,
):  # Removed mock_token
    # Arrange
    error_message = "Adapter error"
    mock_adapter_instance = mock_adapter.return_value
    mock_adapter_instance.get_image_description = AsyncMock(
        side_effect=Exception(error_message)
    )

    service = VisionService(provider="huggingface")
    test_image_base64 = "a_bad_base64_string"

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        await service.get_image_description(test_image_base64)

    assert error_message in str(excinfo.value)
    mock_adapter_instance.get_image_description.assert_awaited_once_with(
        test_image_base64
    )
