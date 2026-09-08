import asyncio
import os
from typing import List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import re
import time

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


def get_all_urls(base_url: str) -> List[str]:
    """
    Discover all URLs from the deployed site by crawling internal links
    """
    urls = set()
    visited = set()

    # Start with the base URL
    to_visit = [base_url]

    # Also check for sitemap if available
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    try:
        sitemap_response = requests.get(sitemap_url)
        if sitemap_response.status_code == 200:
            # Parse sitemap for URLs
            from xml.etree import ElementTree as ET
            root = ET.fromstring(sitemap_response.content)
            for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                url = url_elem.text.strip()
                if url.startswith(base_url):
                    urls.add(url)
    except:
        # If sitemap is not available, proceed with regular crawling
        pass

    # Crawl the site to find all internal links
    while to_visit and len(urls) < 10:  # Limit to 10 URLs for quick test
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Add current URL to the list
                urls.add(current_url)

                # Find all internal links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)

                    # Only add URLs from the same domain
                    if urlparse(full_url).netloc == urlparse(base_url).netloc:
                        if full_url not in visited and full_url.startswith(base_url):
                            to_visit.append(full_url)
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")
            continue

    return list(urls)


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
        model="embed-multilingual-v3.0",  # Using multilingual model for diverse content
        input_type="search_document"  # Appropriate for document search
    )

    return response.embeddings


def create_collection(collection_name: str = "rag_embeddings"):
    """
    Create a Qdrant collection for storing embeddings
    """
    # Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY", None)

    try:
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=False
        )

        # Check if collection already exists
        try:
            client.get_collection(collection_name)
            print(f"Collection '{collection_name}' already exists")
            return client
        except:
            pass

        # Create new collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere multilingual embeddings are 1024-dimensional
                distance=models.Distance.COSINE
            )
        )

        print(f"Collection '{collection_name}' created successfully")
        return client
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        print("Running in demo mode without vector storage...")
        return None


def save_chunk_to_qdrant(client, text_chunk: str, url: str, title: str = "", vector: List[float] = None):
    """
    Save a text chunk to Qdrant with metadata
    """
    if client is None:
        # In demo mode, just return without storing
        print(f"  [DEMO MODE] Would save chunk to Qdrant: {len(text_chunk)} chars from {url}")
        return "demo-id"

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
        collection_name="rag_embeddings",
        points=[
            models.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
        ]
    )

    return point_id


async def main():
    """
    Main function to execute the complete embedding pipeline
    """
    print("Starting the embedding pipeline demo...")

    # Target deployed site
    base_url = "https://hackathon01-book-creation-lnvq.vercel.app/"

    print(f"Discovering URLs from {base_url}...")
    urls = get_all_urls(base_url)
    print(f"Found {len(urls)} URLs to process")

    if urls:
        # Process just the first URL for demo
        url = urls[0]
        print(f"Processing URL: {url}")

        # Extract text from URL
        text_content = extract_text_from_url(url)
        print(f"Extracted text length: {len(text_content)} characters")

        if text_content.strip():
            # Chunk the text
            chunks = chunk_text(text_content)
            print(f"Split into {len(chunks)} chunks")

            # Process first chunk only for demo
            if chunks:
                chunk = chunks[0]
                print(f"Processing first chunk of {len(chunk)} characters...")

                try:
                    # Generate embedding for the chunk
                    embeddings = embed([chunk])
                    print(f"Generated embedding of {len(embeddings[0])} dimensions")

                    # Create Qdrant collection (with fallback for demo mode)
                    print("Setting up Qdrant collection...")
                    qdrant_client = create_collection("rag_embeddings")

                    # Save to Qdrant
                    point_id = save_chunk_to_qdrant(
                        qdrant_client,
                        chunk,
                        url,
                        title=f"First chunk from {url}",
                        vector=embeddings[0]
                    )

                    print(f"Chunk saved to Qdrant with ID: {point_id}")

                except Exception as e:
                    print(f"Error during embedding or storage: {e}")

    print("Demo completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())