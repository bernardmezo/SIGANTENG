# backend/tests/test_ai_orchestrator.py
from unittest.mock import MagicMock, patch

import pytest
from app.services.ai_orchestrator import AIOrchestratorService


@patch("app.services.ai_orchestrator.long_llm_generation_task")
def test_submit_long_llm_generation(mock_task):
    # Arrange
    mock_async_result = MagicMock()
    mock_async_result.id = "test-task-id-abc"
    mock_task.delay.return_value = mock_async_result

    orchestrator = AIOrchestratorService()

    # Act
    task_id = orchestrator.submit_long_llm_generation("Test prompt")

    # Assert
    assert task_id == "test-task-id-abc"
    mock_task.delay.assert_called_once_with("Test prompt")


@patch("app.services.ai_orchestrator.AsyncResult")
@patch("app.services.ai_orchestrator.redis.from_url")
def test_get_task_status_cached(mock_redis_from_url, MockAsyncResult):
    # Arrange
    mock_redis_client = MagicMock()
    mock_redis_client.get.return_value = "Cached result"
    mock_redis_from_url.return_value = mock_redis_client

    orchestrator = AIOrchestratorService()

    # Act
    result = orchestrator.get_task_status_and_result("test-task-id")

    # Assert
    assert result["status"] == "SUCCESS"
    assert result["result"] == "Cached result"
    # Celery's AsyncResult should not be called if cache hits
    MockAsyncResult.assert_not_called()


@patch("app.services.ai_orchestrator.AsyncResult")
@patch("app.services.ai_orchestrator.redis.from_url")
def test_get_task_status_pending(mock_redis_from_url, MockAsyncResult):
    # Arrange
    mock_redis_client = MagicMock()
    mock_redis_client.get.return_value = None
    mock_redis_from_url.return_value = mock_redis_client

    mock_task_result = MockAsyncResult.return_value
    mock_task_result.ready.return_value = False

    orchestrator = AIOrchestratorService()

    # Act
    result = orchestrator.get_task_status_and_result("test-task-id")

    # Assert
    assert result["status"] == "PENDING"
    assert result.get("result") is None


@patch("app.services.ai_orchestrator.AsyncResult")
@patch("app.services.ai_orchestrator.redis.from_url")
def test_get_task_status_success_not_cached(mock_redis_from_url, MockAsyncResult):
    # Arrange
    mock_redis_client = MagicMock()
    mock_redis_client.get.return_value = None
    mock_redis_from_url.return_value = mock_redis_client

    mock_task_result = MockAsyncResult.return_value
    mock_task_result.ready.return_value = True
    mock_task_result.successful.return_value = True
    mock_task_result.get.return_value = {"result": "Final result"}

    orchestrator = AIOrchestratorService()

    # Act
    result = orchestrator.get_task_status_and_result("test-task-id")

    # Assert
    assert result["status"] == "SUCCESS"
    assert result["result"] == "Final result"
    # Verify that the result is cached after being fetched
    mock_redis_client.set.assert_called_once_with(
        "test-task-id", "Final result", ex=600
    )
