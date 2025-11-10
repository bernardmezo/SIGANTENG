# backend/tests/test_tasks.py
from unittest.mock import MagicMock, patch

import pytest
from app.tasks import long_llm_generation_task


@patch("app.tasks.redis_client")
@patch("app.tasks.LLMService")
def test_long_llm_generation_task_success(MockLLMService, mock_redis_client):
    # Arrange
    mock_llm_instance = MockLLMService.return_value

    async def mock_generate_response(prompt):
        return "A long generated response."

    mock_llm_instance.generate_response = mock_generate_response

    # Act
    # Using .run() executes the task logic directly without a worker
    result = long_llm_generation_task.run("A long prompt")

    # Assert
    assert result["status"] == "SUCCESS"
    assert result["result"] == "A long generated response."
    # Check that the service was initialized with no provider, using the default
    MockLLMService.assert_called_once_with()


@patch("app.tasks.long_llm_generation_task.retry")
@patch("app.tasks.LLMService")
def test_long_llm_generation_task_failure(MockLLMService, mock_retry):
    # Arrange
    error_message = "LLM service failed"

    async def mock_fail(prompt):
        raise Exception(error_message)

    mock_llm_service_instance = MockLLMService.return_value
    mock_llm_service_instance.generate_response = mock_fail

    mock_retry.side_effect = Exception("Celery retry called")

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        # Use .run() to test the task's logic
        long_llm_generation_task.run("A failing prompt")

    assert "Celery retry called" in str(excinfo.value)
    mock_retry.assert_called_once()
