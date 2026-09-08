import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams, Distance

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def get_qdrant_client():
    """
    Initialize and return Qdrant client with configuration
    """
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None)

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=False
    )

    return client

def search_similar_vectors(
    client: QdrantClient,
    query_vector: List[float],
    top_k: int = 5,
    collection_name: str = "rag_embedding"
) -> List[Dict[str, Any]]:
    """
    Perform vector similarity search in Qdrant and return top-k results
    """
    # Perform the search using the correct method name for newer Qdrant versions
    search_results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,  # Include payload (metadata) in results
    ).points

    # Format results
    formatted_results = []
    for result in search_results:
        formatted_result = {
            "id": result.id,
            "score": result.score,
            "payload": result.payload,
            "text": result.payload.get("text", "") if result.payload else "",
            "url": result.payload.get("url", "") if result.payload else "",
            "title": result.payload.get("title", "") if result.payload else "",
            "source": result.payload.get("source", "") if result.payload else ""
        }
        formatted_results.append(formatted_result)

    return formatted_results