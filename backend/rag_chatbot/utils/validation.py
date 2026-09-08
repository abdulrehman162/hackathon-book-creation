from typing import Any, Dict
import re

def validate_query(query: str) -> bool:
    """
    Validate user query
    """
    if not query or not query.strip():
        return False

    if len(query.strip()) < 3:
        return False

    return True

def validate_filters(filters: Dict[str, Any]) -> bool:
    """
    Validate search filters
    """
    if not filters:
        return True

    # Basic validation - ensure it's a dictionary with string keys
    if not isinstance(filters, dict):
        return False

    # Check for potentially dangerous keys
    for key in filters.keys():
        if not isinstance(key, str):
            return False
        # Prevent SQL injection-like patterns
        if re.search(r'[;\'"\\]', key):
            return False

    return True

def sanitize_text(text: str) -> str:
    """
    Sanitize text input
    """
    if not text:
        return ""

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[;\'"\\]', '', text)
    return sanitized.strip()

def format_retrieved_chunks(chunks: list) -> list:
    """
    Format retrieved chunks for response
    """
    formatted_chunks = []
    for chunk in chunks:
        formatted_chunk = {
            "id": chunk.get("id", ""),
            "score": chunk.get("score", 0.0),
            "text": chunk.get("text", "")[:500],  # Limit text length
            "url": chunk.get("url", ""),
            "title": chunk.get("title", ""),
            "source": chunk.get("source", "")
        }
        formatted_chunks.append(formatted_chunk)

    return formatted_chunks