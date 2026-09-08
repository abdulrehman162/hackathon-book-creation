# RAG Retrieval and Pipeline Testing - Architectural Plan

## 1. Scope and Dependencies

### In Scope:
- Query processing system for vector similarity search in Qdrant
- Result validation to verify retrieved chunks match original text
- Metadata verification to ensure URL and chunk_id integrity
- Clean JSON response formatting for end-to-end testing
- Performance metrics and error handling
- Integration with existing "rag_embedding" collection

### Out of Scope:
- Building the RAG generation component (only retrieval testing)
- Modifying existing stored vectors
- Training or fine-tuning embedding models
- User interface for the testing system

### External Dependencies:
- Qdrant vector database service
- Cohere API for query embedding generation
- Existing "rag_embedding" collection with stored vectors
- Python runtime environment

## 2. Key Decisions and Rationale

### Technology Stack Decision:
- **Python** for implementation due to Qdrant client library support
- **Qdrant** for vector similarity search (same as storage system)
- **Cohere** for query embedding generation (consistent with stored embeddings)
- **JSON** for response formatting (standard, interoperable format)

### Options Considered:
1. **Query embedding providers**: OpenAI vs Cohere vs Hugging Face - Chose Cohere to match stored embeddings
2. **Response format**: JSON vs XML vs Protocol Buffers - Chose JSON for simplicity and compatibility
3. **Testing approach**: Unit tests vs Integration tests vs End-to-end - Chose end-to-end for comprehensive validation

### Rationale:
- Using same embedding model (Cohere) ensures consistency between storage and retrieval
- JSON format provides flexibility and standardization
- Direct Qdrant integration provides optimal performance
- Comprehensive testing approach validates complete pipeline

## 3. Interfaces and API Contracts

### Public APIs:
- Input: `query_text` (string), `top_k` (integer), `filters` (optional object)
- Output: JSON response with results, metadata, and similarity scores
- Error handling: Structured error responses with appropriate HTTP codes

### Versioning Strategy:
- API versioning through endpoint paths (v1, v2, etc.)
- Response schema versioning in metadata
- Backward compatibility maintained for major versions

### Idempotency, Timeouts, Retries:
- Query operations are idempotent (same input produces same output)
- Timeout: 30 seconds for query processing
- Retry: 3 attempts for transient Qdrant connection failures

### Error Taxonomy with status codes:
- `400`: Invalid query parameters
- `401`: Authentication failure with Qdrant/Cohere
- `404`: Qdrant collection not found
- `429`: Rate limit exceeded from external services
- `500`: Internal processing error
- `503`: Qdrant service unavailable

## 4. Non-Functional Requirements and Budgets

### Performance:
- P95 latency: <2 seconds for query processing
- Throughput: 10 queries per second
- Resource caps: <512MB memory usage during operation
- Concurrency: Support 100 concurrent requests

### Reliability:
- SLO: 99.9% successful query completion
- Error budget: 0.1% failure rate acceptable
- Degradation strategy: Graceful degradation with reduced top-k when under load

### Security:
- API keys stored in environment variables only
- Input validation to prevent injection attacks
- Rate limiting to prevent abuse
- Secure transmission with HTTPS

### Cost:
- Cohere API costs based on query volume
- Qdrant costs based on compute and storage usage

## 5. Data Management and Migration

### Source of Truth:
- Qdrant "rag_embedding" collection as vector storage
- Original source documents as content reference

### Schema Evolution:
- Response schema versioning to support future enhancements
- Migration path for schema updates using version negotiation

### Data Retention:
- Temporary query logs for debugging (7 days)
- Performance metrics retention (30 days)
- Error logs retention (90 days)

## 6. Operational Readiness

### Observability:
- Query response time metrics
- Success/failure rate tracking
- Resource utilization monitoring
- Error rate and type analysis

### Alerting:
- Thresholds for response time degradation (>3 seconds)
- Error rate spikes (>5% failure rate)
- Qdrant connection failures

### Runbooks for common tasks:
- Query performance troubleshooting
- Qdrant connection issue resolution
- API key rotation procedures
- Response format validation

### Deployment and Rollback strategies:
- Containerized deployment with Docker
- Blue-green deployment strategy
- Health checks for service availability
- Configuration via environment variables

### Feature Flags and compatibility:
- Top-k limits configurable via feature flags
- Response format versioning support
- Compatibility with multiple Qdrant versions

## 7. Risk Analysis and Mitigation

### Top 3 Risks:
1. **Qdrant service availability** - Mitigation: Connection pooling, retry logic, circuit breakers
2. **Cohere API costs** - Mitigation: Query caching, rate limiting, usage monitoring
3. **Performance degradation** - Mitigation: Query optimization, result caching, load balancing

### Blast Radius:
- Query issues affect only individual requests
- Qdrant connectivity issues impact entire service temporarily
- Performance issues affect response times but not functionality

### Kill switches/guardrails:
- Circuit breaker for Qdrant connectivity
- Rate limiting to prevent excessive API usage
- Query length limits to prevent resource exhaustion

## 8. Evaluation and Validation

### Definition of Done:
- Query processing returns accurate top-k results
- Retrieved text matches original stored content
- Metadata fields (URL, chunk_id) are preserved correctly
- JSON responses are properly formatted
- Performance requirements are met

### Output Validation:
- Similarity score validation (>0.7 for relevant results)
- Text content integrity checks
- Metadata completeness validation
- Response structure compliance

## 9. Architectural Decision Record (ADR)

### ADR-001: Use Same Embedding Model for Queries
- **Context**: Need to ensure query embeddings match stored embeddings for accurate retrieval
- **Decision**: Use Cohere embed-multilingual-v3.0 model for queries to match stored vectors
- **Status**: Accepted
- **Consequences**: Ensures consistency but ties query processing to same provider as storage

### ADR-002: Direct Qdrant Integration
- **Context**: Need to perform efficient vector similarity search
- **Decision**: Use Qdrant client library directly for optimal performance
- **Status**: Accepted
- **Consequences**: Tight coupling to Qdrant but maximum efficiency

### ADR-003: JSON Response Format
- **Context**: Need standardized output format for downstream processing
- **Decision**: Use clean JSON with structured fields for results and metadata
- **Status**: Accepted
- **Consequences**: Broad compatibility but larger response sizes than alternatives

## 10. Implementation Phases

### Phase 1: Core Query Functionality
- Implement query embedding generation using Cohere
- Set up Qdrant client connection and configuration
- Create basic vector similarity search functionality
- Implement result ranking by similarity scores

### Phase 2: Result Validation
- Add text content verification between stored and retrieved chunks
- Implement metadata validation (URL, chunk_id matching)
- Add similarity score validation and threshold checking
- Create comprehensive result validation functions

### Phase 3: Response Formatting
- Design clean JSON response structure
- Implement proper error response formatting
- Add performance metrics to responses
- Create response serialization functions

### Phase 4: Testing and Validation
- Create comprehensive test suite for all functionality
- Implement end-to-end testing scenarios
- Add performance benchmarking
- Validate integration with existing pipeline

## 11. Detailed Implementation Plan

### Query Processing Module
- Function to convert text query to embedding vector using Cohere API
- Configuration for Cohere client with proper error handling
- Input validation and sanitization for query text
- Support for optional query parameters (top_k, filters)

### Qdrant Search Module
- Qdrant client initialization with connection pooling
- Vector similarity search implementation using cosine distance
- Result ranking and scoring functionality
- Metadata retrieval and validation

### Result Validation Module
- Text content comparison between stored and retrieved chunks
- Metadata integrity verification (URL, chunk_id, etc.)
- Similarity score validation against thresholds
- Data corruption detection

### Response Formatting Module
- Clean JSON response structure definition
- Error response formatting with appropriate status codes
- Performance metrics inclusion in responses
- Response serialization and validation

### Testing Framework
- Unit tests for individual components
- Integration tests for complete pipeline
- Performance tests for response time validation
- End-to-end tests for complete functionality