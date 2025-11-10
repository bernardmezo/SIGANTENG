# backend/app/services/vector_db_service.py
# =================================================================
#
#                 Vector Database Service (Placeholder)
#
# =================================================================
#
#  Purpose:
#  --------
#  Provides a placeholder implementation for a vector database service.
#  This allows the application to run without a concrete vector DB
#  dependency (like Pinecone) while the architecture is being developed.
#
#  Key Features:
#  -------------
#  - Implements the same method signatures as a real service.
#  - Returns empty or default data.
#  - Logs warnings to indicate it's a placeholder.
#
# =================================================================

from app.core.config import settings


class PineconeService:  # Name is kept temporarily to avoid breaking imports
    """
    Placeholder service for vector database interactions.
    This service does NOT connect to a real vector database.
    """

    def __init__(self):
        # Check if keys exist to simulate a real service's setup logic
        self.api_key = settings.PINECONE_API_KEY
        if not self.api_key:
            print(
                "WARNING: Pinecone API key not set. Vector DB Service is in placeholder mode."
            )

    async def upsert_vector(self, id: str, vector: list[float], metadata: dict = None):
        """Placeholder for upserting a vector."""
        print(f"PLACEHOLDER: Upserting vector for id {id}. Not implemented.")
        return True

    async def query_vectors(
        self, query_vector: list[float], top_k: int = 5
    ) -> list[dict]:
        """Placeholder for querying vectors."""
        print("PLACEHOLDER: Querying vectors. Returning empty list. Not implemented.")
        return []
