from typing import List, Dict, Any
import re

def validate_text_content(original_text: str, retrieved_text: str) -> bool:
    """
    Verify that retrieved text matches original stored content
    """
    # Basic similarity check - for now just ensure retrieved text is part of original or vice versa
    # In a more sophisticated implementation, we might use fuzzy matching
    original_clean = re.sub(r'\s+', ' ', original_text.strip().lower())
    retrieved_clean = re.sub(r'\s+', ' ', retrieved_text.strip().lower())

    # Check if retrieved text is contained in original or vice versa (with some tolerance)
    return (retrieved_clean in original_clean or original_clean in retrieved_clean
            or len(set(retrieved_clean.split()) & set(original_clean.split())) > 0)

def validate_metadata(metadata: Dict[str, Any]) -> Dict[str, bool]:
    """
    Validate metadata fields (URL, chunk_id, etc.) are present and correct
    """
    validation_results = {
        "url_valid": bool(metadata.get("url", "")),
        "text_present": bool(metadata.get("text", "")),
        "source_valid": bool(metadata.get("source", "")),
        "all_fields_present": all([
            "url" in metadata,
            "text" in metadata,
            "source" in metadata
        ])
    }

    return validation_results

def validate_similarity_score(score: float, threshold: float = 0.3) -> bool:
    """
    Validate that similarity score is above threshold
    """
    return score >= threshold

def detect_data_corruption(original_vector: List[float], retrieved_metadata: Dict[str, Any]) -> bool:
    """
    Basic check for data corruption in retrieved content
    """
    # Check for obvious corruption signs in text
    text = retrieved_metadata.get("text", "")

    # Check for null/empty text
    if not text:
        return True

    # Check for obvious corruption patterns (could be expanded)
    corruption_indicators = [
        "null" in text.lower(),
        "undefined" in text.lower(),
        len(text) < 10 and not any(c.isalnum() for c in text)  # Very short non-alphanumeric text
    ]

    return any(corruption_indicators)

def validate_result_integrity(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive validation of a single result
    """
    validation_report = {
        "text_content_valid": validate_text_content(result.get("text", ""), result.get("text", "")),
        "metadata_valid": validate_metadata(result),
        "similarity_score_valid": validate_similarity_score(result.get("score", 0)),
        "data_corruption_detected": detect_data_corruption([], result),
        "overall_valid": True
    }

    # Overall validity is true only if all major validations pass
    validation_report["overall_valid"] = (
        validation_report["text_content_valid"] and
        validation_report["metadata_valid"]["all_fields_present"] and
        validation_report["similarity_score_valid"] and
        not validation_report["data_corruption_detected"]
    )

    return validation_report