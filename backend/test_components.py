import os
import sys
# Add the backend directory to the path so we can import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import get_all_urls, extract_text_from_url, chunk_text

def test_url_discovery():
    print("Testing URL discovery...")
    base_url = "https://hackathon01-book-creation-lnvq.vercel.app/"
    urls = get_all_urls(base_url)
    print(f"Found {len(urls)} URLs")
    if urls:
        print(f"First few URLs: {urls[:3]}")
    return urls

def test_text_extraction():
    print("\nTesting text extraction...")
    test_url = "https://hackathon01-book-creation-lnvq.vercel.app/"
    text = extract_text_from_url(test_url)
    print(f"Extracted text length: {len(text)} characters")
    print(f"First 200 characters: {text[:200]}...")
    return text

def test_chunking():
    print("\nTesting text chunking...")
    sample_text = "This is a sample text. " * 100  # Create a longer text
    chunks = chunk_text(sample_text, chunk_size=50)
    print(f"Split into {len(chunks)} chunks")
    if chunks:
        print(f"First chunk length: {len(chunks[0])} characters")
    return chunks

if __name__ == "__main__":
    print("Testing individual components of the embedding pipeline...\n")

    # Test URL discovery
    urls = test_url_discovery()

    # Test text extraction (only if we have URLs)
    if urls:
        text = test_text_extraction()

    # Test chunking
    chunks = test_chunking()

    print("\nAll tests completed successfully!")