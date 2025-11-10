# backend/tests/test_api.py
from unittest.mock import MagicMock

import pytest
from app.api.v1.endpoints.ai_assistant import (
    get_ai_orchestrator,
    get_langchain_orchestrator,
    get_stt_service,
    get_tts_service,
    get_vision_service,
)
from fastapi.testclient import TestClient
from main import app

# --- Mocks ---
mock_ai_orchestrator = MagicMock()
mock_langchain_orchestrator = MagicMock()
mock_stt_service = MagicMock()
mock_tts_service = MagicMock()
mock_vision_service = MagicMock()

# --- Dependency Overrides ---
app.dependency_overrides[get_ai_orchestrator] = lambda: mock_ai_orchestrator
app.dependency_overrides[get_langchain_orchestrator] = (
    lambda: mock_langchain_orchestrator
)
app.dependency_overrides[get_stt_service] = lambda: mock_stt_service
app.dependency_overrides[get_tts_service] = lambda: mock_tts_service
app.dependency_overrides[get_vision_service] = lambda: mock_vision_service

client = TestClient(app)

# --- Tests ---


def test_submit_text_generation_task():
    # Arrange
    mock_ai_orchestrator.submit_long_llm_generation.return_value = "test-task-id-123"

    # Act
    response = client.post(
        "/api/v1/background/generate_text",
        json={"text": "Generate a poem about FastAPI."},
    )

    # Assert
    assert response.status_code == 202
    data = response.json()
    assert data["task_id"] == "test-task-id-123"
    assert data["status"] == "PENDING"
    mock_ai_orchestrator.submit_long_llm_generation.assert_called_once_with(
        "Generate a poem about FastAPI."
    )


def test_get_task_status_success():
    # Arrange
    mock_ai_orchestrator.get_task_status_and_result.return_value = {
        "task_id": "test-task-id-123",
        "status": "SUCCESS",
        "result": "Here is a poem about FastAPI...",
    }

    # Act
    response = client.get("/api/v1/background/tasks/test-task-id-123")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["result"] == "Here is a poem about FastAPI..."
    mock_ai_orchestrator.get_task_status_and_result.assert_called_once_with(
        "test-task-id-123"
    )


def test_get_task_status_pending():
    # Arrange
    mock_ai_orchestrator.get_task_status_and_result.return_value = {
        "task_id": "test-task-id-456",
        "status": "PENDING",
        "result": None,
    }

    # Act
    response = client.get("/api/v1/background/tasks/test-task-id-456")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING"
    assert data["result"] is None
