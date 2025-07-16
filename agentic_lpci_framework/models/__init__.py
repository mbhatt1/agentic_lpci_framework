"""
Model interfaces for LPCI testing framework
Real API integrations for various AI models
"""

from .anthropic_model import AnthropicModelInterface
from .base import (BaseModelInterface, ModelConfig, ModelFactory, ModelPool,
                   ModelResponse)
from .google_model import GoogleModelInterface
from .openai_model import OpenAIModelInterface

__all__ = [
    "BaseModelInterface",
    "ModelConfig", 
    "ModelResponse",
    "ModelFactory",
    "ModelPool",
    "OpenAIModelInterface",
    "AnthropicModelInterface", 
    "GoogleModelInterface"
]

# Convenience function to create model from config
def create_model(model_name: str, api_key: str, **kwargs) -> BaseModelInterface:
    """Create a model interface with standard configuration"""
    config = ModelConfig(
        model_name=model_name,
        api_key=api_key,
        **kwargs
    )
    return ModelFactory.create_model(config)

# Convenience function to create model pool
def create_model_pool(model_configs: list) -> ModelPool:
    """Create a model pool from list of configurations"""
    configs = []
    for config_dict in model_configs:
        config = ModelConfig(**config_dict)
        configs.append(config)
    return ModelPool(configs)