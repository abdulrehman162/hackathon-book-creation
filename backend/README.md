# Docusaurus Content Embedding Pipeline

This project implements an embedding pipeline that extracts text from Docusaurus URLs, generates embeddings using Cohere, and stores them in Qdrant for RAG-based retrieval.

## Features

- URL discovery from deployed Docusaurus sites
- Text extraction and cleaning from web pages
- Content chunking for optimal embedding
- Cohere-based embedding generation
- Qdrant vector storage with metadata
- Asynchronous processing

## Requirements

- Python 3.13+
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

1. Install dependencies:
```bash
pip install requests beautifulsoup4 cohere qdrant-client lxml
```

2. Set environment variables:
```bash
export COHERE_API_KEY="your-cohere-api-key"
export QDRANT_URL="http://localhost:6333"  # Optional, defaults to localhost
export QDRANT_API_KEY="your-qdrant-api-key"  # Optional, for cloud instances
```

## Usage

Run the complete pipeline:
```bash
python main.py
```

The pipeline will:
1. Discover URLs from the target Docusaurus site
2. Extract and clean text content from each page
3. Chunk the content into manageable pieces
4. Generate embeddings using Cohere
5. Store the embeddings in Qdrant with metadata

## Functions

- `get_all_urls(base_url)`: Discover all URLs from a deployed site
- `extract_text_from_url(url)`: Extract clean text from a URL
- `chunk_text(text, chunk_size=512)`: Split text into chunks
- `embed(texts)`: Generate embeddings using Cohere
- `create_collection(collection_name)`: Create Qdrant collection
- `save_chunk_to_qdrant(client, text_chunk, url, title, vector)`: Store embeddings in Qdrant
- `main()`: Execute the complete pipeline

## Configuration

The pipeline targets `https://hackathon01-book-creation-lnvq.vercel.app/` by default. Modify the `base_url` variable in the `main()` function to target a different site.

URL processing is limited to 10 for demonstration purposes to be respectful to the target server. Adjust the limit in the main loop as needed.