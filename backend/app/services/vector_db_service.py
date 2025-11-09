from pinecone import Pinecone, Index, PodSpec
from app.core.config import settings

class PineconeService:
    def __init__(self):
        self.api_key = settings.PINECONE_API_KEY
        self.environment = settings.PINECONE_ENVIRONMENT
        self.index_name = "ai-assistant-kb" # Default index name
        self.pinecone = None
        self.index = None
        
        if self.api_key and self.environment:
            self.pinecone = Pinecone(api_key=self.api_key, environment=self.environment)
            # Ensure index exists or create it
            if self.index_name not in self.pinecone.list_indexes():
                self.pinecone.create_index(
                    name=self.index_name,
                    dimension=1536, # Example dimension for OpenAI embeddings
                    metric='cosine',
                    spec=PodSpec(environment=self.environment)
                )
            self.index = self.pinecone.Index(self.index_name)
        else:
            print("Pinecone API key or environment not set. Pinecone service will be inactive.")

    async def upsert_vector(self, id: str, vector: list[float], metadata: dict = None):
        if not self.index:
            print("Pinecone index not initialized.")
            return
        try:
            self.index.upsert(vectors=[{"id": id, "values": vector, "metadata": metadata}])
            return True
        except Exception as e:
            print(f"Error upserting vector to Pinecone: {e}")
            return False

    async def query_vectors(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        if not self.index:
            print("Pinecone index not initialized.")
            return []
        try:
            response = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True
            )
            return response.matches
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return []
