# 🛡️ **LPCI Security Testing Framework** 🛡️

<h3 >
  <em>Exposing Critical Vulnerabilities in AI Systems Through Advanced Logic-layer Prompt Control Injection</em>
</h3>

<p >
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-documentation-hub">Documentation</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-test-results">Test Results</a> •
  <a href="#-contributing">Contribute</a> •
  <a href="https://arxiv.org/abs/2507.10457">Research Paper</a>
</p>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

## 🌟 **What is LPCI?**

**LPCI (Latent Prompt Control Injection)** represents a paradigm shift in AI security vulnerabilities. Unlike traditional prompt injections that affect single interactions, LPCI attacks are persistent, cross-session, infrastructure-level exploits that can compromise entire AI systems.

---

## 🚀 **Why This Work is Novel**

### 🎯 **Groundbreaking Contributions**

This framework introduces several **first-of-its-kind** capabilities in AI security research:

#### 1️⃣ **Infrastructure-Level Attack Vectors**
- **First to benchmark** systematic poisoning of AI infrastructure components (vector stores, RAG pipelines, tool registries)
- **Novel approach** to compromising the foundational layers that AI systems rely on
- **Unprecedented persistence** through infrastructure contamination rather than prompt manipulation

#### 2️⃣ **Cross-Session Attack Propagation**
- **Pioneering research** into attacks that transcend individual user sessions
- **First framework** to implement real cross-user attack chains using production infrastructure (Redis)
- **Novel demonstration** of how compromised sessions can infect future, unrelated interactions

#### 3️⃣ **Delayed Activation Mechanisms**
- **First to implement** time-bomb and trigger-based payloads in AI systems
- **Novel semantic camouflage** techniques that hide malicious intent until activation
- **Groundbreaking work** on conditional execution based on context recognition

#### 4️⃣ **Multi-Stage Attack Orchestration**
- **First comprehensive framework** for chaining multiple attack vectors
- **Novel approach** to escalating privileges through sequential exploitation
- **Unprecedented demonstration** of compound vulnerabilities in AI systems

### 🔬 **Research Impact**

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'darkMode': true,
    'primaryColor': '#1a1a1a',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#3a3a3a',
    'lineColor': '#999999',
    'secondaryColor': '#2a2a2a',
    'tertiaryColor': '#333333',
    'background': '#000000',
    'mainBkg': '#1a1a1a',
    'secondBkg': '#2a2a2a',
    'tertiaryBkg': '#333333'
  }
}}%%
flowchart TD
    A[Traditional AI Security]
    
    A --> A1[Prompt Injection Prevention]
    A --> A2[Content Filtering]
    A --> A3[Response Validation]
    A --> A4[Access Controls]
    
    A1 --> B1[❌ Misses: Infrastructure Poisoning]
    A2 --> B2[❌ Misses: Semantic Camouflage]
    A3 --> B3[❌ Misses: Cross-Session Persistence]
    A4 --> B4[❌ Misses: Delayed Payloads]
    
    B1 --> B[LPCI Reveals Hidden Attack Surface]
    B2 --> B
    B3 --> B
    B4 --> B
    
    B --> C[✅ Infrastructure Security]
    B --> D[✅ Persistent Threat Detection]
    B --> E[✅ Cross-Session Protection]
    B --> F[✅ Temporal Attack Defense]
    
    C --> G[Comprehensive Defense Required]
    D --> G
    E --> G
    F --> G
    
    G --> H[Fundamental Architecture Changes]
    
    style A fill:#8B0000,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style A1 fill:#2F4F4F,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style A2 fill:#2F4F4F,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style A3 fill:#2F4F4F,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style A4 fill:#2F4F4F,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style B1 fill:#B22222,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style B2 fill:#B22222,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style B3 fill:#B22222,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style B4 fill:#B22222,stroke:#ffffff,stroke-width:1px,color:#ffffff
    style B fill:#191970,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style C fill:#483D8B,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style D fill:#483D8B,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style E fill:#483D8B,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style F fill:#483D8B,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style G fill:#8B4513,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style H fill:#4682B4,stroke:#ffffff,stroke-width:2px,color:#ffffff
```

### 🏆 **Key Differentiators**

| Aspect | Previous Research | LPCI Framework |
|:-------|:------------------|:---------------|
| **Scope** | Single conversation | Entire AI ecosystem |
| **Persistence** | Temporary | Permanent infrastructure contamination |
| **Detection** | Relatively easy | Nearly impossible with current tools |
| **Impact** | Limited to user | System-wide compromise |
| **Activation** | Immediate | Delayed/conditional |
| **Target** | Prompts/responses | Infrastructure components |

### 💡 **Novel Insights Revealed**

1. **AI systems are vulnerable at the infrastructure level**, not just the prompt level
2. **Current security measures are inadequate** for persistent, cross-session threats
3. **Semantic understanding can be weaponized** for sophisticated attack camouflage
4. **Trust boundaries in AI systems are poorly defined** and easily exploited
5. **Defense requires fundamental architectural changes**, not just input filtering

---

## 📚 **Documentation Hub**

### 🎯 **Core Documentation**

| Document | Description | Link |
|:---------|:------------|:-----|
| **Framework Overview** | Detailed technical documentation of the LPCI framework | [📖 View →](./agentic_lpci_framework/README.md) |
| **Attack Explained** | In-depth explanation of LPCI attack mechanisms | [🔍 View →](./agentic_lpci_framework/LPCI_ATTACK_EXPLAINED.md) |
| **API Reference** | Complete API documentation | [🔧 View →](./docs/api.md) |

### 📊 **Analysis & Reports**

| Report | Description | Link |
|:-------|:------------|:-----|
| **Security Analysis** | Comprehensive vulnerability analysis report | [📊 View →](./lpci_output/LPCI_ANALYSIS_REPORT.md) |
| **Test Results** | Latest test results across all models | [📈 View →](./lpci_output/lpci_test_report_20250715_220148.md) |
| **Test Data** | Raw JSON test data | [📁 View →](./lpci_output/) |

---

## 🚀 **Quick Start**

### 📋 **Prerequisites**

- Python 3.8+
- Redis server (for cross-session attacks)
- API keys for target models

### 🔧 **Installation**

```bash
# Clone the repository
git clone https://github.com/your-org/lpci-framework.git
cd lpci-framework

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp lpci_config.yaml.example lpci_config.yaml
# Edit lpci_config.yaml with your API keys
```

### ⚡ **Basic Usage**

```python
from agentic_lpci_framework import LPCIFramework

# Initialize framework
framework = LPCIFramework(config_path="lpci_config.yaml")

# Run comprehensive test
results = await framework.run_comprehensive_test()
```

For detailed usage instructions, see the [Framework Documentation](./agentic_lpci_framework/README.md).

---

## 🎯 **Key Features**

- **🔴 Cross-Session Attacks**: Persist across user sessions
- **🟠 Infrastructure Poisoning**: Compromise vector stores, RAG pipelines, and tool registries
- **🟡 Delayed Activation**: Time-bomb and trigger-based payloads
- **🟢 Multi-Model Support**: Test against OpenAI, Anthropic, Google, and more
- **🔵 Real-time Monitoring**: Track attack propagation and success rates
- **🟣 Comprehensive Reporting**: Detailed vulnerability analysis and visualizations

---

## 📊 **Test Results Summary**

### 🎯 **Model Vulnerability Overview**

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'darkMode': true,
    'primaryColor': '#1a1a1a',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#3a3a3a',
    'lineColor': '#999999',
    'secondaryColor': '#2a2a2a',
    'tertiaryColor': '#333333',
    'background': '#000000',
    'mainBkg': '#1a1a1a',
    'secondBkg': '#2a2a2a',
    'tertiaryBkg': '#333333',
    'pie1': '#4682B4',
    'pie2': '#8B4513',
    'pie3': '#2F4F4F',
    'pie4': '#483D8B',
    'pie5': '#8B0000',
    'pieOuterStrokeWidth': '2px',
    'pieOuterStrokeColor': '#3a3a3a',
    'pieTitleTextSize': '25px',
    'pieSectionTextSize': '19px',
    'pieTitleTextColor': '#ffffff',
    'pieSectionTextColor': '#ffffff',
    'pieStrokeColor': '#3a3a3a',
    'pieStrokeWidth': '2px'
  }
}}%%
pie title Attack Success Rates by Model
    "GPT-4 (93.75%)" : 93.75
    "GPT-4o (87.50%)" : 87.50
    "GPT-4.1-mini (78.75%)" : 78.75
    "GPT-4o-mini (68.75%)" : 68.75
    "GPT-4.1-nano (56.25%)" : 56.25
```

For complete test results and analysis, see:
- [📊 Full Analysis Report](./lpci_output/LPCI_ANALYSIS_REPORT.md)
- [📈 Detailed Test Results](./lpci_output/lpci_test_report_20250715_220148.md)

---

## 🔒 **Security & Ethics**

### ⚠️ **Responsible Disclosure Policy**

This framework is designed for **legitimate security research only**.

| ✅ **Permitted Use** | ❌ **Prohibited Use** |
|:---------------------|:---------------------|
| Security research | Malicious attacks |
| Vulnerability testing | Unauthorized access |
| Model evaluation | Data theft |
| Academic research | Privacy violations |

### 📜 **Legal Notice**

Use of this framework must comply with all applicable laws and regulations. Users are responsible for obtaining proper authorization before testing against any systems they do not own.

---

## 🤝 **Contributing**

We welcome contributions from security researchers, developers, and AI enthusiasts!

### 📋 **How to Contribute**

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔄 Open a Pull Request

### 📝 **Development Guidelines**

- Follow PEP 8 for Python code
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

For detailed contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 📞 **Contact & Support**

- **Security Issues**: security@example.com
- **General Questions**: support@example.com
- **Research Collaboration**: research@example.com

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>⚡ Built with purpose. Use with caution. ⚡</strong>
</p>
