import os
from dotenv import load_dotenv

# Load environment variables from the parent directory
# Try to load from different possible locations
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # If not found, try relative to current directory
    load_dotenv('.env')

class Settings:
    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION", "rag_embedding")

    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("MODEL_NAME", "llama3-8b-8192")

    # Application Configuration
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # RAG Configuration
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
        if not cls.QDRANT_URL:
            raise ValueError("QDRANT_URL environment variable is required")

# Create settings instance
settings = Settings()
settings.validate()