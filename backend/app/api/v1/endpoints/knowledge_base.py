# backend/app/api/v1/endpoints/knowledge_base.py
from app.services.database_service import DatabaseService
from app.services.vector_db_service import PineconeService
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()


# --- Dependency Injection ---
def get_db_service() -> DatabaseService:
    return DatabaseService()


def get_vector_db_service() -> PineconeService:
    return PineconeService()


# --- Pydantic Models ---
class KnowledgeBaseQuery(BaseModel):
    query: str
    top_k: int = 5


class KnowledgeBaseResponse(BaseModel):
    results: list[dict]


class KnowledgeBaseInput(BaseModel):
    id: str
    text: str
    metadata: dict = {}


# --- Endpoints ---
@router.post("/query_knowledge_base", response_model=KnowledgeBaseResponse)
async def query_knowledge_base(
    query: KnowledgeBaseQuery,
    vector_db: PineconeService = Depends(get_vector_db_service),
):
    """
    Queries the vector database for documents relevant to the query.
    """
    try:
        # In a real implementation, you would first convert query.query to a vector
        # For now, we assume query_vectors can handle a text query (it can't, placeholder)
        # query_vector = await embedding_service.embed(query.query)
        # results = await vector_db.query_vectors(query_vector, top_k=query.top_k)

        # Placeholder response
        results = [
            {
                "id": "doc1",
                "score": 0.98,
                "metadata": {"text": "This is a placeholder response."},
            }
        ]
        return KnowledgeBaseResponse(results=results)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error querying knowledge base: {e}"
        )


@router.post("/add_to_knowledge_base")
async def add_to_knowledge_base(
    item: KnowledgeBaseInput,
    db: DatabaseService = Depends(get_db_service),
    vector_db: PineconeService = Depends(get_vector_db_service),
):
    """
    Adds a new item to the knowledge base (both SQL and vector DB).
    This is a simplified endpoint. A real implementation would be a background task.
    """
    try:
        # 1. Insert metadata into PostgreSQL
        # The 'data' dict should match the table schema
        insert_result = await db.insert_data(
            "knowledge_base", {"id": item.id, "content": item.text}
        )
        if not insert_result:
            raise HTTPException(
                status_code=500, detail="Failed to save metadata to database."
            )

        # 2. Create embedding and upsert to Vector DB (Pinecone)
        # This part should ideally be a background task.
        # query_vector = await embedding_service.embed(item.text)
        # await vector_db.upsert_vector(id=item.id, vector=query_vector, metadata=item.metadata)

        return {"message": f"Item {item.id} added to knowledge base."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding to knowledge base: {e}"
        )
