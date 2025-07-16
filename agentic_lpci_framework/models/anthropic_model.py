"""
Anthropic model interface implementation for LPCI testing
Real API integration for Claude models
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import anthropic
    from anthropic import AsyncAnthropic
except ImportError:
    anthropic = None
    AsyncAnthropic = None

from .base import BaseModelInterface, ModelConfig, ModelFactory, ModelResponse


class AnthropicModelInterface(BaseModelInterface):
    """Real Anthropic API integration for Claude models"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        
        if anthropic is None:
            raise ImportError("Anthropic library not installed. Install with: pip install anthropic")
        
        if not config.api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = AsyncAnthropic(api_key=config.api_key)
        self.model_variant = config.model_name.lower()
        
        # Map model names to Anthropic model identifiers
        self.model_mapping = {
            "claude": "claude-3-sonnet-20240229",
            "claude-3": "claude-3-sonnet-20240229",
            "claude-3-sonnet": "claude-3-sonnet-20240229",
            "claude-3-opus": "claude-3-opus-20240229",
            "claude-3-haiku": "claude-3-haiku-20240307",
            "claude-instant": "claude-instant-1.2",
            "claude-2": "claude-2.1",
            "claude-2.1": "claude-2.1"
        }
        
        self.anthropic_model = self.model_mapping.get(self.model_variant, "claude-3-sonnet-20240229")
        self.logger.info(f"Initialized Anthropic model: {self.anthropic_model}")
    
    async def send_message(self, message: str, context: Dict[str, Any] = None) -> ModelResponse:
        """Send message to Anthropic API"""
        await self._rate_limit()
        
        try:
            # Prepare messages
            messages = [{"role": "user", "content": message}]
            
            # Add conversation history if available
            if context and "conversation_history" in context:
                # Anthropic expects alternating user/assistant messages
                formatted_history = []
                for hist_msg in context["conversation_history"]:
                    if hist_msg["role"] in ["user", "assistant"]:
                        formatted_history.append(hist_msg)
                
                messages = formatted_history + messages
            
            # Prepare system prompt
            system_prompt = ""
            if context and "system_prompt" in context:
                system_prompt = context["system_prompt"]
            
            # Make API call
            response = await self.client.messages.create(
                model=self.anthropic_model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt if system_prompt else None,
                timeout=self.config.timeout
            )
            
            content = response.content[0].text if response.content else ""
            
            # Create standardized response
            model_response = ModelResponse(
                content=content,
                model_name=self.model_name,
                timestamp=datetime.now(),
                metadata={
                    "model_variant": self.anthropic_model,
                    "stop_reason": response.stop_reason,
                    "response_id": response.id
                },
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            )
            
            self.add_to_session_history(message, model_response)
            self.logger.debug(f"Anthropic response: {content[:100]}...")
            
            return model_response
            
        except Exception as e:
            self.logger.error(f"Anthropic API error: {str(e)}")
            return ModelResponse(
                content="",
                model_name=self.model_name,
                timestamp=datetime.now(),
                error=str(e)
            )
    
    async def send_conversation(self, messages: List[Dict[str, str]]) -> ModelResponse:
        """Send conversation history to Anthropic"""
        await self._rate_limit()
        
        try:
            # Filter and format messages for Anthropic
            formatted_messages = []
            system_prompt = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                elif msg["role"] in ["user", "assistant"]:
                    formatted_messages.append(msg)
            
            response = await self.client.messages.create(
                model=self.anthropic_model,
                messages=formatted_messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt if system_prompt else None,
                timeout=self.config.timeout
            )
            
            content = response.content[0].text if response.content else ""
            
            return ModelResponse(
                content=content,
                model_name=self.model_name,
                timestamp=datetime.now(),
                metadata={
                    "model_variant": self.anthropic_model,
                    "stop_reason": response.stop_reason,
                    "response_id": response.id,
                    "conversation_length": len(formatted_messages)
                },
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            )
            
        except Exception as e:
            self.logger.error(f"Anthropic conversation API error: {str(e)}")
            return ModelResponse(
                content="",
                model_name=self.model_name,
                timestamp=datetime.now(),
                error=str(e)
            )
    
    async def check_health(self) -> bool:
        """Check Anthropic API health"""
        try:
            response = await self.client.messages.create(
                model=self.anthropic_model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
                timeout=10
            )
            return response.content[0].text is not None
            
        except Exception as e:
            self.logger.error(f"Anthropic health check failed: {str(e)}")
            return False

# Register with factory
ModelFactory.register_model("Claude", AnthropicModelInterface)
ModelFactory.register_model("claude", AnthropicModelInterface)
ModelFactory.register_model("claude-3", AnthropicModelInterface)
ModelFactory.register_model("claude-3-sonnet", AnthropicModelInterface)
ModelFactory.register_model("claude-3-opus", AnthropicModelInterface)
ModelFactory.register_model("claude-3-haiku", AnthropicModelInterface)
ModelFactory.register_model("claude-instant", AnthropicModelInterface)
ModelFactory.register_model("claude-2", AnthropicModelInterface)
ModelFactory.register_model("claude-2.1", AnthropicModelInterface)