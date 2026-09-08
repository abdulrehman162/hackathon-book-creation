from typing import List
import logging
import os
import cohere
from config.settings import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        try:
            response = self.client.embed(
                texts=texts,
                model="embed-multilingual-v3.0",  # Use same model as stored embeddings
                input_type="search_query"  # For query embeddings
            )

            embeddings = [embedding for embedding in response.embeddings]
            logger.info(f"Generated embeddings for {len(texts)} text(s)")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        return self.embed_texts([text])[0]