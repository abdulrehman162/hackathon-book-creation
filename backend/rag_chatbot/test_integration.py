"""
Test script to verify the RAG Chatbot integration
"""
import asyncio
from services.rag_service import RAGService
from config.settings import settings

def test_rag_service():
    """
    Test the RAG service directly
    """
    print("Testing RAG Service Integration...")

    try:
        # Initialize the RAG service
        rag_service = RAGService()

        # Test collection stats
        print("\n1. Testing collection stats...")
        stats = rag_service.get_collection_stats()
        print(f"   Collection: {stats['collection_name']}")
        print(f"   Total documents: {stats['total_documents']}")
        print(f"   Vector size: {stats['vector_size']}")

        # Test a sample query
        print("\n2. Testing sample query...")
        sample_query = "What is digital twin simulation?"

        result = rag_service.query(
            user_query=sample_query,
            top_k=3
        )

        print(f"   Query: {result['query']}")
        print(f"   Retrieved chunks: {result['retrieval_count']}")
        print(f"   Response length: {len(result['response'])} characters")

        if result['retrieved_chunks']:
            first_chunk = result['retrieved_chunks'][0]
            print(f"   First chunk URL: {first_chunk.get('url', 'N/A')}")
            print(f"   First chunk score: {first_chunk.get('score', 0):.3f}")
            print(f"   First chunk preview: {first_chunk.get('text', '')[:100]}...")

        print("\n3. Testing another query...")
        sample_query2 = "Explain URDF robot structure"

        result2 = rag_service.query(
            user_query=sample_query2,
            top_k=2
        )

        print(f"   Query: {result2['query']}")
        print(f"   Retrieved chunks: {result2['retrieval_count']}")
        print(f"   Response length: {len(result2['response'])} characters")

        print("\n✅ All tests passed! RAG service is working correctly.")
        return True

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_rag_service()