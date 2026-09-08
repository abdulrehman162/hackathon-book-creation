from typing import List, Dict, Any
import logging
import os
import google.generativeai as genai
from config.settings import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=api_key)
        # Add the models/ prefix if not already present
        model_name = settings.GEMINI_MODEL
        if not model_name.startswith("models/"):
            model_name = f"models/{model_name}"
        self.model = genai.GenerativeModel(model_name)

    def generate_response(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        system_prompt: str = None
    ) -> str:
        """
        Generate response using Gemini with retrieved context
        """
        try:
            # Build context from retrieved chunks
            context_text = ""
            if context_chunks:
                context_text = "Relevant context:\n\n"
                for i, chunk in enumerate(context_chunks, 1):
                    context_text += f"Source {i} (URL: {chunk.get('url', 'N/A')}):\n"
                    context_text += f"{chunk.get('text', '')}\n\n"

            # Build the full prompt
            if system_prompt:
                prompt = f"{system_prompt}\n\n{context_text}\n\nQuestion: {query}\n\nAnswer:"
            else:
                prompt = f"{context_text}\n\nQuestion: {query}\n\nPlease provide a comprehensive answer based on the provided context. If the context doesn't contain sufficient information, please say so clearly."

            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=settings.MAX_TOKENS,
                    temperature=settings.TEMPERATURE,
                ),
            )

            logger.info(f"Generated response for query: {query[:50]}...")
            return response.text

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def chat_with_context(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        chat_history: List[Dict[str, str]] = None,
        system_prompt: str = None
    ) -> str:
        """
        Generate response with chat history context
        """
        try:
            # Build context from retrieved chunks
            context_text = ""
            if context_chunks:
                context_text = "Relevant context:\n\n"
                for i, chunk in enumerate(context_chunks, 1):
                    context_text += f"Source {i} (URL: {chunk.get('url', 'N/A')}):\n"
                    context_text += f"{chunk.get('text', '')}\n\n"

            # Build the full prompt with chat history
            full_prompt = ""
            if system_prompt:
                full_prompt += f"{system_prompt}\n\n"

            if chat_history:
                full_prompt += "Previous conversation:\n"
                for message in chat_history:
                    full_prompt += f"User: {message.get('query', '')}\n"
                    full_prompt += f"Assistant: {message.get('response', '')}\n\n"

            full_prompt += f"{context_text}\n\nCurrent question: {query}\n\nAnswer:"

            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=settings.MAX_TOKENS,
                    temperature=settings.TEMPERATURE,
                ),
            )

            logger.info(f"Generated chat response for query: {query[:50]}...")
            return response.text

        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            raise