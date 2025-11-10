# backend/tests/adapters/test_openai_llm_adapter.py
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.services.adapters.openai_llm_adapter import OpenAILLMAdapter


@pytest.mark.asyncio
@patch("app.services.adapters.openai_llm_adapter.AsyncOpenAI")
async def test_openai_llm_generate_response_success(MockAsyncOpenAI):
    # Arrange
    mock_choice = MagicMock()
    mock_choice.message.content = "  Test response  "

    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    mock_client = MockAsyncOpenAI.return_value
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)

    adapter = OpenAILLMAdapter(model_name="test-gpt")

    # Act
    response = await adapter.generate_response("Test prompt")

    # Assert
    assert response == "Test response"
    mock_client.chat.completions.create.assert_awaited_once_with(
        model="test-gpt",
        messages=[{"role": "user", "content": "Test prompt"}],
        max_tokens=150,
    )


@pytest.mark.asyncio
@patch("app.services.adapters.openai_llm_adapter.AsyncOpenAI")
async def test_openai_llm_generate_response_failure(MockAsyncOpenAI):
    # Arrange
    mock_client = MockAsyncOpenAI.return_value
    mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API error"))

    adapter = OpenAILLMAdapter(model_name="test-gpt")

    # Act
    response = await adapter.generate_response("Test prompt")

    # Assert
    assert "Sorry, I encountered an error" in response
