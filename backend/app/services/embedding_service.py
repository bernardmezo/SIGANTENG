# backend/app/services/embedding_service.py
# =================================================================
#
#                       Embedding Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service is responsible for converting text into vector
#  embeddings using a pre-trained sentence transformer model.
#  These embeddings are crucial for semantic search and RAG.
#
#  Key Features:
#  -------------
#  - Loads a specified sentence transformer model.
#  - Provides an asynchronous method to generate embeddings for text.
#  - Caches the loaded model for efficient reuse.
#
# =================================================================

import asyncio

from app.core.config import settings
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service for generating vector embeddings from text.
    """

    _model = None

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.DEFAULT_EMBEDDING_MODEL
        if EmbeddingService._model is None:
            try:
                # Load model only once
                EmbeddingService._model = SentenceTransformer(self.model_name)
                print(f"Embedding model '{self.model_name}' loaded successfully.")
            except Exception as e:
                print(f"Error loading embedding model '{self.model_name}': {e}")
                EmbeddingService._model = None

    async def embed_text(self, texts: str | list[str]) -> list[list[float]]:
        """
        Generates embeddings for a given text or list of texts.

        Args:
            texts: A single string or a list of strings to embed.

        Returns:
            A list of lists of floats, where each inner list is an embedding.
        """
        if EmbeddingService._model is None:
            raise RuntimeError("Embedding model is not loaded.")

        # SentenceTransformer's encode method is synchronous, so run in a thread pool
        embeddings = await asyncio.to_thread(EmbeddingService._model.encode, texts)

        # Convert numpy arrays to lists of floats for JSON serialization
        if isinstance(embeddings, list):
            return [embedding.tolist() for embedding in embeddings]
        else:
            return embeddings.tolist()  # For single text input


# Initialize a singleton instance
embedding_service = EmbeddingService()
