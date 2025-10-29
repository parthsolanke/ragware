from pydantic import BaseModel, Field
from typing import Optional, List


class QueryRequest(BaseModel):
    query: str = Field(..., description="User's question about coffee sales data")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of relevant chunks to retrieve")
    return_context: bool = Field(default=False, description="Whether to return retrieved context chunks")


class ContextChunk(BaseModel):
    chunk_text: str
    similarity: float
    chunk_id: Optional[int] = None


class QueryResponse(BaseModel):
    success: bool
    response: str
    query: str
    context: Optional[List[ContextChunk]] = None
    error: Optional[str] = None