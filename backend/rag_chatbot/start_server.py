import uvicorn
import os
from config.settings import settings

def main():
    """
    Start the RAG Chatbot API server
    """
    print("Starting RAG Chatbot API Server...")
    print(f"Host: {settings.APP_HOST}")
    print(f"Port: {settings.APP_PORT}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Qdrant Collection: {settings.QDRANT_COLLECTION_NAME}")

    uvicorn.run(
        "api.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

if __name__ == "__main__":
    main()