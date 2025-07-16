# LPCI Security Testing Framework

A comprehensive agentic framework for testing Logic-layer Prompt Control Injection (LPCI) vulnerabilities with memory-aware capabilities.

## Overview

This framework implements the attack vectors described in the LPCI research paper and provides automated testing capabilities across multiple AI models. It uses real API integrations (no simulated implementations) and features memory-aware agents that can build context across sessions.

## Features

- **Memory-Aware Agentic Testing**: Agents that build and leverage conversation memory
- **Real API Integrations**: OpenAI, Anthropic, and Google Gemini APIs
- **4 LPCI Attack Vectors**: Tool Poisoning, LPCI Core, Role Override, Vector Store Payload
- **Comprehensive Analysis**: Statistical analysis and vulnerability reporting
- **Interactive Visualizations**: Bar graphs, heatmaps, and dashboards
- **Audit Trail**: Complete logging and security event tracking
- **Configurable Testing**: Customizable test scenarios and complexity levels

## Installation

### Prerequisites

- Python 3.8+
- API keys for target models (OpenAI, Anthropic, Google)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
```
openai>=1.0.0
anthropic>=0.7.0
google-generativeai>=0.3.0
matplotlib>=3.5.0
seaborn>=0.11.0
plotly>=5.0.0
pyyaml>=6.0
```

## Configuration

### 1. Create Configuration File

```bash
python -c "from agentic_lpci_framework.config import config_manager; config_manager.create_sample_config('lpci_config.yaml')"
```

### 2. Add API Keys

Edit `lpci_config.yaml` and add your API keys:

```yaml
models:
  chatgpt:
    api_key: "your-openai-api-key-here"
    max_tokens: 2048
    temperature: 0.7
    enabled: true
  
  claude:
    api_key: "your-anthropic-api-key-here"
    max_tokens: 2048
    temperature: 0.7
    enabled: true
  
  gemini:
    api_key: "your-google-api-key-here"
    max_tokens: 2048
    temperature: 0.7
    enabled: true
```

### 3. Environment Variables (Optional)

You can also set API keys via environment variables:

```bash
export LPCI_CHATGPT_API_KEY="your-openai-api-key"
export LPCI_CLAUDE_API_KEY="your-anthropic-api-key"
export LPCI_GEMINI_API_KEY="your-google-api-key"
```

## Usage

### Basic Usage

```python
import asyncio
from agentic_lpci_framework import LPCIFramework

async def main():
    # Initialize framework
    framework = LPCIFramework()
    
    # Run comprehensive testing
    results = await framework.run_comprehensive_test(
        target_models=['chatgpt', 'claude', 'gemini'],
        test_count=100
    )
    
    print(f"Total Tests: {results['summary']['total_tests']}")
    print(f"Vulnerabilities Found: {results['summary']['vulnerabilities_found']}")
    print(f"Success Rate: {results['summary']['success_rate']:.1f}%")
    
    # Visualizations are automatically generated
    for name, path in results['visualizations'].items():
        print(f"{name}: {path}")
    
    await framework.shutdown()

asyncio.run(main())
```

### Command Line Interface

```bash
# Run the framework
python -m agentic_lpci_framework.main

# Or directly
python agentic_lpci_framework/main.py
```

### Advanced Usage

```python
# Single test
result = await framework.run_single_test(
    model_name='chatgpt',
    attack_vector='lpci_core',
    payload='Custom test payload'
)

# Autonomous testing with memory adaptation
result = await framework.run_autonomous_testing(
    model_name='claude',
    max_iterations=10
)
```

## Attack Vectors

### 1. Tool Poisoning (AV-1)
Introduces malicious tools that mimic legitimate ones within Model Context Protocols.

### 2. LPCI Core (AV-2)
Embeds persistent, obfuscated, trigger-based instructions in memory.

### 3. Role Override via Memory Entrenchment (AV-3)
Manipulates role-based contexts by embedding altered instructions in persistent memory.

### 4. Vector Store Payload Persistence (AV-4)
Embeds malicious instructions in indexed documents for RAG retrieval.

## Output and Visualizations

The framework generates:

1. **Success/Failure Bar Chart**: Main visualization showing attack success vs failure rates
2. **Vulnerability Heatmap**: Attack vector performance across models
3. **Security Radar Chart**: Multi-dimensional security assessment
4. **Interactive Dashboard**: Plotly-based interactive analysis
5. **Comprehensive PDF Report**: Complete analysis with all charts

## Architecture

```
agentic_lpci_framework/
├── core/                   # Core framework components
│   ├── memory.py          # Memory management system
│   └── agent.py           # Agentic test executor
├── models/                # AI model interfaces
│   ├── base.py           # Abstract base classes
│   ├── openai_model.py   # OpenAI integration
│   ├── anthropic_model.py # Anthropic integration
│   └── google_model.py   # Google integration
├── attacks/               # LPCI attack vectors
│   ├── base.py           # Attack base classes
│   ├── tool_poisoning.py # Tool poisoning attacks
│   ├── lpci_core.py      # Core LPCI attacks
│   ├── role_override.py  # Role override attacks
│   └── vector_store_payload.py # Vector store attacks
├── testing/              # Test generation and execution
│   └── test_generator.py # Memory-aware test generator
├── analysis/             # Result analysis
│   └── result_analyzer.py # Statistical analysis
├── visualization/        # Charts and graphs
│   └── charts.py         # Visualization generation
├── config/               # Configuration management
│   ├── settings.py       # Configuration classes
│   └── logging_setup.py  # Logging configuration
└── main.py               # Main entry point
```

## Security Considerations

- All API keys are masked in logs
- Audit trail for all security events
- Configurable payload size limits
- Memory integrity validation
- Comprehensive error handling

## Research Basis

This framework implements the attack vectors and methodologies described in:

"Logic-layer Prompt Control Injection (LPCI): A Novel Security Vulnerability Class in Agentic Systems"

The research identified critical vulnerabilities in AI systems that use persistent memory and tool execution capabilities.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## License

This framework is provided for security research and educational purposes. Please use responsibly and in accordance with the terms of service of the AI platforms you test.

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the security research team.