from typing import List, Dict, Any
import logging
from services.qdrant_service import QdrantService
from services.embedding_service import EmbeddingService
from services.groq_service import GroqService
from config.settings import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.embedding_service = EmbeddingService()
        self.groq_service = GroqService()

    def query(self,
              user_query: str,
              top_k: int = None,
              filters: Dict[str, Any] = None,
              system_prompt: str = None) -> Dict[str, Any]:
        """
        Main RAG query method
        """
        if top_k is None:
            top_k = settings.TOP_K

        try:
            logger.info(f"Processing RAG query: {user_query[:50]}...")

            # Step 1: Embed the user query
            query_embedding = self.embedding_service.embed_text(user_query)
            logger.info(f"Generated query embedding with {len(query_embedding)} dimensions")

            # Step 2: Search for similar chunks in Qdrant
            retrieved_chunks = self.qdrant_service.search_similar(
                query_vector=query_embedding,
                top_k=top_k,
                filters=filters
            )
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks from Qdrant")

            # Step 3: Generate response using Groq with context
            response = self.groq_service.generate_response(
                query=user_query,
                context_chunks=retrieved_chunks,
                system_prompt=system_prompt
            )

            # Step 4: Format and return result
            result = {
                "query": user_query,
                "response": response,
                "retrieved_chunks": retrieved_chunks,
                "retrieval_count": len(retrieved_chunks),
                "top_k_used": top_k
            }

            logger.info(f"RAG query completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            raise

    def chat(self,
             user_query: str,
             chat_history: List[Dict[str, str]] = None,
             top_k: int = None,
             filters: Dict[str, Any] = None,
             system_prompt: str = None) -> Dict[str, Any]:
        """
        RAG chat method with conversation history
        """
        if top_k is None:
            top_k = settings.TOP_K

        try:
            logger.info(f"Processing RAG chat query: {user_query[:50]}...")

            # Step 1: Embed the user query
            query_embedding = self.embedding_service.embed_text(user_query)
            logger.info(f"Generated query embedding with {len(query_embedding)} dimensions")

            # Step 2: Search for similar chunks in Qdrant
            retrieved_chunks = self.qdrant_service.search_similar(
                query_vector=query_embedding,
                top_k=top_k,
                filters=filters
            )
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks from Qdrant")

            # Step 3: Generate response using Groq with context and chat history
            response = self.groq_service.chat_with_context(
                query=user_query,
                context_chunks=retrieved_chunks,
                chat_history=chat_history,
                system_prompt=system_prompt
            )

            # Step 4: Format and return result
            result = {
                "query": user_query,
                "response": response,
                "retrieved_chunks": retrieved_chunks,
                "retrieval_count": len(retrieved_chunks),
                "top_k_used": top_k,
                "chat_history": chat_history or []
            }

            logger.info(f"RAG chat query completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error in RAG chat: {e}")
            raise

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the Qdrant collection
        """
        try:
            count = self.qdrant_service.count_points()
            vector_size = self.qdrant_service.get_vector_size()

            stats = {
                "total_documents": count,
                "vector_size": vector_size,
                "collection_name": settings.QDRANT_COLLECTION_NAME
            }

            logger.info(f"Retrieved collection stats: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            raise