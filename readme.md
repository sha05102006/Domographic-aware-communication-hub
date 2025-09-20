# 🌍 Demographic-Aware Communication Web-App

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> **Revolutionizing Communication with AI-Powered Demographic Intelligence**

A comprehensive web application that leverages IBM Granite AI to create culturally sensitive, demographically appropriate, and highly effective communications. Transform your messaging to resonate with any audience, from young professionals to senior executives, across different cultures and regions.

---

## 🚀 **Quick Start**

```bash
# Clone the repository
git clone https://github.com/your-username/demographic-communication-app.git
cd demographic-communication-app

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The IBM Granite model will download automatically on first launch (approximately 2-3GB).

---

## 📋 **Table of Contents**

- [Features Overview](#-features-overview)
- [Installation Guide](#-installation-guide)
- [Project Architecture](#-project-architecture)
- [Feature Documentation](#-feature-documentation)
- [Technical Specifications](#-technical-specifications)
- [Usage Examples](#-usage-examples)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ **Features Overview**

### 🎯 **Core Capabilities**

| Feature | Description | Use Cases |
|---------|-------------|-----------|
| **Smart Message Composer** | AI-powered message optimization for specific demographics | Email campaigns, marketing copy, customer communications |
| **Demographic Profiler** | Create and manage detailed audience profiles | Team management, client relationships, targeted messaging |
| **Conversation Optimizer** | Real-time conversation enhancement and suggestions | Customer service, sales calls, internal communications |
| **Analytics Dashboard** | Comprehensive communication pattern analysis | Performance tracking, ROI measurement, trend analysis |
| **Cultural Adaptation Engine** | Cross-cultural message adaptation for global audiences | International business, cultural sensitivity, global campaigns |
| **Message Tone Analyzer** | Deep analysis of tone, sentiment, and communication effectiveness | Quality assurance, brand consistency, professional development |

### 🌟 **Key Benefits**

- **🎯 Precision Targeting**: Tailor messages for specific age groups, cultures, and professional contexts
- **🌍 Cultural Intelligence**: Avoid cultural missteps with built-in regional adaptation
- **📊 Data-Driven Insights**: Track communication effectiveness with detailed analytics
- **🔒 Privacy-First**: Local AI processing ensures data security and privacy
- **⚡ Real-Time Processing**: Instant message optimization and feedback
- **🎨 Modern UI/UX**: Professional, intuitive interface with glassmorphism design

---

## 🛠️ **Installation Guide**

### **Prerequisites**

- Python 3.8 or higher
- 8GB RAM minimum (16GB recommended for optimal performance)
- 5GB free disk space (for model caching)
- Internet connection (for initial model download)

### **Step 1: Environment Setup**

```bash
# Create virtual environment (recommended)
python -m venv demographic-comm-env

# Activate environment
# On Windows:
demographic-comm-env\Scripts\activate
# On macOS/Linux:
source demographic-comm-env/bin/activate
```

### **Step 2: Install Dependencies**

```bash
pip install -r requirements.txt
```

**Dependencies Include:**
```txt
streamlit>=1.28.0
transformers>=4.35.0
torch>=2.0.0
pandas>=2.0.0
plotly>=5.15.0
numpy>=1.24.0
```

### **Step 3: First Launch**

```bash
streamlit run app.py
```

**Note**: The IBM Granite model (2.3GB) will download automatically on first launch. This may take 5-10 minutes depending on your internet connection.

### **Step 4: GPU Acceleration (Optional)**

For faster processing, install CUDA-enabled PyTorch:

```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 🏗️ **Project Architecture**

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)               │
├─────────────────────────────────────────────────────────────┤
│  📝 Message    🎯 Profile    💬 Conversation   📊 Analytics  │
│   Composer      Manager       Optimizer        Dashboard    │
│                                                             │
│  🌐 Cultural   🔍 Tone                                      │
│   Adapter      Analyzer                                     │
├─────────────────────────────────────────────────────────────┤
│              BUSINESS LOGIC LAYER                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Demographics │  │Text Analysis│  │Cultural Data│          │
│  │Processor    │  │Engine       │  │Manager      │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                  AI MODEL LAYER                             │
│              IBM Granite 3.3-2B Instruct                   │
│         ┌─────────────────────────────────────┐             │
│         │  🧠 Model Manager                   │             │
│         │  • Model Loading & Caching         │             │
│         │  • Context Management              │             │
│         │  • Response Generation             │             │
│         └─────────────────────────────────────┘             │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Session State│  │User Profiles│  │Analytics DB │          │
│  │Management   │  │Storage      │  │Storage      │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### **File Structure**

```
demographic-communication-app/
├── 📄 app.py                          # Main application entry point
├── 📄 requirements.txt                # Python dependencies
├── 📁 config/
│   ├── __init__.py
│   └── settings.py                    # Configuration management
├── 📁 src/
│   ├── __init__.py
│   ├── 📁 models/
│   │   ├── __init__.py
│   │   └── granite_model.py           # IBM Granite model handler
│   ├── 📁 utils/
│   │   ├── __init__.py
│   │   ├── text_analyzer.py           # Text analysis utilities
│   │   ├── demographic_processor.py   # Demographic processing
│   │   └── cultural_adapter.py        # Cultural adaptation logic
│   ├── 📁 components/
│   │   ├── __init__.py
│   │   ├── message_composer.py        # Smart message composer
│   │   ├── profile_manager.py         # Demographic profiler
│   │   ├── conversation_optimizer.py  # Conversation optimizer
│   │   ├── analytics_dashboard.py     # Analytics dashboard
│   │   ├── cultural_engine.py         # Cultural adaptation engine
│   │   └── tone_analyzer.py           # Message tone analyzer
│   └── 📁 ui/
│       ├── __init__.py
│       ├── styles.py                  # CSS styles and themes
│       └── layouts.py                 # UI layout components
├── 📁 assets/
│   ├── 📁 images/
│   │   └── logo.png                   # Application logo
│   ├── 📁 css/
│   │   └── custom.css                 # Additional CSS styles
│   └── 📁 data/
│       ├── cultural_data.json         # Cultural adaptation data
│       └── demographic_templates.json # Demographic templates
├── 📁 tests/
│   ├── __init__.py
│   ├── test_granite_model.py          # Model tests
│   ├── test_analyzers.py              # Analyzer tests
│   └── test_components.py             # Component tests
├── 📁 docs/
│   ├── SETUP.md                       # Detailed setup instructions
│   └── API_GUIDE.md                   # API usage guide
├── 📁 .streamlit/
│   └── config.toml                    # Streamlit configuration
├── 📄 .gitignore                      # Git ignore file
└── 📄 LICENSE                         # MIT License
```

---

## 🎯 **Feature Documentation**

### **1. 📝 Smart Message Composer**

**Purpose**: Transform draft messages into demographic-appropriate communications

**Key Functions**:
- Message type selection (Email, Marketing, Support, etc.)
- Multi-demographic targeting
- Tone and complexity adjustment
- Industry-specific adaptation
- Call-to-action integration

**Usage Example**:
```python
# Input: "Hey, can you send me that report?"
# Target: Senior Executive
# Output: "Could you please provide the quarterly report at your earliest convenience?"
```

**Supported Demographics**:
- **Age Groups**: 18-25, 26-40, 40-60, 60+
- **Professions**: Students, Professionals, Executives, Entrepreneurs
- **Industries**: Tech, Healthcare, Finance, Education, Retail
- **Cultural Context**: Urban, Rural, Traditional, Tech-Savvy

### **2. 🎯 Demographic Profiler**

**Purpose**: Create and manage detailed audience profiles for consistent messaging

**Features**:
- Profile creation wizard
- Demographic data management
- Cultural considerations
- Communication preferences
- Profile templates and sharing

**Profile Components**:
```json
{
  "profile_name": "Tech Startup Audience",
  "demographics": {
    "age_group": "26-35",
    "education": "Bachelor's+",
    "profession": "Technology Professional",
    "location": "Urban",
    "tech_savviness": 9,
    "communication_style": "Direct"
  },
  "cultural_notes": "Values innovation, efficiency, data-driven decisions",
  "preferences": {
    "formality": "Casual-Professional",
    "message_length": "Concise",
    "visual_elements": "High"
  }
}
```

### **3. 💬 Conversation Optimizer**

**Purpose**: Real-time conversation enhancement and suggestion engine

**Optimization Types**:
1. **Professional Enhancement**: Increases formality and business appropriateness
2. **Engagement Boost**: Adds compelling language and emotional appeal
3. **Conciseness**: Reduces word count while maintaining meaning
4. **Cultural Sensitivity**: Adapts for cross-cultural communication

**Real-Time Features**:
- Live tone analysis
- Sentiment monitoring
- Readability scoring
- Cultural appropriateness checking

### **4. 📊 Communication Analytics Dashboard**

**Purpose**: Comprehensive analysis of communication patterns and effectiveness

**Metrics Tracked**:
- **Volume Metrics**: Messages sent, demographics targeted, response rates
- **Quality Metrics**: Tone consistency, formality levels, readability scores
- **Engagement Metrics**: Click-through rates, response times, sentiment analysis
- **Cultural Metrics**: Regional adaptation usage, cultural sensitivity scores

**Visualizations**:
- Time-series communication activity
- Demographic distribution pie charts
- Tone analysis radar charts
- Effectiveness heatmaps

**Key Performance Indicators (KPIs)**:
```python
kpis = {
    "total_messages": 1250,
    "unique_demographics": 12,
    "avg_effectiveness_score": 8.7,
    "cultural_adaptations": 340,
    "response_rate_improvement": "+23%",
    "time_saved_per_message": "3.5 minutes"
}
```

### **5. 🌐 Cultural Adaptation Engine**

**Purpose**: Cross-cultural message adaptation for global audiences

**Supported Regions**:
- **North America**: Direct communication, informal tone acceptable
- **Europe**: Moderate formality, structured approach
- **East Asia**: High formality, hierarchical respect
- **South Asia**: Relationship-focused, context-aware
- **Middle East**: Formal, respectful, family-oriented
- **Latin America**: Warm, personal, relationship-building
- **Africa**: Community-focused, respectful, diverse contexts
- **Australia/Oceania**: Casual yet professional, egalitarian

**Cultural Considerations**:
```python
cultural_factors = {
    "communication_style": ["direct", "indirect"],
    "formality_level": [1, 10],
    "hierarchy_importance": ["low", "medium", "high"],
    "time_orientation": ["monochronic", "polychronic"],
    "context_dependency": ["low", "high"],
    "relationship_focus": ["task", "relationship"]
}
```

### **6. 🔍 Message Tone Analyzer**

**Purpose**: Deep analysis of message tone, sentiment, and effectiveness

**Analysis Dimensions**:
- **Formality Analysis**: Scale 1-10, formal/informal indicators
- **Sentiment Analysis**: Positive/negative/neutral with confidence scores
- **Tone Detection**: Professional, casual, friendly, aggressive, etc.
- **Readability Metrics**: Flesch score, grade level, complexity
- **Effectiveness Scoring**: Overall communication effectiveness (1-10)

**Analysis Output Example**:
```python
analysis_result = {
    "formality": {
        "level": "professional",
        "score": 7.8,
        "indicators": ["please", "thank you", "sincerely"]
    },
    "sentiment": {
        "polarity": "positive",
        "score": 0.75,
        "confidence": 0.89
    },
    "readability": {
        "flesch_score": 65.4,
        "grade_level": "High School (9th-12th grade)",
        "complexity": "medium"
    },
    "effectiveness": {
        "overall_score": 8.2,
        "strengths": ["clear structure", "appropriate tone"],
        "improvements": ["add call-to-action", "reduce complexity"]
    }
}
```

---

## 🔧 **Technical Specifications**

### **AI Model Details**

- **Model**: IBM Granite 3.3-2B Instruct
- **Type**: Causal Language Model (Transformer Architecture)
- **Parameters**: 3.3 billion
- **Context Length**: 8,192 tokens
- **Languages**: Multi-language support with English optimization
- **Fine-tuning**: Instruction-tuned for conversational and business communication

### **Performance Specifications**

| Metric | Specification |
|--------|--------------|
| **Model Size** | 2.3GB (FP16) |
| **RAM Usage** | 4-8GB during inference |
| **CPU Processing** | 2-5 seconds per request |
| **GPU Processing** | 0.5-1 second per request |
| **Max Input Length** | 4,096 tokens |
| **Max Output Length** | 1,024 tokens |

### **System Requirements**

**Minimum Requirements**:
- CPU: 4-core processor
- RAM: 8GB
- Storage: 5GB available space
- OS: Windows 10, macOS 10.15, or Linux Ubuntu 18.04+

**Recommended Requirements**:
- CPU: 8-core processor
- RAM: 16GB
- GPU: NVIDIA RTX 3060 or better (optional)
- Storage: 10GB available space (SSD preferred)

---

## 💡 **Usage Examples**

### **Example 1: Marketing Email Optimization**

```python
# Input Message
original_message = """
Hey everyone! Our new product is awesome and you should totally check it out. 
It's got some cool features and it's really affordable. Buy it now!
"""

# Configuration
demographics = ["Professionals (26-40)", "Tech-Savvy"]
message_type = "Marketing Email"
tone = "Professional"
industry = "Technology"

# Optimized Output
optimized_message = """
Subject: Introducing Our Latest Innovation - Enhanced Productivity Solutions

Dear Valued Customer,

We're excited to announce the launch of our newest product, specifically designed 
to address the productivity challenges faced by modern professionals.

Key benefits include:
• Streamlined workflow integration
• Advanced analytics and reporting
• Competitive pricing with exceptional ROI

We invite you to explore how this solution can transform your daily operations.

Schedule a demo: [Call-to-Action Button]

Best regards,
The [Company] Team
"""
```

### **Example 2: Cross-Cultural Adaptation**

```python
# Original Message (US Context)
us_message = "Great job on the quarterly results! The team really knocked it out of the park."

# Japanese Adaptation
japanese_message = "Thank you for your dedicated effort on the quarterly results. 
The team's commitment and attention to detail contributed significantly to our success."

# German Adaptation  
german_message = "The quarterly results demonstrate the team's systematic approach 
and professional execution. Your contributions meet our high standards."
```

### **Example 3: Tone Analysis Results**

```python
message = "I'm really disappointed with the service quality. This needs to be fixed immediately."

analysis = {
    "sentiment": {"polarity": "negative", "score": -0.7, "confidence": 0.92},
    "formality": {"level": "professional", "score": 7.2},
    "urgency": {"level": "high", "indicators": ["immediately", "needs"]},
    "tone": {"primary": "assertive", "secondary": "concerned"},
    "suggestions": [
        "Consider softening the language for better reception",
        "Add specific examples of the service issues",
        "Include a constructive solution or request"
    ]
}
```

---

## 🚀 **API Reference**

### **Core Classes**

#### **GraniteModelManager**
```python
from src.models.granite_model import GraniteModelManager

manager = GraniteModelManager()
manager.load_model()  # Load IBM Granite model

response = manager.generate_response(
    prompt="Your message here",
    demographic_context="Target: Young Professionals",
    max_tokens=200,
    temperature=0.7
)
```

#### **TextAnalyzer**
```python
from src.utils.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
analysis = analyzer.analyze_communication_style("Your message text")

# Returns comprehensive analysis including:
# - Formality level and score
# - Sentiment polarity and confidence  
# - Readability metrics
# - Tone classification
# - Effectiveness recommendations
```

#### **MessageComposer**
```python
from src.components.message_composer import MessageComposer

composer = MessageComposer(model_manager)
composer.render()  # Renders the UI component

# Programmatic usage:
result = composer.optimize_message(
    message="Original message",
    demographics=["Young Adults", "Tech-Savvy"],
    settings={"tone": "Casual", "complexity": "Simple"}
)
```

### **Configuration Options**

```python
# config/settings.py
class AppConfig:
    MODEL_NAME = "ibm-granite/granite-3.3-2b-instruct"
    MAX_NEW_TOKENS = 400
    TEMPERATURE = 0.7
    
    # UI Configuration
    THEME_PRIMARY_COLOR = "#667eea"
    THEME_SECONDARY_COLOR = "#764ba2"
    
    # Cultural regions, demographics, etc.
    CULTURAL_REGIONS = [
        "US/North America", "UK/Europe", "East Asia", 
        "South Asia", "Middle East", "Latin America"
    ]
```

---

## 🧪 **Testing**

### **Run Tests**

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_granite_model.py  # Model tests
python -m pytest tests/test_analyzers.py     # Analysis tests
python -m pytest tests/test_components.py    # UI component tests

# Run with coverage
python -m pytest --cov=src tests/
```

### **Test Categories**

1. **Model Tests**: IBM Granite model loading, inference, error handling
2. **Analyzer Tests**: Text analysis accuracy, edge cases, performance
3. **Component Tests**: UI functionality, user interactions, data flow
4. **Integration Tests**: End-to-end feature testing

---

## 🐛 **Troubleshooting**

### **Common Issues**

**Issue**: Model fails to load
```bash
Error: "Cannot load IBM Granite model"
Solution: Check internet connection and available disk space (5GB required)
```

**Issue**: Out of memory error
```bash
Error: "CUDA out of memory" or "RAM insufficient"
Solution: Reduce batch size or switch to CPU inference
```

**Issue**: Slow performance
```bash
Symptoms: Long response times (>10 seconds)
Solutions: 
- Enable GPU acceleration
- Increase available RAM
- Close other applications
```

**Issue**: Streamlit connection error
```bash
Error: "Address already in use"
Solution: streamlit run app.py --server.port 8502
```

---

## 🔄 **Version History**

### **v1.0.0 (Current)**
- ✅ All 6 core features implemented
- ✅ IBM Granite 3.3-2B integration
- ✅ Modern UI with glassmorphism design
- ✅ Comprehensive analytics dashboard
- ✅ Cross-cultural adaptation engine
- ✅ Real-time tone analysis

### **Planned Features (v1.1.0)**
- 🔄 Email client integration (Outlook, Gmail)
- 🔄 Slack/Teams bot integration
- 🔄 Advanced A/B testing for messages
- 🔄 Multi-language support expansion
- 🔄 API endpoints for third-party integration
- 🔄 Mobile app version

---

## 👥 **Contributing**

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### **Contribution Guidelines**

- Follow PEP 8 Python style guide
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed
- Ensure cross-platform compatibility

### **Development Setup**

```bash
# Clone repository
git clone https://github.com/your-username/demographic-communication-app.git
cd demographic-communication-app

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run development server
streamlit run app.py --server.runOnSave true
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Demographic-Aware Communication Web-App

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 **Acknowledgments**

- **IBM Research** for the Granite AI model
- **Streamlit Team** for the amazing web framework  
- **HuggingFace** for model hosting and transformers library
- **Plotly** for interactive visualization capabilities
- **Open Source Community** for various supporting libraries

---

## 📞 **Support & Contact**

- **Documentation**: [Project Wiki](https://github.com/your-username/demographic-communication-app/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-username/demographic-communication-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/demographic-communication-app/discussions)
- **Email**: support@demographic-comm-app.com

### **Community**

- 💬 **Discord Server**: [Join our community](https://discord.gg/your-invite)
- 🐦 **Twitter**: [@DemographicCommApp](https://twitter.com/DemographicCommApp)
- 💼 **LinkedIn**: [Company Page](https://linkedin.com/company/demographic-comm-app)

---

## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/demographic-communication-app&type=Date)](https://star-history.com/#your-username/demographic-communication-app&Date)

---

**Made with ❤️ for better human communication**

*Transform every message into meaningful connection*