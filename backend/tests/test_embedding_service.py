# backend/tests/test_embedding_service.py
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from app.services.embedding_service import EmbeddingService


@pytest.mark.asyncio
@patch("app.services.embedding_service.SentenceTransformer")  # Patch the constructor
async def test_embedding_service_embed_text_single(MockSentenceTransformerConstructor):
    # Arrange
    # IMPORTANT: Reset the singleton model before each test to ensure the patch works
    EmbeddingService._model = None

    # Mock the instance that the constructor would return
    mock_model_instance = MockSentenceTransformerConstructor.return_value
    mock_model_instance.encode.return_value = np.array([0.1, 0.2, 0.3])

    # Now, when EmbeddingService() is called, it will get a mock SentenceTransformer
    service = EmbeddingService(model_name="test-model")
    text_input = "hello world"

    # Act
    embedding = await service.embed_text(text_input)

    # Assert
    assert embedding == [0.1, 0.2, 0.3]
    mock_model_instance.encode.assert_called_once_with(text_input)
    MockSentenceTransformerConstructor.assert_called_once_with("test-model")


@pytest.mark.asyncio
@patch("app.services.embedding_service.SentenceTransformer")  # Patch the constructor
async def test_embedding_service_embed_text_list(MockSentenceTransformerConstructor):
    # Arrange
    # IMPORTANT: Reset the singleton model before each test to ensure the patch works
    EmbeddingService._model = None

    mock_model_instance = MockSentenceTransformerConstructor.return_value
    mock_model_instance.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])

    service = EmbeddingService(model_name="test-model")
    text_input = ["hello", "world"]

    # Act
    embeddings = await service.embed_text(text_input)

    # Assert
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]
    mock_model_instance.encode.assert_called_once_with(text_input)
    MockSentenceTransformerConstructor.assert_called_once_with("test-model")


@pytest.mark.asyncio
@patch(
    "app.services.embedding_service.SentenceTransformer",
    side_effect=Exception("Model load error"),
)  # Patch constructor to raise error
async def test_embedding_service_model_not_loaded_on_init(
    MockSentenceTransformerConstructor,
):
    # Arrange
    # IMPORTANT: Reset the singleton model before each test to ensure the patch works
    EmbeddingService._model = None

    # Act - service initialization will fail
    service = EmbeddingService(model_name="non-existent-model")

    # Assert - model should still be None
    assert EmbeddingService._model is None
    MockSentenceTransformerConstructor.assert_called_once_with("non-existent-model")

    # Act & Assert - subsequent embed_text call should raise RuntimeError
    with pytest.raises(RuntimeError, match="Embedding model is not loaded."):
        await service.embed_text("test")
