from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.database_service import SupabaseService
from app.services.vector_db_service import PineconeService

router = APIRouter()

# Initialize services
supabase_service = SupabaseService()
pinecone_service = PineconeService()

class KnowledgeBaseQuery(BaseModel:
    query: str
    top_k: int = 5

class KnowledgeBaseResponse(BaseModel:
    results: list[dict]

@router.post("/query_knowledge_base", response_model=KnowledgeBaseResponse)
async def query_knowledge_base(query: KnowledgeBaseQuery):
    # Example: Query Pinecone for relevant documents
    try:
        results = await pinecone_service.query_vectors(query.query, query.top_k)
        # Fallback or combine with Supabase if needed
        return KnowledgeBaseResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying knowledge base: {e}")

@router.post("/add_to_knowledge_base")
async def add_to_knowledge_base(data: dict):
    # Example: Add data to Supabase and Pinecone
    try:
        await supabase_service.insert_data("knowledge_base", data)
        # Assuming data contains text that needs to be embedded and stored in Pinecone
        # await pinecone_service.upsert_vector(data["id"], data["text"])
        return {"message": "Data added to knowledge base"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding to knowledge base: {e}")
