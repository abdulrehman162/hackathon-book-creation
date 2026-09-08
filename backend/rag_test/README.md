# RAG Retrieval and Pipeline Testing

This module provides comprehensive testing capabilities for RAG (Retrieval Augmented Generation) systems to verify that stored vectors in Qdrant can be retrieved accurately.

## Features

- Query processing for vector similarity search in Qdrant
- Result validation to ensure retrieved chunks match original text
- Metadata verification (URL, chunk_id) to maintain data integrity
- Clean JSON response formatting for end-to-end testing
- Performance metrics and error handling

## Components

### 1. Query Processor (`query_processor.py`)
- Converts text queries to embedding vectors using Cohere
- Validates query input parameters
- Ensures consistency with stored embeddings

### 2. Qdrant Service (`qdrant_service.py`)
- Manages Qdrant client connections
- Performs vector similarity search
- Retrieves top-k results with metadata

### 3. Validators (`validators.py`)
- Validates text content integrity
- Verifies metadata fields (URL, chunk_id)
- Checks similarity scores and detects data corruption
- Provides comprehensive result validation

### 4. Response Formatter (`response_formatter.py`)
- Creates clean JSON responses
- Formats error responses appropriately
- Includes performance metrics
- Ensures consistent response structure

### 5. Main Testing Module (`main.py`)
- Orchestrates the complete testing pipeline
- Runs comprehensive end-to-end tests
- Provides detailed analysis of results

## Usage

### Running Tests
```bash
cd backend
python rag_test/main.py
```

### Simple Test
```bash
python rag_test/simple_test.py
```

### Direct API Usage
```python
from rag_test.main import test_rag_retrieval

result = test_rag_retrieval("Your query here", top_k=5)
print(result)
```

## Success Criteria Verification

The system verifies all required success criteria:

✅ **Query Qdrant and receive correct top-k matches**: Returns top-k most similar vectors based on cosine similarity

✅ **Retrieved chunks match original text**: Validates content integrity between stored and retrieved chunks

✅ **Metadata (url, chunk_id) returns correctly**: Verifies all metadata fields are preserved and returned correctly

✅ **End-to-end test with clean JSON output**: Provides structured JSON response with results, metadata, and validation

## Response Format

The system returns structured JSON responses:

```json
{
  "query": "What is robotics?",
  "top_k": 3,
  "total_results": 2,
  "timestamp": "2025-12-22T15:39:46.111857",
  "processing_time_ms": 4305.53,
  "results": [
    {
      "rank": 1,
      "id": "vector-id",
      "score": 0.440,
      "text": "Retrieved chunk text...",
      "metadata": {
        "url": "source-url",
        "title": "chunk-title",
        "source": "docusaurus_site"
      },
      "validation": {
        "overall_valid": true
      }
    }
  ]
}
```

## Environment Variables

The system requires the following environment variables:
- `COHERE_API_KEY`: Cohere API key for query embeddings
- `QDRANT_URL`: Qdrant service URL
- `QDRANT_API_KEY`: Qdrant API key (if using cloud service)