import time
import sys
import os
from typing import Dict, Any, List

# Add the backend directory to the path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rag_test.query_processor import generate_query_embedding, validate_query_input
from rag_test.qdrant_service import get_qdrant_client, search_similar_vectors
from rag_test.validators import validate_result_integrity
from rag_test.response_formatter import format_search_response, format_error_response, serialize_response

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_rag_retrieval(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Main function to test RAG retrieval and pipeline functionality
    """
    start_time = time.time()

    try:
        # Validate input
        validate_query_input(query, top_k)

        # Generate query embedding
        query_vector = generate_query_embedding(query)

        # Get Qdrant client
        client = get_qdrant_client()

        # Perform similarity search
        results = search_similar_vectors(client, query_vector, top_k)

        # Validate each result
        validation_results = []
        for result in results:
            validation = validate_result_integrity(result)
            validation_results.append(validation)

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Format the response
        response = format_search_response(
            query=query,
            results=results,
            validation_results=validation_results,
            top_k=top_k,
            processing_time=processing_time
        )

        return response

    except Exception as e:
        processing_time = (time.time() - start_time) * 1000
        error_response = format_error_response(
            error_message=str(e),
            error_type=type(e).__name__,
            status_code=500
        )
        error_response["processing_time_ms"] = processing_time
        return error_response

def run_comprehensive_test():
    """
    Run comprehensive end-to-end test of the RAG retrieval system
    """
    print("=== RAG Retrieval and Pipeline Testing ===")

    # Test queries
    test_queries = [
        "What is robotics?",
        "Docusaurus documentation setup",
        "AI and machine learning concepts"
    ]

    for i, query in enumerate(test_queries):
        print(f"\n--- Test {i+1}: '{query}' ---")

        # Run the test
        result = test_rag_retrieval(query, top_k=3)

        # Print formatted response
        print(serialize_response(result))

        # Analyze results
        if "error" not in result:
            print(f"\n[SUCCESS] Query processed successfully in {result.get('processing_time_ms', 'N/A')}ms")
            print(f"[SUCCESS] Retrieved {result['total_results']} results")

            # Check validation results
            valid_results = 0
            for j, res in enumerate(result['results']):
                if res['validation']['overall_valid']:
                    valid_results += 1
                    print(f"  Result {j+1}: [VALID] (score: {res['score']:.3f})")
                else:
                    print(f"  Result {j+1}: [INVALID] validation")

            print(f"[SUCCESS] {valid_results}/{len(result['results'])} results passed validation")
        else:
            print(f"\n[ERROR] Error occurred: {result['error']['message']}")

if __name__ == "__main__":
    run_comprehensive_test()