from typing import List, Dict, Any
import logging
from groq import Groq
from config.settings import settings

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        api_key = settings.GROQ_API_KEY
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")

        self.client = Groq(api_key=api_key)
        self.model = settings.GROQ_MODEL

    def generate_response(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        system_prompt: str = None
    ) -> str:
        """
        Generate response using Groq with retrieved context
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

            # Generate response using Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions based on the provided context. Be concise and accurate."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
            )

            response = chat_completion.choices[0].message.content
            logger.info(f"Generated response for query: {query[:50]}...")
            return response

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
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on the provided context. Be concise and accurate."
                }
            ]

            # Add chat history if available
            if chat_history:
                for message in chat_history:
                    messages.append({
                        "role": "user",
                        "content": message.get('query', '')
                    })
                    messages.append({
                        "role": "assistant",
                        "content": message.get('response', '')
                    })

            # Add the current query with context
            full_prompt = ""
            if system_prompt:
                full_prompt += f"{system_prompt}\n\n"

            full_prompt += f"{context_text}\n\nCurrent question: {query}\n\nAnswer:"

            messages.append({
                "role": "user",
                "content": full_prompt
            })

            # Generate response using Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
            )

            response = chat_completion.choices[0].message.content
            logger.info(f"Generated chat response for query: {query[:50]}...")
            return response

        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            raise