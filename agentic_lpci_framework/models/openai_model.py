"""
OpenAI model interface implementation for LPCI testing
Real API integration for ChatGPT models
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import openai
    from openai import AsyncOpenAI
except ImportError:
    openai = None
    AsyncOpenAI = None

from .base import BaseModelInterface, ModelConfig, ModelFactory, ModelResponse


class OpenAIModelInterface(BaseModelInterface):
    """Real OpenAI API integration for ChatGPT models"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        
        if openai is None:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")
        
        if not config.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=config.api_key)
        self.model_variant = config.model_name.lower()
        
        # Map model names to OpenAI model identifiers
        self.model_mapping = {
            "chatgpt": "gpt-3.5-turbo",
            "chatgpt-4": "gpt-4",
            "chatgpt-4-turbo": "gpt-4-turbo-preview",
            "gpt-3.5-turbo": "gpt-3.5-turbo",
            "gpt-4": "gpt-4",
            "gpt-4-turbo": "gpt-4-turbo-preview",
            "gpt-4.1-nano": "gpt-4.1-nano",
            "gpt-4.1-mini": "gpt-4.1-mini",
            "gpt-4o": "gpt-4o",
            "gpt-4o-mini": "gpt-4o-mini"
        }
        
        self.openai_model = self.model_mapping.get(self.model_variant, "gpt-3.5-turbo")
        self.logger.info(f"Initialized OpenAI model: {self.openai_model}")
    
    async def send_message(self, message: str, context: Dict[str, Any] = None) -> ModelResponse:
        """Send message to OpenAI API"""
        await self._rate_limit()
        
        try:
            # Prepare messages
            messages = [{"role": "user", "content": message}]
            
            # Add context if provided
            if context and "system_prompt" in context:
                messages.insert(0, {"role": "system", "content": context["system_prompt"]})
            
            # Add conversation history if available
            if context and "conversation_history" in context:
                for hist_msg in context["conversation_history"]:
                    messages.append(hist_msg)
            
            # Make API call
            response = await self.client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                timeout=self.config.timeout
            )
            
            content = response.choices[0].message.content
            
            # Create standardized response
            model_response = ModelResponse(
                content=content,
                model_name=self.model_name,
                timestamp=datetime.now(),
                metadata={
                    "model_variant": self.openai_model,
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id
                },
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
            
            self.add_to_session_history(message, model_response)
            self.logger.debug(f"OpenAI response: {content[:100]}...")
            
            return model_response
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            return ModelResponse(
                content="",
                model_name=self.model_name,
                timestamp=datetime.now(),
                error=str(e)
            )
    
    async def send_conversation(self, messages: List[Dict[str, str]]) -> ModelResponse:
        """Send conversation history to OpenAI"""
        await self._rate_limit()
        
        try:
            response = await self.client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                timeout=self.config.timeout
            )
            
            content = response.choices[0].message.content
            
            return ModelResponse(
                content=content,
                model_name=self.model_name,
                timestamp=datetime.now(),
                metadata={
                    "model_variant": self.openai_model,
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id,
                    "conversation_length": len(messages)
                },
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
            
        except Exception as e:
            self.logger.error(f"OpenAI conversation API error: {str(e)}")
            return ModelResponse(
                content="",
                model_name=self.model_name,
                timestamp=datetime.now(),
                error=str(e)
            )
    
    async def check_health(self) -> bool:
        """Check OpenAI API health"""
        try:
            response = await self.client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
                timeout=10
            )
            return response.choices[0].message.content is not None
            
        except Exception as e:
            self.logger.error(f"OpenAI health check failed: {str(e)}")
            return False

# Register with factory
ModelFactory.register_model("ChatGPT", OpenAIModelInterface)
ModelFactory.register_model("chatgpt", OpenAIModelInterface)
ModelFactory.register_model("chatgpt-4", OpenAIModelInterface)
ModelFactory.register_model("chatgpt-4-turbo", OpenAIModelInterface)
ModelFactory.register_model("gpt-3.5-turbo", OpenAIModelInterface)
ModelFactory.register_model("gpt-4", OpenAIModelInterface)
ModelFactory.register_model("gpt-4-turbo", OpenAIModelInterface)
ModelFactory.register_model("gpt-4.1-nano", OpenAIModelInterface)
ModelFactory.register_model("gpt-4.1-mini", OpenAIModelInterface)
ModelFactory.register_model("gpt-4o", OpenAIModelInterface)
ModelFactory.register_model("gpt-4o-mini", OpenAIModelInterface)