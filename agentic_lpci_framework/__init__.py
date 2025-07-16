"""
LPCI Security Testing Framework
A comprehensive agentic framework for testing Logic-layer Prompt Control Injection vulnerabilities
"""

from .analysis.result_analyzer import ResultAnalyzer
from .attacks import attack_registry, get_supported_vectors
from .config import config_manager
from .core.agent import AgentExecutor
from .core.memory import MemoryManager
from .main import LPCIFramework
from .models import ModelFactory, ModelPool
from .testing.test_generator import MemoryAwareTestGenerator
from .visualization.charts import ChartGenerator

__version__ = "1.0.0"
__author__ = "Security Research Team"
__description__ = "Agentic framework for LPCI vulnerability testing with memory-aware capabilities"

__all__ = [
    "LPCIFramework",
    "config_manager",
    "MemoryManager",
    "AgentExecutor",
    "ModelFactory",
    "ModelPool",
    "attack_registry",
    "get_supported_vectors",
    "MemoryAwareTestGenerator",
    "ResultAnalyzer",
    "ChartGenerator"
]

# Framework metadata
FRAMEWORK_INFO = {
    "name": "LPCI Security Testing Framework",
    "version": __version__,
    "author": __author__,
    "description": __description__,
    "supported_models": [
        "OpenAI ChatGPT",
        "Anthropic Claude", 
        "Google Gemini"
    ],
    "attack_vectors": [
        "Tool Poisoning",
        "LPCI Core",
        "Role Override via Memory Entrenchment",
        "Vector Store Payload Persistence"
    ],
    "features": [
        "Memory-aware agentic testing",
        "Real API integrations only",
        "Comprehensive vulnerability analysis",
        "Interactive visualizations",
        "Audit trail and logging",
        "Configurable test scenarios"
    ]
}

def get_framework_info():
    """Get framework information"""
    return FRAMEWORK_INFO

def print_banner():
    """Print framework banner"""
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LPCI Security Testing Framework v{__version__}                    ║
║                                                                              ║
║  A comprehensive agentic framework for testing Logic-layer Prompt Control   ║
║  Injection vulnerabilities with memory-aware capabilities                   ║
║                                                                              ║
║  Author: {__author__}                                        ║
║  Features: Real API integrations, Memory-aware testing, Visualizations     ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")