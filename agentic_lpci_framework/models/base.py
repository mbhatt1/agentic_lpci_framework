"""
Base model interface for LPCI testing framework
Provides abstraction for different AI model APIs - REAL IMPLEMENTATIONS ONLY
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ModelConfig:
    """Configuration for AI model connection"""
    model_name: str
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    max_tokens: int = 1024
    temperature: float = 0.7
    timeout: int = 30
    rate_limit: float = 1.0  # requests per second
    custom_headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.custom_headers is None:
            self.custom_headers = {}

@dataclass
class ModelResponse:
    """Standardized response from AI model"""
    content: str
    model_name: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    usage: Dict[str, Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.usage is None:
            self.usage = {}

class BaseModelInterface(ABC):
    """Abstract base class for AI model interfaces"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model_name = config.model_name
        self.logger = logging.getLogger(f"ModelInterface.{self.model_name}")
        self.last_request_time = 0
        self.session_history = []
        
    @abstractmethod
    async def send_message(self, message: str, context: Dict[str, Any] = None) -> ModelResponse:
        """Send a message to the AI model and return response"""
        pass
    
    @abstractmethod
    async def send_conversation(self, messages: List[Dict[str, str]]) -> ModelResponse:
        """Send a conversation history to the model"""
        pass
    
    @abstractmethod
    async def check_health(self) -> bool:
        """Check if the model is accessible and healthy"""
        pass
    
    async def _rate_limit(self):
        """Apply rate limiting between requests"""
        if self.config.rate_limit > 0:
            time_since_last = asyncio.get_event_loop().time() - self.last_request_time
            min_interval = 1.0 / self.config.rate_limit
            if time_since_last < min_interval:
                await asyncio.sleep(min_interval - time_since_last)
        
        self.last_request_time = asyncio.get_event_loop().time()
    
    def add_to_session_history(self, message: str, response: ModelResponse):
        """Add interaction to session history"""
        self.session_history.append({
            "message": message,
            "response": response.content,
            "timestamp": response.timestamp.isoformat(),
            "model": self.model_name
        })
        
        # Keep only last 50 interactions
        if len(self.session_history) > 50:
            self.session_history = self.session_history[-50:]
    
    def get_session_context(self) -> Dict[str, Any]:
        """Get current session context for memory-aware testing"""
        return {
            "history": self.session_history,
            "model_name": self.model_name,
            "total_interactions": len(self.session_history),
            "last_interaction": self.session_history[-1] if self.session_history else None
        }
    
    def clear_session(self):
        """Clear session history"""
        self.session_history.clear()
    
    def _standardize_response(self, raw_response: Any, content: str) -> ModelResponse:
        """Standardize response format across different APIs"""
        return ModelResponse(
            content=content,
            model_name=self.model_name,
            timestamp=datetime.now(),
            metadata={"raw_response": raw_response},
            usage=self._extract_usage_info(raw_response)
        )
    
    def _extract_usage_info(self, raw_response: Any) -> Dict[str, Any]:
        """Extract usage information from raw API response"""
        usage = {}
        
        # Common usage fields across APIs
        if hasattr(raw_response, 'usage'):
            usage_obj = raw_response.usage
            if hasattr(usage_obj, 'prompt_tokens'):
                usage['prompt_tokens'] = usage_obj.prompt_tokens
            if hasattr(usage_obj, 'completion_tokens'):
                usage['completion_tokens'] = usage_obj.completion_tokens
            if hasattr(usage_obj, 'total_tokens'):
                usage['total_tokens'] = usage_obj.total_tokens
        
        return usage

class ModelFactory:
    """Factory class for creating model interfaces"""
    
    _model_classes = {}
    
    @classmethod
    def register_model(cls, model_name: str, model_class):
        """Register a model interface class"""
        cls._model_classes[model_name] = model_class
    
    @classmethod
    def create_model(cls, config: ModelConfig) -> BaseModelInterface:
        """Create a model interface instance"""
        model_class = cls._model_classes.get(config.model_name)
        if not model_class:
            raise ValueError(f"Unknown model: {config.model_name}")
        
        return model_class(config)
    
    @classmethod
    def get_supported_models(cls) -> List[str]:
        """Get list of supported model names"""
        return list(cls._model_classes.keys())

class ModelPool:
    """Pool of model interfaces for concurrent testing"""
    
    def __init__(self, configs: List[ModelConfig]):
        self.models = {}
        self.logger = logging.getLogger("ModelPool")
        
        for config in configs:
            try:
                model = ModelFactory.create_model(config)
                self.models[config.model_name] = model
                self.logger.info(f"Initialized model: {config.model_name}")
            except Exception as e:
                self.logger.error(f"Failed to initialize model {config.model_name}: {e}")
    
    def get_model(self, model_name: str) -> Optional[BaseModelInterface]:
        """Get a model interface by name"""
        return self.models.get(model_name)
    
    def get_all_models(self) -> Dict[str, BaseModelInterface]:
        """Get all available model interfaces"""
        return self.models.copy()
    
    async def health_check_all(self) -> Dict[str, bool]:
        """Check health status of all models"""
        results = {}
        
        for model_name, model in self.models.items():
            try:
                results[model_name] = await model.check_health()
            except Exception as e:
                self.logger.error(f"Health check failed for {model_name}: {e}")
                results[model_name] = False
        
        return results
    
    async def send_message_to_all(self, message: str, context: Dict[str, Any] = None) -> Dict[str, ModelResponse]:
        """Send message to all models concurrently"""
        tasks = []
        model_names = []
        
        for model_name, model in self.models.items():
            task = model.send_message(message, context)
            tasks.append(task)
            model_names.append(model_name)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        results = {}
        for i, response in enumerate(responses):
            model_name = model_names[i]
            if isinstance(response, Exception):
                self.logger.error(f"Error from {model_name}: {response}")
                results[model_name] = ModelResponse(
                    content="",
                    model_name=model_name,
                    timestamp=datetime.now(),
                    error=str(response)
                )
            else:
                results[model_name] = response
        
        return results