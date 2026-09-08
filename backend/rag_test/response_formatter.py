from typing import List, Dict, Any, Optional
import json
from datetime import datetime

def format_search_response(
    query: str,
    results: List[Dict[str, Any]],
    validation_results: List[Dict[str, Any]],
    top_k: int,
    processing_time: Optional[float] = None
) -> Dict[str, Any]:
    """
    Format clean JSON response for search results
    """
    response = {
        "query": query,
        "top_k": top_k,
        "total_results": len(results),
        "timestamp": datetime.utcnow().isoformat(),
        "processing_time_ms": processing_time,
        "results": []
    }

    for i, (result, validation) in enumerate(zip(results, validation_results)):
        formatted_result = {
            "rank": i + 1,
            "id": result["id"],
            "score": result["score"],
            "text": result["text"],
            "metadata": {
                "url": result["url"],
                "title": result["title"],
                "source": result["source"]
            },
            "validation": validation
        }
        response["results"].append(formatted_result)

    return response

def format_error_response(
    error_message: str,
    error_type: str = "GENERAL_ERROR",
    status_code: int = 500
) -> Dict[str, Any]:
    """
    Format clean JSON response for errors
    """
    error_response = {
        "error": {
            "type": error_type,
            "message": error_message,
            "timestamp": datetime.utcnow().isoformat(),
            "status_code": status_code
        }
    }
    return error_response

def serialize_response(response: Dict[str, Any]) -> str:
    """
    Serialize response to JSON string with proper formatting
    """
    return json.dumps(response, indent=2, ensure_ascii=False)

def validate_response_format(response: Dict[str, Any]) -> bool:
    """
    Validate that response follows expected structure
    """
    required_keys = ["query", "top_k", "total_results", "timestamp", "results"]
    has_required_keys = all(key in response for key in required_keys)

    if not has_required_keys:
        return False

    # Validate results structure
    if not isinstance(response["results"], list):
        return False

    for result in response["results"]:
        required_result_keys = ["rank", "id", "score", "text", "metadata", "validation"]
        if not all(key in result for key in required_result_keys):
            return False

    return True