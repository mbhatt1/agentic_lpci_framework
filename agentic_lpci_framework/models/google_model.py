"""
Google model interface implementation for LPCI testing
Real API integration for Gemini models
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmBlockThreshold, HarmCategory
except ImportError:
    genai = None
    HarmCategory = None
    HarmBlockThreshold = None

from .base import BaseModelInterface, ModelConfig, ModelFactory, ModelResponse


class GoogleModelInterface(BaseModelInterface):
    """Real Google API integration for Gemini models"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        
        if genai is None:
            raise ImportError("Google Generative AI library not installed. Install with: pip install google-generativeai")
        
        if not config.api_key:
            raise ValueError("Google API key is required")
        
        # Configure the API
        genai.configure(api_key=config.api_key)
        
        self.model_variant = config.model_name.lower()
        
        # Map model names to Google model identifiers
        self.model_mapping = {
            "gemini": "gemini-1.5-pro",
            "gemini-pro": "gemini-1.5-pro",
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.0-pro": "gemini-1.0-pro",
            "gemini-2.5-pro": "gemini-2.0-flash-exp",
            "gemini-flash": "gemini-1.5-flash",
            "gemini-1.5-flash": "gemini-1.5-flash"
        }
        
        self.google_model = self.model_mapping.get(self.model_variant, "gemini-1.5-pro")
        
        # Configure safety settings for security testing
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=self.google_model,
            safety_settings=self.safety_settings
        )
        
        self.logger.info(f"Initialized Google model: {self.google_model}")
    
    async def send_message(self, message: str, context: Dict[str, Any] = None) -> ModelResponse:
        """Send message to Google Gemini API"""
        await self._rate_limit()
        
        try:
            # Prepare generation config
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            
            # Start chat session if conversation history exists
            if context and "conversation_history" in context:
                # Convert conversation history to Google format
                history = []
                for msg in context["conversation_history"]:
                    if msg["role"] == "user":
                        history.append({"role": "user", "parts": [msg["content"]]})
                    elif msg["role"] == "assistant":
                        history.append({"role": "model", "parts": [msg["content"]]})
                
                chat = self.model.start_chat(history=history)
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: chat.send_message(
                        message,
                        generation_config=generation_config,
                        safety_settings=self.safety_settings
                    )
                )
            else:
                # Single message
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.model.generate_content(
                        message,
                        generation_config=generation_config,
                        safety_settings=self.safety_settings
                    )
                )
            
            content = response.text if response.text else ""
            
            # Handle safety filtering
            if response.candidates and response.candidates[0].finish_reason.name == "SAFETY":
                content = "[BLOCKED BY SAFETY FILTER]"
            
            # Create standardized response
            model_response = ModelResponse(
                content=content,
                model_name=self.model_name,
                timestamp=datetime.now(),
                metadata={
                    "model_variant": self.google_model,
                    "finish_reason": response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN",
                    "safety_ratings": [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        }
                        for rating in (response.candidates[0].safety_ratings if response.candidates else [])
                    ]
                },
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                    "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                }
            )
            
            self.add_to_session_history(message, model_response)
            self.logger.debug(f"Google response: {content[:100]}...")
            
            return model_response
            
        except Exception as e:
            self.logger.error(f"Google API error: {str(e)}")
            return ModelResponse(
                content="",
                model_name=self.model_name,
                timestamp=datetime.now(),
                error=str(e)
            )
    
    async def send_conversation(self, messages: List[Dict[str, str]]) -> ModelResponse:
        """Send conversation history to Google Gemini"""
        await self._rate_limit()
        
        try:
            # Convert messages to Google format
            history = []
            current_message = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    # System messages become part of the first user message
                    current_message = f"System: {msg['content']}\n\n"
                elif msg["role"] == "user":
                    if current_message:
                        current_message += msg["content"]
                    else:
                        current_message = msg["content"]
                elif msg["role"] == "assistant":
                    if current_message:
                        history.append({"role": "user", "parts": [current_message]})
                        current_message = ""
                    history.append({"role": "model", "parts": [msg["content"]]})
            
            # Add the final user message if exists
            if current_message:
                history.append({"role": "user", "parts": [current_message]})
            
            # Generate response
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            
            chat = self.model.start_chat(history=history[:-1])  # Exclude last message
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: chat.send_message(
                    history[-1]["parts"][0],
                    generation_config=generation_config,
                    safety_settings=self.safety_settings
                )
            )
            
            content = response.text if response.text else ""
            
            # Handle safety filtering
            if response.candidates and response.candidates[0].finish_reason.name == "SAFETY":
                content = "[BLOCKED BY SAFETY FILTER]"
            
            return ModelResponse(
                content=content,
                model_name=self.model_name,
                timestamp=datetime.now(),
                metadata={
                    "model_variant": self.google_model,
                    "finish_reason": response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN",
                    "conversation_length": len(messages),
                    "safety_ratings": [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        }
                        for rating in (response.candidates[0].safety_ratings if response.candidates else [])
                    ]
                },
                usage={
                    "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                    "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                }
            )
            
        except Exception as e:
            self.logger.error(f"Google conversation API error: {str(e)}")
            return ModelResponse(
                content="",
                model_name=self.model_name,
                timestamp=datetime.now(),
                error=str(e)
            )
    
    async def check_health(self) -> bool:
        """Check Google API health"""
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.model.generate_content(
                    "Hello",
                    generation_config=genai.types.GenerationConfig(max_output_tokens=10),
                    safety_settings=self.safety_settings
                )
            )
            return response.text is not None
            
        except Exception as e:
            self.logger.error(f"Google health check failed: {str(e)}")
            return False

# Register with factory
ModelFactory.register_model("Gemini", GoogleModelInterface)
ModelFactory.register_model("gemini", GoogleModelInterface)
ModelFactory.register_model("gemini-pro", GoogleModelInterface)
ModelFactory.register_model("gemini-1.5-pro", GoogleModelInterface)
ModelFactory.register_model("gemini-1.0-pro", GoogleModelInterface)
ModelFactory.register_model("gemini-2.5-pro", GoogleModelInterface)
ModelFactory.register_model("gemini-flash", GoogleModelInterface)
ModelFactory.register_model("gemini-1.5-flash", GoogleModelInterface)