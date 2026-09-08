# RAG Chatbot API

Production-ready Retrieval-Augmented Generation (RAG) Chatbot API that integrates with Qdrant vector database and uses Google Generative AI (Gemini) for response generation.

## Features

- **FastAPI** web framework with async support
- **Qdrant** vector database integration for similarity search
- **Google Generative AI (Gemini)** for response generation
- **Cohere** embeddings (compatible with existing embeddings)
- Production-ready architecture with logging and error handling
- CORS support for web frontend integration
- Configurable via environment variables
- Clean, modular code structure

## Architecture

```
rag_chatbot/
├── api/                    # FastAPI application
│   └── main.py            # Main API endpoints
├── services/              # Business logic
│   ├── rag_service.py     # Main RAG orchestrator
│   ├── qdrant_service.py  # Qdrant interaction
│   ├── embedding_service.py # Embedding generation
│   └── gemini_service.py  # Gemini interaction
├── config/                # Configuration
│   └── settings.py        # Settings and environment variables
├── utils/                 # Utilities
│   └── validation.py      # Input validation
├── requirements.txt       # Dependencies
├── start_server.py        # Startup script
└── README.md              # This file
```

## Requirements

- Python 3.8+
- Google Generative AI API key
- Qdrant vector database (already populated with embeddings)
- Existing Cohere embeddings in Qdrant collection

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with the following variables:
```env
GEMINI_API_KEY=your_google_generative_ai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key (if using cloud)
QDRANT_COLLECTION_NAME=rag_embedding

# Optional configurations
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False
TOP_K=5
MAX_TOKENS=2048
TEMPERATURE=0.7
```

## Usage

### Start the Server

```bash
python start_server.py
```

Or directly with uvicorn:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

#### Health Check
```
GET /
```

#### Chat (RAG Query)
```
POST /chat
```

Request body:
```json
{
  "query": "Your question here",
  "top_k": 5,
  "filters": {},
  "system_prompt": "Optional system prompt"
}
```

#### Chat with History
```
POST /chat-with-history
```

Request body:
```json
{
  "query": "Your question here",
  "chat_history": [
    {"query": "Previous query", "response": "Previous response"}
  ],
  "top_k": 5,
  "filters": {},
  "system_prompt": "Optional system prompt"
}
```

#### Collection Stats
```
GET /stats
```

#### Health Check
```
GET /health
```

## Example Usage

### Python Client
```python
import requests

# Chat endpoint
response = requests.post("http://localhost:8000/chat", json={
    "query": "What is digital twin simulation?",
    "top_k": 3
})

data = response.json()
print(data["response"])
```

### cURL
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain URDF robot structure",
    "top_k": 5
  }'
```

## Configuration

Environment variables (in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | - | Required: Google Generative AI API key |
| `QDRANT_URL` | `http://localhost:6333` | Required: Qdrant instance URL |
| `QDRANT_API_KEY` | - | Qdrant API key (if using cloud) |
| `QDRANT_COLLECTION_NAME` | `rag_embedding` | Qdrant collection name |
| `APP_HOST` | `0.0.0.0` | Server host |
| `APP_PORT` | `8000` | Server port |
| `DEBUG` | `False` | Debug mode |
| `TOP_K` | `5` | Number of top results to retrieve |
| `MAX_TOKENS` | `2048` | Maximum tokens for generation |
| `TEMPERATURE` | `0.7` | Generation temperature |

## Frontend Integration

The API is designed to work with a React frontend. Example integration:

```jsx
const [messages, setMessages] = useState([]);
const [input, setInput] = useState('');

const sendMessage = async () => {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: input })
  });

  const data = await response.json();
  setMessages([...messages, { role: 'user', content: input }]);
  setMessages([...messages, { role: 'assistant', content: data.response }]);
};
```

## Error Handling

The API includes comprehensive error handling:
- Input validation
- Qdrant connection errors
- Gemini API errors
- Proper HTTP status codes
- Detailed error messages

## Security

- Input sanitization
- Environment variable configuration
- CORS middleware (configurable)
- API key management

## Development

For development, run with auto-reload:
```bash
uvicorn api.main:app --reload
```

## Production Deployment

For production deployment, consider:
- Using a process manager like `supervisor` or `systemd`
- Setting `DEBUG=False`
- Using a reverse proxy (nginx)
- SSL termination
- Proper logging configuration