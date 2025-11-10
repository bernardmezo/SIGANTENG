# backend/tests/adapters/test_openai_vision_adapter.py
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.services.adapters.openai_vision_adapter import OpenAIVisionAdapter


@pytest.mark.asyncio
@patch("app.services.adapters.openai_vision_adapter.AsyncOpenAI")
async def test_openai_vision_get_description_success(MockAsyncOpenAI):
    # Arrange
    mock_choice = MagicMock()
    mock_choice.message.content = " A description of the image. "

    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    mock_client = MockAsyncOpenAI.return_value
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)

    adapter = OpenAIVisionAdapter(model_name="test-vision-gpt")
    test_image_base64 = "base64string"

    # Act
    description = await adapter.get_image_description(test_image_base64)

    # Assert
    assert description == "A description of the image."
    mock_client.chat.completions.create.assert_awaited_once()

    # Check the content of the message sent to the API
    call_args = mock_client.chat.completions.create.call_args
    messages = call_args.kwargs["messages"]
    assert messages[0]["content"][0]["type"] == "text"
    assert messages[0]["content"][1]["type"] == "image_url"
    assert (
        messages[0]["content"][1]["image_url"]["url"]
        == f"data:image/jpeg;base64,{test_image_base64}"
    )


@pytest.mark.asyncio
@patch("app.services.adapters.openai_vision_adapter.AsyncOpenAI")
async def test_openai_vision_get_description_failure(MockAsyncOpenAI):
    # Arrange
    mock_client = MockAsyncOpenAI.return_value
    mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API error"))

    adapter = OpenAIVisionAdapter(model_name="test-vision-gpt")

    # Act
    description = await adapter.get_image_description("bad-base64")

    # Assert
    assert "Could not generate a description" in description
