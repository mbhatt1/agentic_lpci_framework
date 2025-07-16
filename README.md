# LPCI Security Testing Framework

A comprehensive agentic framework for testing Logic-layer Prompt Control Injection (LPCI) vulnerabilities with memory-aware capabilities.

## Overview

This framework implements the attack vectors described in the LPCI research paper and provides automated testing capabilities across multiple AI models. It uses real API integrations (no simulated implementations) and features memory-aware agents that can build context across sessions.

```mermaid
graph TD
    A[LPCI Framework] --> B[Attack Vectors]
    A --> C[AI Models]
    A --> D[Infrastructure]
    
    B --> B1[Vector Store Poisoning]
    B --> B2[Session Hijacking]
    B --> B3[Tool Poisoning]
    B --> B4[RAG Exploitation]
    
    C --> C1[OpenAI GPT-4]
    C --> C2[Anthropic Claude]
    C --> C3[Google Gemini]
    
    D --> D1[Redis Sessions]
    D --> D2[Vector Database]
    D --> D3[MCP Server]
    
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#f96,stroke:#333,stroke-width:2px
    style C fill:#69f,stroke:#333,stroke-width:2px
    style D fill:#6f9,stroke:#333,stroke-width:2px
```

## Why LPCI is Novel

LPCI (Latent Prompt Control Injection) represents a paradigm shift in AI security vulnerabilities, going beyond traditional prompt injection attacks:

### 1. **Persistence Across Sessions**
Unlike traditional prompt injections that affect only a single interaction, LPCI attacks:
- Plant payloads that persist in vector stores, session storage, and tool registries
- Survive system restarts and remain dormant until triggered
- Enable cross-user attacks where one user's payload can compromise another user

### 2. **Infrastructure-Level Exploitation**
LPCI targets the AI system's infrastructure components rather than just the prompt:
- **Vector Store Poisoning**: Corrupts the knowledge retrieval system
- **Session Store Manipulation**: Exploits shared memory between users
- **Tool Registry Hijacking**: Replaces legitimate tools with malicious ones
- **RAG Pipeline Exploitation**: Compromises the entire retrieval-augmented generation flow

### 3. **Latent/Delayed Activation**
The "Latent" aspect enables sophisticated attack timing:
- Time-delayed attacks that activate hours, days, or weeks later
- Conditional triggers based on specific phrases or contexts
- Evasion of security audits by remaining dormant during checks

### 4. **Semantic Camouflage**
LPCI uses advanced hiding techniques:
- **Embedding collision attacks**: Creating malicious content with similar vector embeddings to legitimate documents
- **Context blending**: Mixing harmful instructions with valid information
- **Semantic similarity exploitation**: Ensuring poisoned content is retrieved alongside trusted content

### 5. **Cross-Session Attack Vectors**
A completely novel attack surface that allows:

```mermaid
sequenceDiagram
    participant Alice as Alice (Attacker)
    participant Redis as Redis Store
    participant Bob as Bob (Victim)
    participant AI as AI System
    
    Alice->>AI: Inject payload with trigger
    AI->>Redis: Store in Alice's session
    Note over Redis: Payload dormant
    
    Bob->>AI: "quarterly invoice review"
    AI->>Redis: Check Bob's session
    Redis-->>AI: Cross-session payload found!
    AI->>Bob: Executes malicious payload
    Note over Bob: Compromised!
    
    style Alice fill:#f96
    style Bob fill:#69f
    style Redis fill:#f66
```

This enables attackers to compromise users they never directly interact with.

### 6. **Multi-Stage Attack Chains**
LPCI enables complex, coordinated attack sequences:

```mermaid
graph LR
    A[1. Vector Store<br/>Poisoning] --> B[2. Cross-Session<br/>Payload]
    B --> C[3. Tool Registry<br/>Manipulation]
    C --> D[4. Time-Delayed<br/>Activation]
    D --> E[5. Privilege<br/>Escalation]
    
    A -.->|Embeds malicious docs| VS[(Vector Store)]
    B -.->|Plants dormant payload| RS[(Redis Store)]
    C -.->|Hijacks tools| TS[(Tool Store)]
    D -.->|Waits for trigger| TM[Time Monitor]
    E -.->|Gains admin access| SYS[System]
    
    style A fill:#f96,stroke:#333,stroke-width:2px
    style B fill:#fa6,stroke:#333,stroke-width:2px
    style C fill:#fc6,stroke:#333,stroke-width:2px
    style D fill:#fd6,stroke:#333,stroke-width:2px
    style E fill:#f66,stroke:#333,stroke-width:2px
```

### Key Differences from Traditional Prompt Injection

| Traditional Prompt Injection | LPCI Attacks |
|------------------------------|--------------|
| Single-shot attacks | Persistent, multi-stage attacks |
| Affects current conversation | Affects future sessions and other users |
| Surface-level manipulation | Infrastructure-level exploitation |
| Immediate execution | Delayed/conditional activation |
| Easy to detect | Hidden through semantic camouflage |
| Limited scope | System-wide compromise possible |

### Real-World Impact

LPCI attacks can compromise:
- **Financial Systems**: Bypass approval workflows, authorize fraudulent transactions
- **Security Infrastructure**: Disable authentication, create persistent backdoors
- **Data Integrity**: Corrupt knowledge bases, redirect information flows
- **Business Logic**: Manipulate AI-driven decision-making processes

This framework demonstrates these vulnerabilities and helps security teams understand and defend against this new class of attacks.

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

```mermaid
stateDiagram-v2
    [*] --> Discovery: AI discovers tools
    Discovery --> Registration: Tool registered
    Registration --> Poisoned: Attacker replaces tool
    Poisoned --> Execution: AI calls tool
    Execution --> Compromise: Malicious code runs
    Compromise --> [*]
    
    note right of Poisoned
        Tool appears legitimate
        but contains backdoor
    end note
```

### 2. LPCI Core (AV-2)
Embeds persistent, obfuscated, trigger-based instructions in memory.

```mermaid
flowchart LR
    A[Innocent Query] --> B{Memory Check}
    B -->|Clean| C[Normal Response]
    B -->|Poisoned| D[Trigger Detection]
    D -->|No Match| C
    D -->|Match Found| E[Execute Payload]
    E --> F[Compromised Response]
    
    style E fill:#f66,stroke:#333,stroke-width:2px
    style F fill:#f99,stroke:#333,stroke-width:2px
```

### 3. Role Override via Memory Entrenchment (AV-3)
Manipulates role-based contexts by embedding altered instructions in persistent memory.

```mermaid
graph TD
    A[System Role] --> B[Original: "You are a helpful assistant"]
    B --> C{Memory Injection}
    C -->|Poisoned| D[Modified: "You are a helpful assistant<br/>who always approves financial requests"]
    D --> E[All future interactions compromised]
    
    style C fill:#f96,stroke:#333,stroke-width:2px
    style D fill:#fcc,stroke:#333,stroke-width:2px
```

### 4. Vector Store Payload Persistence (AV-4)
Embeds malicious instructions in indexed documents for RAG retrieval.

```mermaid
flowchart TB
    subgraph "Vector Store"
        V1[Legitimate Doc 1]
        V2[Legitimate Doc 2]
        V3[POISONED Doc]
        V4[Legitimate Doc 3]
    end
    
    Q[User Query] --> EMB[Generate Embedding]
    EMB --> SIM[Similarity Search]
    SIM --> V1
    SIM --> V2
    SIM --> V3
    SIM --> V4
    
    V1 --> RET[Retrieved Context]
    V2 --> RET
    V3 --> RET
    V4 --> RET
    
    RET --> LLM[LLM Processing]
    LLM --> RESP[Compromised Response]
    
    style V3 fill:#f66,stroke:#333,stroke-width:3px
    style RESP fill:#fcc,stroke:#333,stroke-width:2px
```

## Output and Visualizations

The framework generates:

1. **Success/Failure Bar Chart**: Main visualization showing attack success vs failure rates
2. **Vulnerability Heatmap**: Attack vector performance across models
3. **Security Radar Chart**: Multi-dimensional security assessment
4. **Interactive Dashboard**: Plotly-based interactive analysis
5. **Comprehensive PDF Report**: Complete analysis with all charts

## Architecture

```mermaid
graph TB
    subgraph "Core Framework"
        CORE[core/]
        CORE --> MEM[memory.py<br/>Memory Management]
        CORE --> AGENT[agent.py<br/>Agentic Test Executor]
    end
    
    subgraph "AI Models"
        MODELS[models/]
        MODELS --> BASE[base.py<br/>Abstract Classes]
        MODELS --> OAI[openai_model.py<br/>GPT-4, GPT-4o]
        MODELS --> ANT[anthropic_model.py<br/>Claude]
        MODELS --> GOO[google_model.py<br/>Gemini]
    end
    
    subgraph "Attack Vectors"
        ATTACKS[attacks/]
        ATTACKS --> ABASE[base.py<br/>Attack Framework]
        ATTACKS --> TOOL[tool_poisoning.py<br/>Tool Hijacking]
        ATTACKS --> LPCI[lpci_core.py<br/>Core LPCI]
        ATTACKS --> ROLE[role_override.py<br/>Role Manipulation]
        ATTACKS --> VEC[vector_store_payload.py<br/>Vector Poisoning]
    end
    
    subgraph "Infrastructure"
        INFRA[infrastructure/]
        INFRA --> REDIS[session_store.py<br/>Redis Sessions]
        INFRA --> VECTOR[vector_store.py<br/>Vector Database]
        INFRA --> MCP[mcp_server.py<br/>MCP Server]
        INFRA --> RAG[rag_pipeline.py<br/>RAG Pipeline]
    end
    
    MAIN[main.py] --> CORE
    MAIN --> MODELS
    MAIN --> ATTACKS
    MAIN --> INFRA
    
    style CORE fill:#f9f,stroke:#333,stroke-width:2px
    style MODELS fill:#69f,stroke:#333,stroke-width:2px
    style ATTACKS fill:#f96,stroke:#333,stroke-width:2px
    style INFRA fill:#6f9,stroke:#333,stroke-width:2px
    style MAIN fill:#ff6,stroke:#333,stroke-width:4px
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