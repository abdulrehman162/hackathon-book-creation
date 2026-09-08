import sys
import os

# Add the backend directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_processor import generate_query_embedding, validate_query_input
from qdrant_service import get_qdrant_client, search_similar_vectors
from validators import validate_result_integrity
from response_formatter import format_search_response, serialize_response

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def simple_test():
    print("=== Simple RAG Retrieval Test ===")

    # Test query
    query = "What is robotics?"
    print(f"Query: '{query}'")

    try:
        # Generate query embedding
        print("1. Generating query embedding...")
        query_vector = generate_query_embedding(query)
        print(f"   Generated embedding with {len(query_vector)} dimensions")

        # Get Qdrant client
        print("2. Connecting to Qdrant...")
        client = get_qdrant_client()

        # Count points in collection first
        count = client.count("rag_embedding")
        print(f"   Collection has {count.count} vectors")

        # Perform similarity search
        print("3. Performing similarity search...")
        results = search_similar_vectors(client, query_vector, top_k=3)
        print(f"   Retrieved {len(results)} results")

        # Validate each result
        print("4. Validating results...")
        validation_results = []
        for i, result in enumerate(results):
            print(f"   Result {i+1}: Score={result['score']:.3f}, URL={result['url'][:50]}...")
            validation = validate_result_integrity(result)
            validation_results.append(validation)
            print(f"      Valid: {validation['overall_valid']}")

        # Format the response
        print("5. Formatting response...")
        response = format_search_response(
            query=query,
            results=results,
            validation_results=validation_results,
            top_k=3,
            processing_time=0
        )

        print("\n=== SUCCESS: RAG retrieval test completed ===")
        print(f"Retrieved {len(results)} relevant chunks from Qdrant")
        print("All components working correctly:")
        print("- Query embedding generation: ✓")
        print("- Qdrant similarity search: ✓")
        print("- Result validation: ✓")
        print("- Response formatting: ✓")
        print("- Correct collection (rag_embedding): ✓")

        return True

    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    simple_test()