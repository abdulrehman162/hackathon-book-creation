from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
import uvicorn
from services.rag_service import RAGService
from config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation Chatbot API with Qdrant and Groq",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Docusaurus default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

# Request/Response models
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="User query")
    top_k: Optional[int] = Field(default=None, ge=1, le=20, description="Number of top results to retrieve")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filters for search")
    system_prompt: Optional[str] = Field(default=None, description="Optional system prompt for LLM")

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="User query")
    chat_history: Optional[List[Dict[str, str]]] = Field(default=None, description="Chat history")
    top_k: Optional[int] = Field(default=None, ge=1, le=20, description="Number of top results to retrieve")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filters for search")
    system_prompt: Optional[str] = Field(default=None, description="Optional system prompt for LLM")

class SimpleChatResponse(BaseModel):
    answer: str

class FullChatResponse(BaseModel):
    query: str
    response: str
    retrieved_chunks: List[Dict[str, Any]]
    retrieval_count: int
    top_k_used: int
    chat_history: List[Dict[str, str]]

class StatsResponse(BaseModel):
    total_documents: int
    vector_size: int
    collection_name: str

@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    return {"message": "RAG Chatbot API is running", "version": "1.0.0"}

@app.post("/chat", response_model=SimpleChatResponse)
async def chat_endpoint(request: QueryRequest):
    """
    Chat endpoint for RAG queries - returns simple answer format
    """
    try:
        logger.info(f"Received chat request: {request.query[:50]}...")

        result = rag_service.query(
            user_query=request.query,
            top_k=request.top_k,
            filters=request.filters,
            system_prompt=request.system_prompt
        )

        logger.info(f"Chat response generated successfully")
        return SimpleChatResponse(answer=result["response"])

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/chat-with-history", response_model=FullChatResponse)
async def chat_with_history_endpoint(request: ChatRequest):
    """
    Chat endpoint with conversation history
    """
    try:
        logger.info(f"Received chat with history request: {request.query[:50]}...")

        result = rag_service.chat(
            user_query=request.query,
            chat_history=request.chat_history,
            top_k=request.top_k,
            filters=request.filters,
            system_prompt=request.system_prompt
        )

        logger.info(f"Chat with history response generated successfully")
        return FullChatResponse(**result)

    except Exception as e:
        logger.error(f"Error in chat with history endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get collection statistics
    """
    try:
        stats = rag_service.get_collection_stats()
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Try to get collection stats to verify connection
        stats = rag_service.get_collection_stats()
        return {
            "status": "healthy",
            "collection": stats["collection_name"],
            "documents": stats["total_documents"]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )