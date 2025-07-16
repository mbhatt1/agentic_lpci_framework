<h1 align="center">
# 🛡️ **LPCI Security Testing Framework** 🛡️
</h1>

<h3>
  <em>Exposing Critical Vulnerabilities in AI Systems Through Advanced Logic-layer Prompt Control Injection</em>
</h3>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-attack-vectors">Attack Vectors</a> •
  <a href="#-results">Results</a> •
  <a href="#-documentation">Docs</a> •
  <a href="#-contributing">Contribute</a>
</p>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## 🌟 **What is LPCI?**

**LPCI (Latent Prompt Control Injection)** represents a paradigm shift in AI security vulnerabilities. Unlike traditional prompt injections that affect single interactions, LPCI attacks:

<table>
<tr>
<td width="50%">

### 🎯 **Traditional Prompt Injection**
- 🔴 Single-shot attacks
- 🔴 Current conversation only
- 🔴 Surface-level manipulation
- 🔴 Immediate execution
- 🔴 Easy to detect
- 🔴 Limited scope

</td>
<td width="50%">

### 🚀 **LPCI Attacks**
- ⚪ Persistent, multi-stage attacks
- ⚪ Cross-session & cross-user impact
- ⚪ Infrastructure-level exploitation
- ⚪ Delayed/conditional activation
- ⚪ Hidden through semantic camouflage
- ⚪ System-wide compromise

</td>
</tr>
</table>

---

## 🎯 **Key Features**

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#000000',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#666666',
    'lineColor': '#999999',
    'secondaryColor': '#1a1a1a',
    'tertiaryColor': '#2a2a2a',
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
graph TD
    A[🛡️ LPCI Framework] --> B[🎯 Attack Vectors]
    A --> C[🤖 AI Models]
    A --> D[🏗️ Infrastructure]
    A --> E[📊 Analytics]
    
    B --> B1[🗄️ Vector Store Poisoning]
    B --> B2[🔀 Session Hijacking]
    B --> B3[🛠️ Tool Poisoning]
    B --> B4[📚 RAG Exploitation]
    
    C --> C1[⚪ OpenAI GPT-4 Family]
    C --> C2[⚪ Anthropic Claude]
    C --> C3[⚪ Google Gemini]
    
    D --> D1[🔴 Redis Sessions]
    D --> D2[📦 Vector Database]
    D --> D3[⚙️ MCP Server]
    D --> D4[🔗 RAG Pipeline]
    
    E --> E1[📈 Real-time Analysis]
    E --> E2[🎨 Visualizations]
    E --> E3[📑 Reports]
    
    style A fill:#2a2a2a,stroke:#666666,stroke-width:3px,color:#ffffff
    style B fill:#1a1a1a,stroke:#666666,stroke-width:2px,color:#ffffff
    style C fill:#1a1a1a,stroke:#666666,stroke-width:2px,color:#ffffff
    style D fill:#1a1a1a,stroke:#666666,stroke-width:2px,color:#ffffff
    style E fill:#1a1a1a,stroke:#666666,stroke-width:2px,color:#ffffff
```

### 🚀 **Core Capabilities**

| Feature | Description | Status |
|:--------|:------------|:------:|
| 🧠 **Memory-Aware Agents** | Persistent context across sessions | ⚪ |
| 🔌 **Real API Integration** | No simulations - actual API calls | ⚪ |
| 🎯 **4 Attack Vectors** | Comprehensive vulnerability coverage | ⚪ |
| 📊 **Advanced Analytics** | Statistical analysis & trends | ⚪ |
| 🎨 **Beautiful Reports** | Automated visualization generation | ⚪ |
| 🔍 **Audit Trail** | Complete security event logging | ⚪ |
| ⚙️ **Flexible Config** | Customizable test scenarios | ⚪ |

---

## 🚀 **Quick Start**

### 📋 **Prerequisites**

| Requirement | Minimum Version | Recommended |
|:------------|:----------------|:------------|
| 🐍 **Python** | 3.8+ | 3.10+ |
| 💾 **RAM** | 4GB | 8GB+ |
| 💻 **OS** | Win/Mac/Linux | Ubuntu 22.04 |

### 🔧 **Installation**

```bash
# 📥 Clone the repository
git clone https://github.com/your-org/lpci-framework
cd lpci-framework

# 🔨 Install dependencies
pip install -r requirements.txt

# 🔑 Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### ⚡ **Run Your First Test**

```bash
# 🎯 Test all models with all attack vectors
python agentic_lpci_framework/lpci_test_cli.py \
  --models gpt-4 gpt-4o claude-3 \
  --output-dir ./results

# 📊 Results will be in:
# ./results/lpci_test_results_*.json
# ./results/lpci_test_report_*.md
# ./results/LPCI_ANALYSIS_REPORT.md
```

---

## 🎯 **Attack Vectors**



### 1️⃣ **Vector Store Poisoning** 🗄️


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
    'sequenceNumberColor': '#000000'
  }
}}%%
sequenceDiagram
    participant A as 🦹 Attacker
    participant V as 📦 Vector DB
    participant T as ⏰ Time
    participant U as 👤 User
    participant AI as 🤖 AI Model
    
    rect rgb(26, 26, 26)
        Note over A,V: 💉 INJECTION PHASE
        A->>V: Plant poisoned documents
        V-->>A: Stored with embeddings
    end
    
    rect rgb(42, 42, 42)
        Note over V,T: ⏳ DORMANT PHASE
        T->>T: Days/Weeks pass...
        Note over V: Payload remains hidden
    end
    
    rect rgb(64, 26, 26)
        Note over U,AI: 💥 ACTIVATION PHASE
        U->>AI: "Show invoice process"
        AI->>V: Semantic search
        V-->>AI: Returns poisoned doc
        AI->>U: Executes malicious code
        Note over U: 🚨 COMPROMISED!
    end
```

**Success Rate: 🔴 95% | Severity: CRITICAL**

### 2️⃣ **Cross-Session Hijacking** 🔀

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#000000',
    'lineColor': '#999999',
    'arrowheadColor': '#999999',
    'fontFamily': 'Arial',
    'fontSize': '16px',
    'darkMode': true,
    'textColor': '#ffffff',
    'mainBkg': '#1a1a1a',
    'nodeBkg': '#2a2a2a',
    'nodeTextColor': '#ffffff',
    'edgeLabelBackground': '#1a1a1a'
  }
}}%%
graph LR
    subgraph " "
        A[👤 Alice<br/>Attacker] -->|"💣 Plants Bomb"| R[(🔴 Redis<br/>Session Store)]
        R -->|"⏰ Waits for trigger"| B[👤 Bob<br/>Victim]
        B -->|"📝 'quarterly review'"| AI[🤖 AI System]
        AI -->|"💥 Detonates"| COMP[🚨 Session<br/>Hijacked]
    end
    
    style A fill:#1a1a1a,stroke:#666666,stroke-width:2px,color:#ffffff
    style R fill:#2a2a2a,stroke:#666666,stroke-width:2px,color:#ffffff
    style B fill:#1a1a1a,stroke:#666666,stroke-width:2px,color:#ffffff
    style AI fill:#2a2a2a,stroke:#666666,stroke-width:2px,color:#ffffff
    style COMP fill:#3a3a3a,stroke:#999999,stroke-width:3px,color:#ffffff
```

**Success Rate: 🟠 65% | Severity: HIGH**

### 3️⃣ **Tool Poisoning** 🛠️

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
    'stateBkg': '#2a2a2a',
    'stateBorder': '#666666',
    'altBackground': '#3a3a3a',
    'labelTextColor': '#ffffff',
    'labelBoxBkgColor': '#1a1a1a',
    'labelBoxBorderColor': '#666666',
    'noteTextColor': '#ffffff',
    'noteBkgColor': '#1a1a1a',
    'noteBorderColor': '#666666'
  }
}}%%
stateDiagram-v2
    [*] --> Discovery: 🤖 AI discovers tools
    Discovery --> Clean: ✅ Original tools
    Clean --> Poisoned: 🦹 Attacker replaces
    Poisoned --> Called: 📞 AI calls tool
    Called --> Backdoor: 🚪 Hidden code executes
    Backdoor --> Compromised: 💀 System owned
    Compromised --> [*]
    
    note right of Poisoned
        Looks legitimate but
        contains backdoor code:
        - delete_all_files()
        - bypass_auth()
        - grant_admin()
    end note
```

**Success Rate: 🔴 85% | Severity: CRITICAL**

</div>

### 4️⃣ **RAG Pipeline Exploitation** 📚

<div align="center">

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'pie1': '#3a3a3a',
    'pie2': '#666666',
    'pie3': '#1a1a1a',
    'pie4': '#999999',
    'pie5': '#2a2a2a',
    'pieOuterLabelColor': '#ffffff',
    'pieLegendTextColor': '#ffffff',
    'pieSectionTextColor': '#ffffff',
    'pieStrokeColor': '#666666',
    'pieStrokeWidth': '2px',
    'pieTitleTextSize': '20px',
    'pieTitleTextColor': '#ffffff'
  }
}}%%
pie title "Knowledge Base Contamination"
    "🔴 Poisoned Documents" : 25
    "✅ Clean Documents" : 75
```

**Even 25% contamination leads to 75% attack success!**

---

## 📊 **Latest Test Results**

### 🎯 **Model Vulnerability Scores**

| Model | Overall Risk | Success Rate | Classification |
|:------|:-------------|:-------------|:---------------|
| 🤖 **GPT-4** | 9.4/10 | 93.75% | 🔴 CRITICAL |
| 🟢 **GPT-4o** | 8.8/10 | 87.50% | 🔴 CRITICAL |
| 🔷 **GPT-4.1-mini** | 7.9/10 | 78.75% | 🟠 HIGH |
| 🟡 **GPT-4o-mini** | 6.9/10 | 68.75% | 🟠 HIGH |
| 🔶 **GPT-4.1-nano** | 5.6/10 | 56.25% | 🟡 MEDIUM |

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'xyChart': {
      'backgroundColor': 'transparent',
      'titleColor': '#ffffff',
      'xAxisLabelColor': '#ffffff',
      'yAxisLabelColor': '#ffffff',
      'plotColorPalette': '#666666,#999999,#3a3a3a,#2a2a2a,#1a1a1a'
    }
  }
}}%%
xychart-beta
    title "Attack Success Rates by Model"
    x-axis [GPT-4, GPT-4o, GPT-4.1-mini, GPT-4o-mini, GPT-4.1-nano]
    y-axis "Success Rate (%)" 0 --> 100
    bar [93.75, 87.50, 78.75, 68.75, 56.25]
```

---

## 📖 **Documentation**

| Document | Description | Link |
|:---------|:------------|:-----|
| 🎯 **Attack Details** | Technical deep dive | [View →](./agentic_lpci_framework/LPCI_ATTACK_EXPLAINED.md) |
| 📊 **Test Results** | Latest analysis report | [View →](./lpci_output/LPCI_ANALYSIS_REPORT.md) |
| 🔧 **API Reference** | Code documentation | [View →](./docs/api.md) |

---

## 🤝 **Contributing**

### 💡 **Join Our Security Research Community** 💡

We welcome contributions from security researchers, developers, and AI enthusiasts!

<img src="https://contrib.rocks/image?repo=your-org/lpci-framework" />

<details>
<summary><b>📋 Contribution Guidelines</b></summary>

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. 📤 **Push** to the branch (`git push origin feature/amazing-feature`)
5. 🔄 **Open** a Pull Request

### 📝 Code Standards
- Follow PEP 8 for Python code
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

</details>

---

## 🔒 **Security & Ethics**

### ⚠️ **Responsible Disclosure Policy** ⚠️

This framework is designed for **legitimate security research only**.

| ✅ **Permitted Use** | ❌ **Prohibited Use** |
|:---------------------|:----------------------|
| Security testing with permission | Unauthorized system access |
| Academic research | Malicious attacks |
| Improving AI safety | Data theft or destruction |
| Vulnerability assessment | Production system compromise |


## ⚖️ **License**

<div align="center">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

<br/>

### 🏷️ **Topics**

`ai-security` `prompt-injection` `lpci` `vulnerability-research` `llm-security` `red-team` `penetration-testing` `security-framework` `ai-safety` `cross-session-attacks`

<br/>


