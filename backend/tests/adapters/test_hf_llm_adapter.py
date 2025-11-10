# backend/tests/adapters/test_hf_llm_adapter.py
from unittest.mock import MagicMock, patch

import pytest
from app.services.adapters.hf_llm_adapter import HuggingFaceLLMAdapter


@pytest.mark.asyncio
@patch("app.services.adapters.hf_llm_adapter.pipeline")
async def test_hf_llm_generate_response_success(mock_pipeline):
    # Arrange
    mock_generator = MagicMock(return_value=[{"generated_text": "Test response"}])
    mock_pipeline.return_value = mock_generator

    adapter = HuggingFaceLLMAdapter(model_name="test-model")

    # Act
    response = await adapter.generate_response("Test prompt")

    # Assert
    assert response == "Test response"
    mock_pipeline.assert_called_once_with(
        "text-generation",
        model="test-model",
        token="",
    )
    mock_generator.assert_called_once_with("Test prompt", max_new_tokens=150)


@pytest.mark.asyncio
@patch("app.services.adapters.hf_llm_adapter.pipeline")
async def test_hf_llm_generate_response_failure(mock_pipeline):
    # Arrange
    mock_generator = MagicMock(side_effect=Exception("Pipeline error"))
    mock_pipeline.return_value = mock_generator

    adapter = HuggingFaceLLMAdapter(model_name="test-model")

    # Act
    response = await adapter.generate_response("Test prompt")

    # Assert
    assert "Sorry, I encountered an error" in response
