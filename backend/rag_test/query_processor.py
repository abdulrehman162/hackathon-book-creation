import os
from typing import List
import cohere

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def generate_query_embedding(query_text: str) -> List[float]:
    """
    Convert text query to embedding vector using Cohere
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(cohere_api_key)

    # Generate embedding for the query
    response = co.embed(
        texts=[query_text],
        model="embed-multilingual-v3.0",  # Using same model as stored embeddings
        input_type="search_query"  # Appropriate for search queries
    )

    return response.embeddings[0]

def validate_query_input(query_text: str, top_k: int = 5) -> bool:
    """
    Validate query input parameters
    """
    if not query_text or len(query_text.strip()) == 0:
        raise ValueError("Query text cannot be empty")

    if not isinstance(top_k, int) or top_k <= 0 or top_k > 100:
        raise ValueError("top_k must be an integer between 1 and 100")

    # Limit query length to prevent resource issues
    if len(query_text) > 10000:
        raise ValueError("Query text exceeds maximum length of 10000 characters")

    return True