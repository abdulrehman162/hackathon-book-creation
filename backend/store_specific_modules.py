import os
from typing import List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import re
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def extract_text_from_url(url: str) -> str:
    """
    Extract clean text content from a URL
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get main content - try common content containers for Docusaurus
        content_selectors = [
            'main',  # Docusaurus main content
            '.container',  # Common container
            '.main-content',  # Common main content class
            '.content',  # Content class
            'article',  # Article tag
            '.markdown',  # Markdown content
            '.doc-content',  # Docusaurus documentation content
            '.theme-doc-content',  # Docusaurus theme content
            '.docs-page',  # Docusaurus docs page
            'body'  # Fallback to body
        ]

        text_content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text_content += element.get_text(separator=' ', strip=True) + "\n\n"
                break

        # If no specific content container found, get all text
        if not text_content.strip():
            text_content = soup.get_text(separator=' ', strip=True)

        # Clean up the text
        # Remove extra whitespace
        text_content = re.sub(r'\s+', ' ', text_content)
        # Remove special characters but keep basic punctuation
        text_content = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text_content)

        return text_content.strip()
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 512) -> List[str]:
    """
    Split text into chunks of specified size
    """
    if not text:
        return []

    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) > chunk_size and current_chunk:
            # If adding the next word exceeds chunk size, save current chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word)

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    # If a single chunk is still too long, split by sentences
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > chunk_size:
            # Split by sentences
            sentences = re.split(r'[.!?]+', chunk)
            temp_chunk = ""
            for sentence in sentences:
                sentence = sentence.strip()
                if len(temp_chunk + " " + sentence) <= chunk_size:
                    temp_chunk += " " + sentence
                else:
                    if temp_chunk.strip():
                        final_chunks.append(temp_chunk.strip())
                    temp_chunk = sentence
            if temp_chunk.strip():
                final_chunks.append(temp_chunk.strip())
        else:
            final_chunks.append(chunk)

    return [chunk for chunk in final_chunks if chunk.strip()]

def embed(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings using Cohere
    """
    # Initialize Cohere client
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(cohere_api_key)

    # Generate embeddings
    response = co.embed(
        texts=texts,
        model="embed-multilingual-v3.0",
        input_type="search_document"
    )

    return response.embeddings

def get_qdrant_client():
    """
    Get Qdrant client
    """
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None)

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=False
    )
    return client

def save_chunk_to_qdrant(client, text_chunk: str, url: str, title: str = "", vector: List[float] = None):
    """
    Save a text chunk to Qdrant with metadata
    """
    import uuid

    # Generate embedding if not provided
    if vector is None:
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        co = cohere.Client(cohere_api_key)
        response = co.embed(
            texts=[text_chunk],
            model="embed-multilingual-v3.0",
            input_type="search_document"
        )
        vector = response.embeddings[0]

    # Prepare payload with metadata
    payload = {
        "text": text_chunk,
        "url": url,
        "title": title,
        "source": "docusaurus_site"
    }

    # Generate a unique ID for the point
    point_id = str(uuid.uuid4())

    # Upsert the point to Qdrant
    client.upsert(
        collection_name="rag_embedding",
        points=[
            models.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
        ]
    )

    return point_id

def main():
    """
    Store content from specific modules in Qdrant
    """
    print("Starting to store specific module content in Qdrant...")

    # Target specific module URLs
    module_urls = [
        "https://hackathon01-book-creation-lnvq.vercel.app/docs/module2-digital-twin/",
        "https://hackathon01-book-creation-lnvq.vercel.app/docs/module3-ros2-communication/",
        "https://hackathon01-book-creation-lnvq.vercel.app/docs/module4-urdf-robot-structure/",
        "https://hackathon01-book-creation-lnvq.vercel.app/docs/module5-isaac-ai-brain/",
    ]

    # Create Qdrant client
    qdrant_client = get_qdrant_client()

    # Count vectors before adding new content
    initial_count = qdrant_client.count("rag_embedding")
    print(f"Initial vector count: {initial_count.count}")

    # Process each module URL
    for i, url in enumerate(module_urls):
        print(f"\nProcessing {url}...")

        # Extract text from URL
        text_content = extract_text_from_url(url)
        if not text_content.strip():
            print(f"  No content extracted from {url}")
            continue

        print(f"  Extracted {len(text_content)} characters")

        # Chunk the text
        chunks = chunk_text(text_content)
        print(f"  Split into {len(chunks)} chunks")

        # Process each chunk
        for j, chunk in enumerate(chunks):
            if len(chunk.strip()) < 10:  # Skip very short chunks
                continue

            try:
                # Generate embedding for the chunk
                embeddings = embed([chunk])

                # Save to Qdrant
                point_id = save_chunk_to_qdrant(
                    qdrant_client,
                    chunk,
                    url,
                    title=f"Module content from {url}",
                    vector=embeddings[0]
                )

                print(f"    Saved chunk {j+1} to Qdrant with ID: {point_id}")

            except Exception as e:
                print(f"    Error processing chunk {j+1} from {url}: {e}")
                continue

        # Add delay to be respectful to the target site
        time.sleep(1)

    # Count total vectors after adding new content
    final_count = qdrant_client.count("rag_embedding")
    print(f"\nFinal vector count: {final_count.count}")
    print(f"Added {final_count.count - initial_count.count} new vectors to Qdrant")

    # Verify by retrieving a few vectors
    print(f"\nRetrieving sample vectors to verify...")
    points = qdrant_client.scroll(
        collection_name='rag_embedding',
        limit=5  # Get first 5 points
    )

    for i, point in enumerate(points[0]):
        print(f'\\nSample {i+1}:')
        print(f'  URL: {point.payload.get("url", "")}')
        print(f'  Title: {point.payload.get("title", "")}')
        print(f'  Text preview: {str(point.payload.get("text", ""))[:100]}...')

if __name__ == "__main__":
    main()