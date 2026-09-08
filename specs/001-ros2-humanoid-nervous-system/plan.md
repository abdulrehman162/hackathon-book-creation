# Embedding Pipeline Setup - Architectural Plan

## 1. Scope and Dependencies

### In Scope:
- Extract text from deployed Docusaurus URLs (specifically https://hackathon01-book-creation-lnvq.vercel.app/)
- Generate embeddings using Cohere
- Store embeddings in Qdrant for RAG-based retrieval
- Implement URL crawling and text cleaning functionality
- Build a complete pipeline from URL discovery to vector storage

### Out of Scope:
- Frontend UI for querying the RAG system
- Advanced query processing beyond basic vector search
- Real-time content synchronization
- Complex authentication systems

### External Dependencies:
- Cohere API for embedding generation
- Qdrant vector database service
- Target Docusaurus site (https://hackathon01-book-creation-lnvq.vercel.app/)
- Python runtime environment

## 2. Key Decisions and Rationale

### Technology Stack Decision:
- **Python** for backend processing due to rich ecosystem for web scraping and ML
- **Cohere** for embeddings due to multilingual support and quality
- **Qdrant** for vector storage due to performance and ease of use
- **BeautifulSoup** for HTML parsing due to reliability

### Options Considered:
1. **Embedding providers**: OpenAI vs Cohere vs Hugging Face - Chose Cohere for multilingual support
2. **Vector databases**: Pinecone vs Qdrant vs Chroma - Chose Qdrant for self-hosting capability
3. **Web scraping**: Selenium vs Requests/BeautifulSoup - Chose Requests/BS for efficiency

### Rationale:
- Cohere provides high-quality multilingual embeddings suitable for technical documentation
- Qdrant offers excellent performance for similarity search with metadata filtering
- Requests + BeautifulSoup is efficient for static site crawling

## 3. Interfaces and API Contracts

### Public APIs:
- Input: `base_url` (string) - starting point for crawling
- Output: Vector embeddings stored in Qdrant with metadata
- Error handling: Graceful degradation on network failures

### Versioning Strategy:
- Semantic versioning for the pipeline (v1.0.0)
- Qdrant collection schema versioning in metadata

### Error Taxonomy:
- `400`: Invalid URL format
- `404`: Page not found during crawling
- `429`: Rate limit exceeded from target site
- `500`: Cohere API failure
- `503`: Qdrant service unavailable

## 4. Non-Functional Requirements and Budgets

### Performance:
- P95 latency: <5 seconds for single document processing
- Throughput: Process 10 pages per minute (respectful crawling)
- Resource caps: <512MB memory usage during processing

### Reliability:
- SLO: 99% successful embedding generation
- Error budget: 1% failure rate acceptable
- Degradation strategy: Cache results, fallback to partial processing

### Security:
- API keys stored in environment variables only
- No sensitive data stored in Qdrant payloads
- Rate limiting to respect target site policies

### Cost:
- Cohere API costs based on token usage
- Qdrant costs based on vector storage and queries

## 5. Data Management and Migration

### Source of Truth:
- Original Docusaurus site content
- Qdrant vector database as processed knowledge base

### Schema Evolution:
- Qdrant collection schema includes version in metadata
- Migration path for schema updates using collection aliases

### Data Retention:
- Embeddings retained indefinitely unless content changes
- Stale embeddings identified by content hash comparison

## 6. Operational Readiness

### Observability:
- Logging of processing steps and errors
- Metrics for crawl success rate and embedding quality
- Performance monitoring for API calls

### Alerting:
- Thresholds for processing failures (>5% failure rate)
- On-call owners for infrastructure issues

### Deployment:
- Containerized deployment with Docker
- Health checks for service availability
- Configuration via environment variables

## 7. Risk Analysis and Mitigation

### Top 3 Risks:
1. **Rate limiting from target site** - Mitigation: Implement respectful crawling with delays
2. **Cohere API costs** - Mitigation: Cache embeddings, process in batches
3. **Qdrant storage costs** - Mitigation: Optimize chunking strategy

### Blast Radius:
- Crawling issues affect only the embedding process
- API failures impact individual requests, not entire system

## 8. Evaluation and Validation

### Definition of Done:
- All URLs from target site crawled successfully
- Embeddings generated for all content
- Data stored in Qdrant with proper metadata
- Pipeline runs without errors

### Output Validation:
- Embedding dimension verification (1024 for Cohere multilingual model)
- Content integrity checks
- Metadata completeness validation

## 9. Implementation Phases

### Phase 1: Infrastructure Setup
- Set up Python project with UV package manager
- Install dependencies (requests, beautifulsoup4, cohere, qdrant-client)
- Create basic project structure

### Phase 2: Core Functionality
- Implement `get_all_urls()` function to discover all pages from target site
- Implement `extract_text_from_url()` for content extraction and cleaning
- Implement `chunk_text()` for content segmentation

### Phase 3: Embedding and Storage
- Implement `embed()` function using Cohere API
- Implement `create_collection()` for Qdrant setup
- Implement `save_chunk_to_qdrant()` for vector storage

### Phase 4: Pipeline Integration
- Create main function to orchestrate the complete pipeline
- Add error handling and logging
- Implement rate limiting for respectful crawling

## 10. Detailed Implementation Plan

### URL Discovery (`get_all_urls`)
- Start from base URL: https://hackathon01-book-creation-lnvq.vercel.app/
- Parse sitemap.xml if available to discover all pages
- Crawl internal links up to configurable depth
- Filter to only include same-domain URLs
- Return list of all discovered URLs

### Text Extraction (`extract_text_from_url`)
- Fetch HTML content from URL
- Parse with BeautifulSoup
- Remove script, style, and navigation elements
- Extract main content from Docusaurus-specific selectors:
  - `.container`
  - `.main-content`
  - `.theme-doc-content`
  - `article`
  - `main`
- Clean text by removing extra whitespace and special characters
- Preserve document structure and context

### Content Chunking (`chunk_text`)
- Split large documents into smaller chunks
- Default chunk size: 512 words
- Implement sentence-aware splitting to preserve context
- Add overlap between chunks to maintain semantic continuity
- Skip very short chunks (<10 words)

### Embedding Generation (`embed`)
- Initialize Cohere client with API key from environment
- Use "embed-multilingual-v3.0" model for technical content
- Set input_type to "search_document" for retrieval purposes
- Handle API rate limits and errors gracefully
- Process in batches to optimize API usage

### Qdrant Integration
- Initialize Qdrant client with connection details from environment
- Create collection with 1024-dimensional vectors (Cohere output)
- Use cosine distance for similarity search
- Store metadata: original text, URL, title, and source
- Generate unique IDs for each vector record

### Main Pipeline
- Coordinate all components in a single workflow
- Implement async processing for efficiency
- Add progress tracking and logging
- Include safeguards against overwhelming target site
- Limit processing to 10 URLs initially for demonstration