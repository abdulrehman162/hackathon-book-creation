from typing import List, Dict, Any
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from config.settings import settings

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def search_similar(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant
        """
        try:
            # Prepare filters if provided
            qdrant_filters = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )

                if conditions:
                    qdrant_filters = models.Filter(
                        must=conditions
                    )

            # Perform the search
            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=top_k,
                with_payload=True,
                query_filter=qdrant_filters
            ).points

            # Format results
            formatted_results = []
            for result in search_results:
                formatted_result = {
                    "id": result.id,
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "url": result.payload.get("url", ""),
                    "title": result.payload.get("title", ""),
                    "source": result.payload.get("source", ""),
                    "metadata": result.payload
                }
                formatted_results.append(formatted_result)

            logger.info(f"Retrieved {len(formatted_results)} results from Qdrant")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching Qdrant: {e}")
            raise

    def get_vector_size(self) -> int:
        """
        Get the size of vectors in the collection
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.config.params.vectors.size
        except Exception as e:
            logger.error(f"Error getting vector size: {e}")
            raise

    def count_points(self) -> int:
        """
        Count total points in the collection
        """
        try:
            count_result = self.client.count(self.collection_name)
            return count_result.count
        except Exception as e:
            logger.error(f"Error counting points: {e}")
            raise