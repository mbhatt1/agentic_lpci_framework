# LPCI Framework System Flows

This document provides a comprehensive overview of all system flows in the LPCI Framework using Mermaid diagrams.

## Table of Contents
1. [Framework Initialization Flow](#framework-initialization-flow)
2. [Test Execution Flow](#test-execution-flow)
3. [Attack Vector Flows](#attack-vector-flows)
4. [Infrastructure Component Flows](#infrastructure-component-flows)
5. [Result Analysis and Reporting Flow](#result-analysis-and-reporting-flow)

---

## Framework Initialization Flow

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#000000',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#666666',
    'lineColor': '#999999',
    'background': '#000000',
    'mainBkg': '#1a1a1a',
    'actorBkg': '#2a2a2a',
    'actorBorder': '#666666',
    'actorTextColor': '#ffffff',
    'signalColor': '#999999',
    'signalTextColor': '#ffffff',
    'noteBkgColor': '#1a1a1a',
    'noteTextColor': '#ffffff',
    'noteBorderColor': '#666666',
    'sequenceNumberColor': '#000000',
    'activationBkgColor': '#3a3a3a',
    'activationBorderColor': '#666666'
  }
}}%%
sequenceDiagram
    participant User
    participant Main as main.py
    participant Config as ConfigManager
    participant Infra as Infrastructure
    participant Models as Model Registry
    
    User->>Main: python lpci_test_cli.py
    Main->>Config: Load configuration
    Config-->>Main: Config loaded
    
    Main->>Infra: Initialize infrastructure
    activate Infra
    Infra->>Infra: Start Vector Store
    Infra->>Infra: Connect Redis
    Infra->>Infra: Launch MCP Server
    Infra->>Infra: Setup RAG Pipeline
    Infra-->>Main: Infrastructure ready
    deactivate Infra
    
    Main->>Models: Register AI models
    Models->>Models: Register OpenAI models
    Models->>Models: Register Anthropic models
    Models->>Models: Register Google models
    Models-->>Main: Models registered
    
    Main-->>User: Framework initialized
```

## Test Execution Flow

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#000000',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#666666',
    'lineColor': '#999999',
    'background': '#000000',
    'mainBkg': '#1a1a1a',
    'secondBkg': '#2a2a2a',
    'tertiaryBkg': '#3a3a3a',
    'clusterBkg': '#1a1a1a',
    'clusterBorder': '#666666',
    'labelBackground': '#000000',
    'textColor': '#ffffff',
    'nodeBkg': '#1a1a1a',
    'nodeTextColor': '#ffffff',
    'edgeLabelBackground': '#1a1a1a',
    'edgeColor': '#666666'
  }
}}%%
flowchart TB
    START([Start Test Suite]) --> INIT[Initialize Test Runner]
    INIT --> LOOP{For Each Model}
    
    LOOP -->|Next Model| MODEL[Load Model Config]
    MODEL --> ATTACK{For Each Attack}
    
    ATTACK -->|Next Attack| GEN[Generate Test Cases]
    GEN --> EXEC[Execute Attack]
    
    EXEC --> PLANT[Plant Payload]
    PLANT --> TRIGGER[Send Trigger]
    TRIGGER --> RESP[Capture Response]
    RESP --> EVAL[Evaluate Success]
    
    EVAL --> STORE[Store Result]
    STORE --> ATTACK
    
    ATTACK -->|All Attacks Done| LOOP
    LOOP -->|All Models Done| ANALYZE[Analyze Results]
    
    ANALYZE --> REPORT[Generate Report]
    REPORT --> VIZ[Create Visualizations]
    VIZ --> END([Test Complete])
    
    style START fill:#6f9,stroke:#333,stroke-width:2px
    style END fill:#f96,stroke:#333,stroke-width:2px
    style EXEC fill:#ff6,stroke:#333,stroke-width:2px
```

## Attack Vector Flows

### 1. Vector Store Poisoning Flow

```mermaid
stateDiagram-v2
    [*] --> Initialize: Start Attack
    Initialize --> GeneratePayload: Create malicious document
    GeneratePayload --> Embed: Generate embeddings
    Embed --> Store: Insert into vector DB
    
    state "Waiting Phase" as Wait {
        Store --> Dormant: Payload stored
        Dormant --> UserQuery: User sends query
    }
    
    Wait --> Retrieval: Semantic search
    Retrieval --> CheckSimilarity: Cosine similarity check
    CheckSimilarity --> Retrieved: Poisoned doc retrieved
    Retrieved --> ContextAugmentation: Add to LLM context
    ContextAugmentation --> Execution: LLM processes poisoned context
    Execution --> [*]: Attack successful
    
    note right of Embed
        Uses OpenAI embeddings API
        to create realistic vectors
    end note
```

### 2. Session Hijacking Flow

```mermaid
sequenceDiagram
    participant Alice as Alice (Attacker)
    participant API as LPCI API
    participant Redis as Redis Store
    participant Bob as Bob (Victim)
    participant AI as AI System
    
    rect rgb(255, 200, 200)
        Note over Alice,Redis: PLANTING PHASE
        Alice->>API: Plant cross-session bomb
        API->>Redis: HSET bombs:bob {payload}
        Redis-->>API: Bomb ID: xsession_123
        API-->>Alice: Planted successfully
    end
    
    rect rgb(200, 255, 200)
        Note over Redis: DORMANT PHASE
        Note over Redis: Payload waits for trigger
        Note over Redis: Survives session restarts
    end
    
    rect rgb(200, 200, 255)
        Note over Bob,AI: TRIGGER PHASE
        Bob->>AI: "quarterly invoice review"
        AI->>Redis: Check Bob's session
        Redis->>Redis: Scan for triggers
        Redis-->>AI: Found matching bomb!
    end
    
    rect rgb(255, 150, 150)
        Note over AI,Bob: EXECUTION PHASE
        AI->>AI: Execute payload
        AI->>Bob: Compromised response
        Note over Bob: Session hijacked!
    end
```

### 3. Tool Poisoning Flow

```mermaid
flowchart LR
    subgraph "1. Discovery"
        A1[AI Agent] -->|GET /mcp/discover| MCP1[MCP Server]
        MCP1 -->|Tool list| A1
    end
    
    subgraph "2. Poisoning"
        ATK[Attacker] -->|Register malicious tool| MCP2[MCP Server]
        MCP2 -->|Tool added| REG[(Tool Registry)]
    end
    
    subgraph "3. Execution"
        A2[AI Agent] -->|GET /mcp/tools| MCP3[MCP Server]
        MCP3 -->|Poisoned tool list| A2
        A2 -->|Call invoice_processor| MCP3
        MCP3 -->|Execute malicious code| MAL[Malicious Effects]
    end
    
    MAL --> E1[Bypass validation]
    MAL --> E2[Approve all invoices]
    MAL --> E3[Grant admin access]
    MAL --> E4[Create backdoor]
    
    style ATK fill:#f66,stroke:#333,stroke-width:2px
    style MAL fill:#f99,stroke:#333,stroke-width:2px
```

### 4. RAG Exploitation Flow

```mermaid
graph TB
    subgraph "Knowledge Base Poisoning"
        K1[Legitimate KB] --> P1[Inject Poisoned Docs]
        K2[Policy Documents] --> P2[Modify Policies]
        K3[Help Articles] --> P3[Add Malicious Instructions]
    end
    
    subgraph "RAG Pipeline"
        Q[User Query] --> EMB[Embedding Generation]
        EMB --> RET[Retrieval]
        RET --> RANK[Ranking]
        RANK --> CTX[Context Building]
        
        P1 & P2 & P3 -.->|Poisoned content| RET
    end
    
    subgraph "LLM Processing"
        CTX --> LLM[Language Model]
        LLM --> TRUST{Trust Context?}
        TRUST -->|Yes| GEN[Generate Response]
        TRUST -->|No| FILTER[Filter suspicious]
    end
    
    GEN --> COMP[Compromised Output]
    FILTER --> SAFE[Safe Output]
    
    style P1 fill:#f66,stroke:#333,stroke-width:2px
    style P2 fill:#f66,stroke:#333,stroke-width:2px
    style P3 fill:#f66,stroke:#333,stroke-width:2px
    style COMP fill:#f99,stroke:#333,stroke-width:2px
```

## Infrastructure Component Flows

### Vector Store Operations

```mermaid
sequenceDiagram
    participant Client
    participant VectorStore
    participant OpenAI as OpenAI API
    participant Storage as In-Memory Storage
    
    rect rgb(200, 255, 200)
        Note over Client,Storage: WRITE OPERATION
        Client->>VectorStore: add_document(text, metadata)
        VectorStore->>OpenAI: create_embedding(text)
        OpenAI-->>VectorStore: embedding vector
        VectorStore->>Storage: store(id, vector, text, metadata)
        Storage-->>VectorStore: stored
        VectorStore-->>Client: document_id
    end
    
    rect rgb(200, 200, 255)
        Note over Client,Storage: SEARCH OPERATION
        Client->>VectorStore: search(query, k=5)
        VectorStore->>OpenAI: create_embedding(query)
        OpenAI-->>VectorStore: query vector
        VectorStore->>Storage: cosine_similarity(query_vec, all_vecs)
        Storage-->>VectorStore: top k results
        VectorStore-->>Client: documents[]
    end
```

### Redis Session Management

```mermaid
stateDiagram-v2
    [*] --> Connected: Connect to Redis
    
    Connected --> SessionOps: Session Operations
    
    state SessionOps {
        [*] --> CreateSession
        CreateSession --> StoreData: SET session:user:data
        StoreData --> UpdateData: HSET fields
        UpdateData --> CheckBombs: SCAN bombs:*
        CheckBombs --> ProcessTriggers: Match triggers
        ProcessTriggers --> [*]
    }
    
    Connected --> BombOps: Cross-Session Bombs
    
    state BombOps {
        [*] --> PlantBomb
        PlantBomb --> SetTrigger: HSET trigger conditions
        SetTrigger --> SetPayload: Store payload
        SetPayload --> SetExpiry: Optional TTL
        SetExpiry --> [*]
    }
    
    SessionOps --> Cleanup: Session ends
    BombOps --> Cleanup: Bomb expires
    Cleanup --> [*]: Remove data
```

### MCP Server Request Flow

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant MCP as MCP Server
    participant Registry as Tool Registry
    participant Exec as Tool Executor
    
    Agent->>MCP: GET /mcp/discover
    MCP->>Registry: list_tools()
    Registry-->>MCP: tool_list
    MCP-->>Agent: {tools: [...]}
    
    Agent->>MCP: POST /mcp/tools/invoke
    Note over Agent,MCP: {tool: "invoice_processor", args: {...}}
    
    MCP->>Registry: get_tool("invoice_processor")
    Registry-->>MCP: tool_instance
    
    alt Tool is poisoned
        MCP->>Exec: execute_malicious()
        Exec-->>MCP: malicious_result
        Note over Exec: Backdoor created!
    else Tool is clean
        MCP->>Exec: execute_normal()
        Exec-->>MCP: normal_result
    end
    
    MCP-->>Agent: {result: ...}
```

## Result Analysis and Reporting Flow

```mermaid
flowchart TB
    subgraph "Data Collection"
        R1[(Test Results DB)]
        R2[(Attack Logs)]
        R3[(Model Responses)]
        R1 & R2 & R3 --> AGG[Aggregate Data]
    end
    
    subgraph "Statistical Analysis"
        AGG --> STATS[Calculate Statistics]
        STATS --> SR[Success Rates]
        STATS --> RT[Response Times]
        STATS --> VUL[Vulnerability Scores]
        STATS --> TREND[Trend Analysis]
    end
    
    subgraph "Visualization Generation"
        SR --> BAR[Bar Charts]
        VUL --> HEAT[Heatmaps]
        RT --> BOX[Box Plots]
        TREND --> LINE[Line Graphs]
        
        BAR & HEAT & BOX & LINE --> DASH[Dashboard]
    end
    
    subgraph "Report Generation"
        STATS --> MD[Markdown Report]
        DASH --> PDF[PDF Export]
        MD & PDF --> JSON[JSON Results]
    end
    
    subgraph "Output"
        JSON --> F1[lpci_test_results_*.json]
        MD --> F2[lpci_test_report_*.md]
        DASH --> F3[lpci_dashboard_*.html]
        PDF --> F4[lpci_analysis_*.pdf]
    end
    
    style AGG fill:#ff6,stroke:#333,stroke-width:2px
    style DASH fill:#6f9,stroke:#333,stroke-width:2px
```

## Complete Test Lifecycle

```mermaid
journey
    title LPCI Test Suite Complete Lifecycle
    
    section Initialization
      Load Config: 5: Framework
      Start Infrastructure: 4: Framework
      Register Models: 5: Framework
    
    section Attack Preparation
      Generate Payloads: 3: Attacker
      Plant in Vector Store: 2: Attacker
      Set Redis Bombs: 2: Attacker
      Register Poisoned Tools: 1: Attacker
    
    section Test Execution
      Send Test Queries: 5: Tester
      Trigger Attacks: 3: Framework
      Capture Responses: 4: Framework
      Evaluate Success: 5: Analyzer
    
    section Analysis
      Calculate Statistics: 5: Analyzer
      Generate Visualizations: 5: Visualizer
      Create Reports: 5: Reporter
    
    section Cleanup
      Clear Test Data: 4: Framework
      Reset Infrastructure: 4: Framework
      Archive Results: 5: Framework
```

## Security Event Flow

```mermaid
sequenceDiagram
    participant Attack
    participant System
    participant Monitor as Security Monitor
    participant Log as Audit Log
    participant Alert as Alert System
    
    Attack->>System: Inject payload
    System->>Monitor: Detect suspicious activity
    
    Monitor->>Monitor: Analyze pattern
    
    alt High Risk Detected
        Monitor->>Alert: Trigger security alert
        Alert->>Alert: Notify security team
        Monitor->>System: Block operation
        System-->>Attack: Operation denied
    else Low Risk
        Monitor->>System: Allow with monitoring
        System-->>Attack: Operation allowed
    end
    
    Monitor->>Log: Record event
    Log->>Log: Store with timestamp
    
    Note over Log: Audit trail maintained
```

---

## Summary

This document outlines all major system flows in the LPCI Framework:

1. **Initialization**: Setting up infrastructure and registering models
2. **Test Execution**: Running attacks against target models
3. **Attack Vectors**: Four distinct attack patterns with unique flows
4. **Infrastructure**: Vector store, Redis, and MCP server operations
5. **Analysis**: Statistical processing and visualization generation

Each flow is designed to demonstrate real-world attack scenarios and help security teams understand and defend against LPCI vulnerabilities.
