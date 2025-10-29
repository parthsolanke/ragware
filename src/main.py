from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.models import QueryRequest, QueryResponse, ContextChunk
from src.vector_dataframe import VectorDataframe
from src.ragware import RAGWare

settings = get_settings()
ragware = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ragware
    
    print("Starting RAGWare API...")
    
    vdf = VectorDataframe()
    ragware = RAGWare(vdf)
    
    print(f"Vector database loaded with {len(vdf.df)} chunks")
    print("RAG system initialized successfully")
    
    yield
    
    print("Shutting down RAG Coffee Sales API...")


app = FastAPI(
    title="RAGWare API",
    description="RAG-based natural language Q&A",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "RAG Coffee Sales API",
        "version": "1.0.0",
        "status": "running",
        "description": "Ask questions about coffee sales data using natural language",
        "endpoints": {
            "query": "/query (POST) - Ask questions about coffee sales",
            "health": "/health (GET) - Check API health",
        },
        "example_queries": [
            "What time of day do people buy the most coffee?",
            "Which coffee type is most popular?",
            "What is the average order value?",
            "How many sales were made in the morning?"
        ]
    }

@app.get("/health")
async def health():
    if ragware is None:
        return {"status": "initializing"}
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_coffee_sales(request: QueryRequest):
    if ragware is None:
        raise HTTPException(status_code=503, detail="RAGWare not initialized")
    try:
        result = ragware.query(
            user_query=request.query,
            top_k=request.top_k,
            return_context=request.return_context
        )
        
        context_chunks = None
        if request.return_context and result["context"] is not None:
            context_chunks = [
                ContextChunk(
                    chunk_text=row['chunked_combined'],
                    similarity=float(row['similarity']),
                    chunk_id=idx
                )
                for idx, row in result["context"].iterrows()
            ]
        
        return QueryResponse(
            success=True,
            response=result["response"],
            query=request.query,
            context=context_chunks,
            error=None
        )
    
    except Exception as e:
        return QueryResponse(
            success=False,
            response="",
            query=request.query,
            context=None,
            error=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )