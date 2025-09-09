"""
Local LLM service using Ollama as a drop-in replacement for OpenAI.
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger('phoenix.local_llm')


class LocalLLMService:
    """
    OpenAI-compatible service using Ollama for local LLM inference.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.default_model = "llama3.1:8b"
        
    def chat_completions_create(
        self, 
        model: str = None, 
        messages: List[Dict[str, str]] = None, 
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a chat completion using Ollama.
        
        Args:
            model: Model name (defaults to llama3.1:8b)
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters (ignored for compatibility)
            
        Returns:
            OpenAI-compatible response dictionary
        """
        if model is None:
            model = self.default_model
            
        if messages is None:
            messages = []
            
        try:
            # Convert OpenAI format to Ollama format
            prompt = self._format_messages(messages)
            
            logger.info(f"Generating with Ollama model: {model}")
            logger.debug(f"Prompt: {prompt[:200]}...")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=30  # 30 second timeout
            )
            
            response.raise_for_status()
            ollama_response = response.json()
            
            # Convert Ollama response to OpenAI format
            openai_response = self._format_response(ollama_response)
            
            logger.info(f"Successfully generated response with {len(openai_response['choices'][0]['message']['content'])} characters")
            return openai_response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            raise Exception(f"Local LLM service error: {e}")
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert OpenAI messages format to a single prompt string.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
            else:
                # Unknown role, treat as user message
                prompt_parts.append(f"User: {content}")
        
        # Join with double newlines for better separation
        return "\n\n".join(prompt_parts)
    
    def _format_response(self, ollama_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Ollama response to OpenAI-compatible format.
        
        Args:
            ollama_response: Raw response from Ollama API
            
        Returns:
            OpenAI-compatible response dictionary
        """
        response_text = ollama_response.get("response", "")
        
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": ollama_response.get("prompt_eval_count", 0),
                "completion_tokens": ollama_response.get("eval_count", 0),
                "total_tokens": ollama_response.get("prompt_eval_count", 0) + ollama_response.get("eval_count", 0)
            }
        }
    
    def test_connection(self) -> bool:
        """
        Test if Ollama service is running and accessible.
        
        Returns:
            True if service is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


# Model configurations for different tasks
MODEL_CONFIGS = {
    'orchestrator': {
        'model': 'mistral:7b',  # Faster model
        'temperature': 0.7,
        'max_tokens': 1000  # Reduced tokens
    },
    'worker': {
        'model': 'mistral:7b',
        'temperature': 0.7,
        'max_tokens': 500  # Reduced tokens
    },
    'quality_control': {
        'model': 'mistral:7b',  # Faster model
        'temperature': 0.3,
        'max_tokens': 300  # Reduced tokens
    }
}


def get_llm_service(task_type: str = 'orchestrator') -> LocalLLMService:
    """
    Get a configured LLM service for a specific task type.
    
    Args:
        task_type: Type of task ('orchestrator', 'worker', 'quality_control')
        
    Returns:
        Configured LocalLLMService instance
    """
    service = LocalLLMService()
    
    if task_type in MODEL_CONFIGS:
        config = MODEL_CONFIGS[task_type]
        service.default_model = config['model']
    
    return service
