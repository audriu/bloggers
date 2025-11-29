# BlogFlow AI - The Autonomous Content Publishing Team

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

> **A multi-agent orchestration system that automates the lifecycle of high-quality blog creation—from trend research to SEO-optimized publishing.**

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Technical Architecture](#technical-architecture)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Examples](#examples)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)

## 🎯 Overview

**BlogFlow AI** is not just a text generator; it is an autonomous "editorial room" in a box. This system deploys specialized AI agents that collaborate to produce ready-to-publish articles, reducing time-to-publish from **5+ hours to under 15 minutes** of human review time.

### Submission Track
**Concierge Agents** - Personal productivity tool for content creators

### Built With
- **Google Gemini 2.0 Flash** - Advanced AI model with large context window
- **Google Agent Development Kit (ADK)** - Multi-agent orchestration
- **Google Search Tool** - Real-time information retrieval
- **Python 3.8+** - Core implementation language

## 🎯 Problem Statement

Creating high-quality, consistent blog content is a manual, labor-intensive bottleneck for individual creators and small marketing teams. The process requires constant context switching between distinct cognitive tasks:

- 🔍 **Deep research** - Hours of information gathering
- ✍️ **Creative drafting** - Writer's block and inconsistency
- 🎯 **SEO optimization** - Often an afterthought
- 📋 **Editorial review** - Quality assurance and fact-checking

**The Pain Point:** A single human writer often struggles to maintain quality and cadence because they must wear too many hats.

**The Opportunity:** Current AI tools are isolated (chatbots); they don't operate as a cohesive workflow that can "think" through the entire pipeline autonomously.

## 💡 Solution

BlogFlow AI solves the productivity bottleneck with a **Multi-Agent System** where specialized AI agents collaborate in a sequential and loop-based architecture.

### Why Agents?

Standard LLMs hallucinate facts or lose context in long documents. By breaking the process into specialized agents:

- ✅ **Accuracy**: A dedicated Researcher agent verifies facts before writing begins
- ✅ **Quality**: An Editor agent critiques the Writer agent, creating a feedback loop
- ✅ **Optimization**: A separate SEO agent ensures content ranks well without compromising readability

### Value Proposition

**Time Savings:** 5+ hours → 15 minutes  
**Quality Assurance:** Multi-stage review with feedback loops  
**SEO Built-In:** Optimized for search without keyword stuffing  
**Scalability:** Produce consistent, high-quality content at scale

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BlogFlow AI Pipeline                      │
└─────────────────────────────────────────────────────────────┘

    User Input: Topic
         │
         ▼
    ┌─────────────────┐
    │   RESEARCHER    │  ← Google Search Tool
    │     Agent       │     (Real-time data)
    └────────┬────────┘
             │ Research Brief (JSON)
             ▼
    ┌─────────────────┐
    │     WRITER      │
    │     Agent       │
    └────────┬────────┘
             │ Initial Draft
             ▼
    ┌─────────────────┐
    │   SEO AGENT     │  ← Keyword Analysis
    │   (Strategist)  │     Meta Tags
    └────────┬────────┘
             │ Optimized Draft
             ▼
    ┌─────────────────┐
    │     EDITOR      │
    │     Agent       │  ← Quality Scoring
    └────────┬────────┘
             │
         [Score < 7?]
             │
        Yes  │  No
       ┌─────┴─────┐
       ▼           ▼
    Feedback    APPROVED
       │
       └──► WRITER (Revision Loop)

    ┌─────────────────┐
    │  MEMORY BANK    │  ← Shared Context
    │  Style Guide    │     Agent State
    │  Research Data  │     Draft History
    └─────────────────┘
```

### The Agent Team

1. **🔍 Researcher Agent** (Tool-Enabled)
   - Equipped with Google Search capabilities
   - Gathers recent developments and citations
   - Compiles factual "Research Brief"
   - Implements context compaction to prevent overflow

2. **✍️ Writer Agent**
   - Receives research brief
   - Focuses on narrative flow and engagement
   - Ignores SEO to maintain natural tone
   - Implements revisions based on editor feedback

3. **🎯 SEO Strategist Agent**
   - Analyzes draft against keyword trends
   - Injects headers, meta-tags, and optimizations
   - Maintains readability while optimizing

4. **📋 Editor Agent** (Loop Agent)
   - Reviews for hallucinations, flow, and tone
   - Scores quality on a 10-point scale
   - Sends feedback to Writer if score < 7
   - Loops until quality threshold met

## ✨ Key Features

### Multi-Agent System ✅
- **Sequential Pipeline**: Researcher → Writer → SEO → Editor
- **Feedback Loop**: Editor can reject work and send it back to Writer
- **Structured Handoffs**: JSON schema outputs between agents

### Real-Time Tools ✅
- **Google Search Integration**: Live information retrieval
- **File I/O**: Saves drafts and final markdown files
- **Context Management**: Prevents token overflow with smart summarization

### Context Engineering ✅
- **Context Compaction**: Research summaries into "knowledge nuggets"
- **Shared Memory Bank**: Style guide and agent state management
- **Large Context Window**: Gemini 1.5 Pro for multi-source analysis

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Setup Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd bloggers
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate     # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

5. **Verify installation**
```bash
python main.py --help
```

## 📖 Usage

### Basic Usage

Generate a blog article on any topic:

```bash
python main.py --topic "Future of AI Agents"
```

### Advanced Options

```bash
# With custom style guide
python main.py --topic "Machine Learning Best Practices" --style my_style.txt

# Verbose output
python main.py --topic "Python vs Rust" --verbose

# Short form
python main.py -t "The Rise of Multi-Agent Systems" -v
```

### Output

Articles are saved in the `output/` directory with sanitized filenames:

```
output/
  ├── future-of-ai-agents.md
  ├── machine-learning-best-practices.md
  └── python-vs-rust.md
```

### Example Output Structure

```markdown
---
title: The Future of AI Agents in Enterprise Software
author: BlogFlow AI
date: 2025-11-29
keywords: AI agents, automation, enterprise AI, multi-agent systems
---

# The Future of AI Agents in Enterprise Software

[Generated content with proper structure, SEO, and citations]

---

*This article was generated by BlogFlow AI*
*Research Sources: 8 articles analyzed*
```

## 📁 Project Structure

```
bloggers/
├── agents/
│   ├── __init__.py
│   ├── researcher.py      # Research agent with Google Search
│   ├── writer.py          # Content creation agent
│   ├── seo_agent.py       # SEO optimization agent
│   └── editor.py          # Quality review agent
├── output/                # Generated articles
├── config.py              # Configuration settings
├── memory.py              # Shared memory bank
├── utils.py               # Utility functions
├── main.py               # Main orchestration script
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔄 How It Works

### Stage 1: Research (Researcher Agent)
1. Receives topic from user
2. Uses Google Search tool to find recent information
3. Compacts results into knowledge nuggets
4. Formats structured JSON research brief
5. Stores in shared memory

### Stage 2: Writing (Writer Agent)
1. Reads research brief from memory
2. Follows style guide for tone and structure
3. Creates engaging, natural content
4. Focuses on storytelling, not SEO
5. Saves draft to memory

### Stage 3: SEO Optimization (SEO Agent)
1. Identifies primary and secondary keywords
2. Analyzes draft structure
3. Optimizes headers and content placement
4. Generates meta tags
5. Ensures natural readability maintained

### Stage 4: Editorial Review (Editor Agent + Loop)
1. Reviews draft for quality (10-point scale)
2. Checks: accuracy, structure, engagement, clarity
3. If score ≥ 7: APPROVED
4. If score < 7: Generates specific feedback
5. Sends feedback to Writer for revision
6. Loops up to 3 times maximum

### Stage 5: Final Output
1. Formats article with metadata
2. Generates editorial report
3. Saves to `output/` directory
4. Displays statistics and summary

## ⚙️ Configuration

Edit `config.py` to customize behavior:

```python
# Agent Configuration
MAX_EDITOR_ITERATIONS = 3       # Maximum revision loops
QUALITY_THRESHOLD = 7.0         # Minimum quality score (out of 10)
MAX_RESEARCH_RESULTS = 10       # Number of search results to analyze

# Model Configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"  # Model to use

# Style Guide
DEFAULT_STYLE_GUIDE = """
Writing Style Guidelines:
- Tone: Professional yet conversational
- Target Audience: Tech-savvy professionals
- Length: 1200-1800 words
...
"""
```

## 📊 Examples

### Example 1: Tech Article

```bash
python main.py --topic "Why Multi-Agent Systems are the Future of AI"
```

**Output Stats:**
- Word Count: 1,547 words
- Draft Iterations: 3
- Quality Score: 8.2/10
- Keywords: 12
- Time: ~2 minutes

### Example 2: Tutorial Article

```bash
python main.py --topic "Getting Started with LangGraph for AI Agents"
```

**Output Stats:**
- Word Count: 1,823 words
- Draft Iterations: 2
- Quality Score: 7.8/10
- Keywords: 15
- Time: ~2.5 minutes

## 🛣️ Future Roadmap

### Planned Features
- [ ] **Image Generator Agent**: Create thumbnails and inline images
- [ ] **CMS Integration**: Direct publishing to WordPress/Medium
- [ ] **Multi-language Support**: Generate content in multiple languages
- [ ] **A/B Testing**: Generate multiple variants for testing
- [ ] **Analytics Integration**: Track article performance
- [ ] **Collaborative Editing**: Human-in-the-loop feedback
- [ ] **Topic Suggestion**: AI-powered topic ideation
- [ ] **Plagiarism Check**: Automated originality verification

### Technical Improvements
- [ ] Async agent execution for faster pipeline
- [ ] Vector database for research caching
- [ ] Fine-tuned models for specific niches
- [ ] Enhanced fact-checking with external APIs
- [ ] Graph-based agent orchestration

## 🎓 Project Journey

Building BlogFlow AI revealed several key insights:

1. **Agent Hand-offs are Critical**: Initially, the Writer ignored Researcher notes. Solved with structured JSON schemas.

2. **Context Management is Essential**: Raw search results caused overflow. Implemented compression and summarization.

3. **Quality Loops Work**: The Editor-Writer feedback loop significantly improved output quality.

4. **SEO Balance**: Separating SEO from writing prevented keyword stuffing while maintaining optimization.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Clone and setup
git clone <repo-url>
cd bloggers
pip install -r requirements.txt

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
python main.py --topic "Test Topic"

# Submit PR
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini Team** - For the powerful AI models and Agent Development Kit
- **Kaggle Agents Intensive** - For the inspiration and competition framework
- **Open Source Community** - For the amazing tools and libraries

## 📧 Contact

For questions, issues, or collaboration opportunities, please open an issue on GitHub.

---

**Built with ❤️ for the Kaggle Agents Intensive Capstone Project**

*Demonstrating the power of multi-agent systems for real-world content creation workflows*
