# Mito - The Powerhouse AI Toolkit

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/C%2B%2B-17-blue.svg" alt="C++">
  <img src="https://img.shields.io/badge/tests-231-brightgreen.svg" alt="Tests">
  <img src="https://img.shields.io/badge/plugins-316-orange.svg" alt="Plugins">
  <img src="https://img.shields.io/badge/modules-36-purple.svg" alt="Modules">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/llama.cpp-integrated-yellow.svg" alt="llama.cpp">
  <img src="https://img.shields.io/badge/FastAPI-server-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/agents-8_types-red.svg" alt="Agents">
</p>

<p align="center">
  <b>Mito</b> is a comprehensive AI toolkit providing a unified interface for LLMs, transformers, vision, speech, and more. Built with Python and C++ for maximum flexibility and performance.
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
- [Python API](#python-api)
- [Module Documentation](#module-documentation)
- [Agent Framework](#agent-framework)
- [API Server](#api-server)
- [Configuration System](#configuration-system)
- [Integration Plugins](#integration-plugins)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Mito is a unified AI toolkit that combines:
- **14 AI modules** for NLP, computer vision, speech processing, and generative AI
- **276 integration plugins** for connecting to external services
- **8 specialized agent types** for autonomous task execution
- **36 core infrastructure modules** for production-ready systems
- **C++ inference engine** with llama.cpp integration for high-performance LLM inference
- **REST API server** with API key auth (`X-API-Key`), optional JWT validation, CORS, metrics, and rate limiting
- **Enterprise-grade features** including authentication, audit logging, resilience patterns, and more

### Design Philosophy

Mito follows these core principles:
1. **Unified Interface**: Single API for all AI capabilities
2. **Production Ready**: Built-in resilience, monitoring, and security
3. **Extensible**: Plugin architecture for unlimited integrations
4. **Performance**: C++ backend for computationally intensive operations
5. **Developer Experience**: Intuitive CLI and comprehensive documentation

---

## 🌟 Key Features

### 🤖 AI/ML Capabilities
- **14 AI Modules**: LLM, NLP, vision, speech, embeddings, sentiment, and more
- **8 LLM Providers**: OpenAI, Anthropic, Mistral, Cohere, Groq, Ollama, Together, Fireworks
- **Vision Models**: Image classification, object detection, segmentation, OCR
- **Speech Processing**: Recognition (Whisper), text-to-speech, emotion detection
- **Embeddings**: Sentence transformers, semantic search, vector stores
- **Generative AI**: Text generation, summarization, translation, question answering

### 🧠 Agent Framework
- **8 Agent Types**: ReAct, Research, Code, Data, Planner, Evaluator, and more
- **Memory Systems**: Short-term and long-term agent memory
- **Tool Registry**: Dynamic tool discovery and execution
- **Multi-Agent Orchestration**: Coordination, consensus, and delegation
- **Streaming Responses**: Real-time token streaming
- **Evaluation Framework**: Performance metrics and leaderboards

### 🔌 Integration Ecosystem
- **276 Pre-built Plugins**: Connect to virtually any service
- **Communication**: GitHub, Slack, Discord, Telegram, Teams, WhatsApp, Matrix, Twilio
- **CRM & Sales**: Salesforce, HubSpot, Intercom, Zendesk, Freshdesk
- **Project Management**: Jira, Linear, Trello, Asana, Notion, Confluence
- **DevOps**: GitLab, Vercel, Sentry, Datadog, PagerDuty, Grafana
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, ClickHouse
- **Vector Databases**: Pinecone, Weaviate, Qdrant, ChromaDB, FAISS
- **Cloud**: AWS (10+ services), GCP (6+ services), Azure (4+ services)
- **AI/ML**: All major AI providers plus specialized services

### 🏗️ Infrastructure
- **Event Bus**: Typed events, middleware, persistence
- **Workflow Engine**: DAG-based execution with retries and parallel steps
- **Scheduler**: Cron, interval, and one-shot tasks with daemon mode
- **Resilience patterns (not enabled in API)**: Circuit breaker, retry, bulkhead, timeout, fallback
- **Configuration System**: Validation, profiles, hot reload, environment overrides
- **Audit Logging**: Immutable logs with integrity checks and compliance features
- **Session Management**: TTL-based storage with multi-backend support
- **Middleware Stack**: CORS, authentication, rate limiting, security headers

### 🔐 Security & Compliance
- **Authentication**: API key via `MITO_API_KEY` (`X-API-Key` header) with optional RS256 JWT validation when `MITO_JWT_PUBLIC_KEY` is set
- **Encryption**: AES, Fernet, bcrypt, argon2, scrypt, PBKDF2
- **Audit Trails**: Immutable logs with integrity verification
- **Rate Limiting**: Configurable request throttling
- **Input Validation**: Email, URL, IP, UUID, JSON schema validation

---

## 🏛️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Mito CLI / Python API                   │
├─────────────────────────────────────────────────────────────┤
│                      AI Modules Layer                        │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ LLM │ │Vision│ │NLP  │ │Embed│ │Speech│ │Sentim│ │OCR  │  │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Infrastructure Layer                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │Event Bus│ │Workflow │ │Scheduler│ │Resilien.│ │Audit   ││
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────────┘│
├─────────────────────────────────────────────────────────────┤
│                      Plugin System                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 316 Integration Plugins (Communication, CRM, DevOps...)││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                      Agent Framework                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │ReAct    │ │Research │ │Code     │ │Data     │ │Planner ││
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────────┘│
├─────────────────────────────────────────────────────────────┤
│                      API Server (FastAPI)                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ REST Endpoints │ Middleware │ API Key (X-API-Key) │ Rate Limit││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                     C++ Inference Engine                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ llama.cpp │ GGUF Models │ High-Performance Inference    ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Component Hierarchy

```
mito/
├── python/               # Python AI modules
│   ├── ai/              # AI/ML implementations
│   │   ├── ocr.py       # Optical Character Recognition
│   │   ├── textgen.py   # Text generation with transformers
│   │   ├── llama.py     # Llama model integration
│   │   ├── sentiment.py # Sentiment and emotion analysis
│   │   ├── embeddings.py# Text embeddings
│   │   ├── speech.py    # Speech recognition (Whisper)
│   │   ├── translate.py # Translation models
│   │   ├── summarize.py # Text summarization
│   │   ├── qa.py        # Question answering
│   │   └── tts.py       # Text-to-speech
│   └── ...
├── agents/              # Agent framework
│   ├── __init__.py      # Core agent classes
│   └── rag.py           # RAG implementation
├── server/              # FastAPI server
│   └── api.py           # REST API endpoints
├── events/              # Event system
├── workflow/            # Workflow engine
├── scheduler/           # Task scheduler
├── resilience/          # Resilience patterns
├── crypto/              # Cryptography utilities
├── config/              # Configuration system
├── audit/               # Audit logging (not exposed via API)
├── plugins/             # Plugin system
├── middleware/           # Server middleware
├── vectorstores/        # Vector search
├── knowledge/           # Knowledge graph
├── sessions/            # Session management
├── data/                # Data storage
├── httpclient/          # HTTP client
├── msgqueue/            # Message queue
├── validators/          # Input validation
├── formatters/          # Output formatting
├── converters/          # Data converters
├── serializers/         # Serialization
├── strings/             # String utilities
├── datetime_utils/      # Date/time utilities
├── parsers/             # Config parsers
├── generators/          # Data generators
├── health/              # Health checks
├── features/            # Feature flags
├── os_swap/             # OS virtualization
├── native/              # Native extensions
├── tests/               # Test suite
└── main.cpp             # C++ CLI engine
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.11+** (recommended)
- **C++ compiler** (g++ or clang++)
- **Git** for cloning repositories
- **pip** for Python package management

### Option 1: Full Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/mito.git
cd mito

# Install Python dependencies
pip install -r requirements.txt

# Build C++ CLI (optional, for llama.cpp support)
make

# Download a Llama model
./scripts/download-model.sh "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf" model.gguf

# Create configuration
python -c "from config import create_default_config; create_default_config()"
```

### Option 2: Python-Only Installation

```bash
# Clone and install Python dependencies only
git clone https://github.com/yourusername/mito.git
cd mito
pip install -r requirements.txt

# Skip C++ compilation
echo "Building Python-only version..."
```

### Option 3: Docker Installation

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y g++ make

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "server.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option 4: Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mito-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mito
  template:
    metadata:
      labels:
        app: mito
    spec:
      containers:
      - name: mito
        image: mito:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2"
        env:
        - name: MITO_API_PORT
          value: "8000"
        - name: MITO_MODEL_LLAMA_MODEL
          value: "/models/model.gguf"
```

### Dependencies

**Core Dependencies:**
- `torch>=2.0.0` - PyTorch for deep learning
- `transformers>=4.30.0` - Hugging Face Transformers
- `numpy>=1.24.0` - Numerical computing
- `llama-cpp-python>=0.1.0` - Llama.cpp Python bindings

**Vision Dependencies:**
- `torchvision>=0.15.0` - Computer vision models
- `pillow>=9.0.0` - Image processing
- `easyocr>=1.7.0` - OCR text recognition

**NLP Dependencies:**
- `sentence-transformers>=2.2.0` - Sentence embeddings

**Server Dependencies:**
- `fastapi>=0.100.0` - Web framework
- `uvicorn>=0.23.0` - ASGI server
- `pydantic>=2.0.0` - Data validation

**Utility Dependencies:**
- `pyyaml>=6.0` - YAML parsing
- `prometheus-client>=0.17.0` - Metrics collection
- `requests>=2.28.0` - HTTP client

---

## 🏃‍♂️ Quick Start

### 1. Using the CLI

```bash
# List available tools
./mito -l

# Chat with a Llama model
./mito chat model.gguf

# Run inference with a specific prompt
./mito llama model.gguf "Explain quantum computing in simple terms"

# Text generation
./mito textgen "The future of AI is"

# Sentiment analysis
./mito sentiment "I love this product! It's amazing!"

# OCR on an image
./mito ocr image.png

# Image classification
./mito classify photo.jpg --top-k 3

# Speech recognition
./mito speech audio.wav

# Text-to-speech
./mito tts "Hello, how are you today?" -o output.wav

# Translation
./mito translate "Hello world" --model Helsinki-NLP/opus-mt-en-es

# Text embeddings
./mito embed "Machine learning is fascinating"

# Summarization
./mito summarize "Long article text here..."

# Question answering
./mito qa "What is Python?" "Python is a programming language..."

# RAG question answering
./mito rag --query "What are the benefits of renewable energy?" --add "Solar power is clean..."

# Run an agent task
./mito agent "Write a Python function to calculate fibonacci numbers"

# Start the API server
./mito server --host 0.0.0.0 --port 8000
```

### 2. Using the C++ CLI

```bash
# Build the C++ CLI
make

# Run interactive chat
./llama-cli -m model.gguf -i

# Run with specific parameters
./llama-cli -m model.gguf -p "Hello, how are you?" -t 8 -c 1024

# Show version and llama.cpp status
./llama-cli -v

# Show help
./llama-cli -h
```

### 3. Using Python API

```python
# Basic AI module usage
from python.ai import TextGenerator, SentimentAnalyzer, Embedder

# Text generation
generator = TextGenerator(model_name="gpt2")
result = generator.generate_single("The weather today is", max_length=50)
print(result)

# Sentiment analysis
analyzer = SentimentAnalyzer()
result = analyzer.analyze("This movie was absolutely fantastic!")
print(f"Sentiment: {result['label']} ({result['score']:.2f})")

# Text embeddings
embedder = Embedder(model_name="sentence-transformers/all-MiniLM-L6-v2")
embedding = embedder.embed("Artificial intelligence is transforming industries")
print(f"Embedding dimension: {len(embedding)}")

# Using the quick functions
from python.ai import quick_sentiment, quick_embed, quick_summarize

sentiment = quick_sentiment("I'm so happy today!")
embedding = quick_embed("Machine learning algorithms")
summary = quick_summarize("Long article text here...")
```

### 4. Using the Agent Framework

```python
from agents import ReActAgent, AgentMemory, ToolRegistry, create_tool

# Define tools
def calculator(expr: str) -> str:
    try:
        return str(eval(expr))
    except:
        return "Error"

def web_search(query: str) -> str:
    return f"Search results for: {query}"

# Create tools
calc_tool = create_tool("calculator", "Calculate math expressions", calculator, ["math"])
search_tool = create_tool("search", "Search the web", web_search, ["web"])

# Create agent with memory and tools
memory = AgentMemory(max_short_term=50, max_long_term=1000)
agent = ReActAgent(
    name="Assistant",
    role="Helpful AI assistant with math and web search capabilities",
    tools=[calc_tool, search_tool],
    memory=memory
)

# Run the agent
result = agent.run("What is 15 * 23 + 7? Also search for recent AI news.")
print(result)

# Get agent metrics
metrics = agent.get_metrics()
print(f"Tasks completed: {metrics['tasks_completed']}")
print(f"Memory entries: {metrics['memory']['total']}")

# Stream responses
for chunk in agent.stream("Explain quantum computing"):
    print(chunk, end="", flush=True)
```

### 5. Starting the API Server

```python
import uvicorn
from server import api

# Start the server
uvicorn.run(api.app, host="0.0.0.0", port=8000)

# Or use the CLI
# ./mito server --host 0.0.0.0 --port 8000
```

### 6. Configuration Example

```yaml
# mito.yaml
version: "1.0.0"
profile: "default"

model:
  default_model: "gpt2"
  llama_model: "models/llama-2-7b-chat.Q4_K_M.gguf"
  llama_ctx: 2048
  llama_threads: 4
  temperature: 0.7
  max_tokens: 256

api:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  cors_origins:
    - "https://app.example.com"
    - "http://localhost:3000"
  api_keys:
    - "sk_live_abc123"
    - "sk_test_xyz789"
  rate_limit: 100
  timeout: 30

storage:
  models_dir: "./models"
  data_dir: "./data"
  cache_dir: "./.cache"
  vector_store_path: "./data/vectorstore.json"
  max_cache_size_mb: 1024

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "./logs/mito.log"
  max_size_mb: 100
  backup_count: 5

observability:
  enable_metrics: true
  metrics_port: 9090
  enable_tracing: false
  trace_sample_rate: 0.1
  health_check_interval: 30
```

---

## 📚 CLI Reference

### Global Options

```bash
./mito -v, --version    # Show version
./mito -l, --list       # List all available tools
./mito -h, --help       # Show help message
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `llama` | Llama LLM inference | `./mito llama model.gguf "Hello"` |
| `ocr` | OCR text recognition | `./mito ocr image.png` |
| `textgen` | Text generation | `./mito textgen "The future is"` |
| `classify` | Image classification | `./mito classify photo.jpg --top-k 5` |
| `sentiment` | Sentiment analysis | `./mito sentiment "I love this!"` |
| `speech` | Speech recognition | `./mito speech audio.wav` |
| `translate` | Translation | `./mito translate "Hello" --model Helsinki-NLP/opus-mt-en-es` |
| `embed` | Text embeddings | `./mito embed "Machine learning"` |
| `summarize` | Text summarization | `./mito summarize "Long text..."` |
| `qa` | Question answering | `./mito qa "What is AI?" "AI is..."` |
| `tts` | Text-to-speech | `./mito tts "Hello" -o speech.wav` |
| `rag` | RAG question answering | `./mito rag --query "?" --add "doc"` |
| `agent` | Agent execution | `./mito agent "Write a function"` |
| `chat` | Interactive chat | `./mito chat model.gguf` |
| `server` | Start API server | `./mito server --port 8000` |

### Command Details

#### Llama Inference
```bash
./mito llama <model> <prompt> [options]
  --tokens <n>    # Max tokens to generate (default: 128)
  --temp <n>      # Temperature (default: 0.7)
  --ctx <n>       # Context size (default: 2048)
  -t, --threads <n> # Number of threads (default: 4)
```

#### OCR
```bash
./mito ocr <image>
  # No additional options
```

#### Image Classification
```bash
./mito classify <image>
  --top-k <n>     # Number of top predictions (default: 5)
```

#### Speech Recognition
```bash
./mito speech <audio>
  --model <name>  # Whisper model size (default: "base")
```

#### Text-to-Speech
```bash
./mito tts <text>
  -o, --output <file>  # Output audio file (default: "speech.wav")
```

#### Translation
```bash
./mito translate <text>
  --model <name>  # Translation model (default: "Helsinki-NLP/opus-mt-en-es")
```

#### RAG
```bash
./mito rag [options]
  --query <text>    # Question to answer
  --add <text>      # Add document (pipe-separated)
  --save <path>     # Save vector store
```

### C++ CLI Options

```bash
./llama-cli [options]
  -m, --model <file>     # Path to GGUF model file (required)
  -p, --prompt <text>    # Input prompt
  -i, --interactive      # Start interactive mode
  -t, --threads <n>      # Number of threads (default: 4)
  -c, --context <n>      # Context size (default: 512)
  --temp <n>             # Temperature (default: 0.7)
  --top-p <n>            # Top-p sampling (default: 0.95)
  --top-k <n>            # Top-k sampling (default: 40)
  --max-tokens <n>       # Max tokens to generate (default: 128)
  -v, --version          # Show version
  -h, --help             # Show help
```

---

## 🐍 Python API

### AI Modules

#### Text Generation
```python
from python.ai import TextGenerator, quick_generate

# Create generator
gen = TextGenerator(model_name="gpt2")

# Generate single completion
result = gen.generate_single("Once upon a time", max_length=100)
print(result)

# Generate multiple completions
results = gen.generate_multiple(
    prompt="The future of technology",
    num_return_sequences=3,
    max_length=50
)

# Quick function
result = quick_generate("Machine learning is", max_length=50)
```

#### Sentiment Analysis
```python
from python.ai import SentimentAnalyzer, EmotionDetector, quick_sentiment, quick_emotion

# Analyze sentiment
analyzer = SentimentAnalyzer()
result = analyzer.analyze("This product is amazing!")
print(f"Label: {result['label']}, Score: {result['score']:.4f}")

# Detect emotions
detector = EmotionDetector()
emotions = detector.detect("I'm so excited about this new opportunity!")
print(f"Primary emotion: {emotions['primary']}")
print(f"Emotions: {emotions['scores']}")

# Quick functions
sentiment = quick_sentiment("I love this!")
emotion = quick_emotion("This is frustrating...")
```

#### Text Embeddings
```python
from python.ai import Embedder, quick_embed

# Create embedder
embedder = Embedder(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Embed single text
embedding = embedder.embed("Artificial intelligence is transforming industries")
print(f"Dimension: {len(embedding)}")

# Batch embeddings
embeddings = embedder.embed_batch([
    "First sentence",
    "Second sentence", 
    "Third sentence"
])

# Similarity
similarity = embedder.similarity("cat", "kitten")
print(f"Similarity: {similarity:.4f}")

# Quick function
embedding = quick_embed("Hello world")
```

#### OCR (Optical Character Recognition)
```python
from python.ai import OCREngine, quick_ocr

# Create OCR engine
engine = OCREngine(languages=['en', 'es'])

# Read text from image
results = engine.read_text("document.png")
for r in results:
    print(f"Text: {r['text']}")
    print(f"Confidence: {r['confidence']:.2%}")
    print(f"Bounding box: {r['bbox']}")

# Quick function
text = quick_ocr("image.jpg")
print(text)
```

#### Image Classification
```python
from python.ai import ImageClassifier, quick_classify

# Create classifier
classifier = ImageClassifier()

# Classify image
results = classifier.classify("photo.jpg", top_k=5)
for r in results:
    print(f"{r['label']}: {r['score']:.4f}")

# Quick function
predictions = quick_classify("image.png")
print(predictions)
```

#### Speech Recognition
```python
from python.ai import SpeechRecognizer, quick_transcribe

# Create recognizer
recognizer = SpeechRecognizer(model_name="base")

# Transcribe audio
text = recognizer.get_text("recording.wav")
print(f"Transcription: {text}")

# With timestamps
result = recognizer.transcribe_with_timestamps("audio.mp3")
for segment in result:
    print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s]: {segment['text']}")

# Quick function
text = quick_transcribe("audio.wav")
```

#### Translation
```python
from python.ai import Translator, quick_translate

# Create translator
translator = Translator(model_name="Helsinki-NLP/opus-mt-en-es")

# Translate text
translated = translator.translate("Hello, how are you?")
print(f"Translation: {translated}")

# Batch translation
translations = translator.translate_batch([
    "Good morning",
    "Thank you",
    "Goodbye"
])

# Quick function
result = quick_translate("Hello world", model="Helsinki-NLP/opus-mt-en-de")
```

#### Summarization
```python
from python.ai import Summarizer, quick_summarize

# Create summarizer
summarizer = Summarizer()

# Summarize text
long_text = "..."  # Long article text
summary = summarizer.summarize(long_text, max_length=130)
print(f"Summary: {summary}")

# Quick function
summary = quick_summarize("Long text to summarize...", max_length=100)
```

#### Question Answering
```python
from python.ai import QAModel, quick_qa

# Create QA model
qa = QAModel()

# Answer question based on context
context = "Python is a high-level programming language. It was created by Guido van Rossum."
result = qa.answer("Who created Python?", context)
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['score']:.4f}")

# Quick function
result = quick_qa("What is machine learning?", "Machine learning is a subset of AI...")
```

#### Text-to-Speech
```python
from python.ai import TTSEngine, quick_speak

# Create TTS engine
tts = TTSEngine()

# Generate speech
output_file = tts.speak("Hello, how are you today?", "output.wav")
print(f"Saved to: {output_file}")

# Quick function
quick_speak("Welcome to Mito!", "welcome.wav")
```

### Agent Framework

#### Basic Agent
```python
from agents import Agent, AgentMemory

# Create agent with memory
memory = AgentMemory(max_short_term=50, max_long_term=1000)
agent = Agent(
    name="Assistant",
    role="Helpful AI assistant",
    memory=memory,
    model="gpt2"
)

# Run agent
result = agent.run("What is the capital of France?")
print(result)

# Get metrics
metrics = agent.get_metrics()
print(f"Tasks completed: {metrics['tasks_completed']}")
print(f"State: {metrics['state']}")

# Stream responses
for chunk in agent.stream("Explain quantum computing"):
    print(chunk, end="", flush=True)
```

#### ReAct Agent with Tools
```python
from agents import ReActAgent, ToolRegistry, create_tool

# Define tools
def calculator(expr: str) -> str:
    try:
        return str(eval(expr))
    except:
        return "Error"

def search(query: str) -> str:
    return f"Search results for: {query}"

# Create tools
tools = [
    create_tool("calculator", "Calculate math expressions", calculator, ["math"]),
    create_tool("search", "Search the web", search, ["web"])
]

# Create agent
agent = ReActAgent(
    name="Assistant",
    role="Helpful assistant with math and web search",
    tools=tools
)

# Run with max iterations
result = agent.run("What is 25 * 16? Also search for latest AI news.", max_iterations=5)
print(result)

# Get tool registry stats
stats = agent.tool_registry.get_stats()
print(f"Total tools: {stats['total_tools']}")
print(f"Total usage: {stats['total_usage']}")
```

#### Research Agent
```python
from agents import ResearchAgent

# Create research agent
agent = ResearchAgent(name="researcher")

# Conduct research
result = agent.research("Quantum Computing", depth=3)
print(f"Topic: {result['topic']}")
print(f"Questions explored: {len(result['questions'])}")
print(f"Findings: {len(result['findings'])}")
print(f"Synthesis: {result['synthesis']}")
```

#### Code Agent
```python
from agents import CodeAgent

# Create code agent
agent = CodeAgent(name="coder")

# Generate code
code = agent.generate("A function to sort a list of dictionaries by a key", language="python")
print(code)

# Review code
issues = agent.review(code, language="python")
for issue in issues:
    print(f"{issue['type']}: {issue['message']}")

# Refactor code
refactored = agent.refactor(code, strategy="extract")
```

#### Multi-Agent System
```python
from agents import MultiAgentSystem, Agent, create_tool

# Create agents
researcher = Agent(name="researcher", role="Research specialist")
coder = Agent(name="coder", role="Code specialist")
planner = Agent(name="planner", role="Strategic planner")

# Create multi-agent system
system = MultiAgentSystem(name="development-team")
system.add_agent(researcher)
system.add_agent(coder)
system.set_coordinator(planner)

# Delegate tasks
result = system.delegate_task("Research Python best practices", "researcher")
print(f"Research result: {result}")

# Broadcast task to all agents
results = system.broadcast_task("What are your specialties?")
for agent_name, result in results.items():
    print(f"{agent_name}: {result}")

# Get system stats
stats = system.get_system_stats()
print(f"Agents: {stats['agents']}")
print(f"Tasks completed: {stats['tasks_completed']}")
```

#### Agent Evaluation
```python
from agents import AgentEvaluator

# Create evaluator
evaluator = AgentEvaluator()

# Evaluate agent performance
result = evaluator.evaluate(
    agent_name="coder",
    task="Write a sorting function",
    result="[Generated code]",
    expected="[Expected code]",
    score=0.85,
    metrics={"correctness": 0.9, "efficiency": 0.8}
)

print(f"Evaluation ID: {result['id']}")
print(f"Score: {result['score']}")
print(f"Passed: {result['passed']}")

# Get agent stats
stats = evaluator.get_agent_stats("coder")
print(f"Average score: {stats['avg_score']:.2f}")
print(f"Pass rate: {stats['pass_rate']:.2%}")

# Get leaderboard
leaderboard = evaluator.get_leaderboard()
for entry in leaderboard:
    print(f"{entry['agent']}: {entry['avg_score']:.2f}")
```

### Infrastructure Modules

#### Event Bus
```python
from events import EventBus, Event, EventPriority

# Create event bus
bus = EventBus(persist_dir="./events")

# Define handlers
def handle_user_login(event: Event):
    print(f"User logged in: {event.data['user_id']}")

def handle_error(event: Event):
    print(f"Error occurred: {event.data['error']}")

# Register handlers
bus.subscribe("user.login", handle_user_login)
bus.subscribe("error", handle_error, priority=10)  # Higher priority

# Publish events
login_event = Event.create(
    event_type="user.login",
    data={"user_id": "alice", "ip": "1.2.3.4"},
    source="auth-service",
    priority=EventPriority.HIGH
)
bus.publish(login_event)

# Get event history
history = bus.get_history(limit=10)
for event in history:
    print(f"{event.type}: {event.data}")
```

#### Configuration System
```python
from config import ConfigManager, ConfigSchema, create_default_schema

# Create config manager
manager = ConfigManager("mito.yaml", schema=create_default_schema())

# Load configuration
config = manager.load()
print(f"API Port: {config.api.port}")
print(f"Model: {config.model.default_model}")

# Validate configuration
errors = manager.validate()
if errors:
    print(f"Validation errors: {errors}")

# Hot reload
manager.on_change(lambda cfg: print("Config changed!"))
manager.start_watching()

# Environment overrides (MITO_API_PORT=9000)
manager.set("api.port", 9000)
port = manager.get("api.port")
print(f"Port from env: {port}")

# Profiles
profiles = manager.get_profiles()
print(f"Available profiles: {profiles}")
manager.load_profile("production")
```

#### Resilience patterns (not enabled in API)
```python
from resilience import (
    CircuitBreaker, Retry, Bulkhead, Timeout, Fallback,
    CircuitBreakerConfig, RetryConfig
)

# Circuit Breaker
config = CircuitBreakerConfig(
    failure_threshold=5,
    recovery_timeout=30.0,
    success_threshold=3
)
breaker = CircuitBreaker("api-service", config)

@breaker
def call_api():
    # API call that might fail
    return requests.get("https://api.example.com")

try:
    result = call_api()
except Exception as e:
    print(f"Circuit open: {e}")

# Retry with exponential backoff
retry_config = RetryConfig(
    max_retries=3,
    backoff_factor=2.0,
    retry_exceptions=(ConnectionError, TimeoutError)
)
retry = Retry(retry_config)

@retry
def unreliable_operation():
    # Operation that might fail
    pass

# Bulkhead (resource isolation)
from resilience import Bulkhead
bulkhead = Bulkhead(name="database", max_concurrent=5, max_wait=10.0)

@bulkhead
def db_query():
    # Database query with limited concurrency
    pass

# Timeout
from resilience import Timeout
timeout = Timeout(seconds=5.0)

@timeout
def slow_operation():
    # Operation that might timeout
    pass

# Fallback
from resilience import Fallback
fallback = Fallback(
    primary=lambda: risky_operation(),
    fallback=lambda: default_value
)
result = fallback.execute()
```

#### Workflow Engine
```python
from workflow import Workflow, StepConfig

# Create workflow
workflow = Workflow(name="data-pipeline")

# Define steps
def extract_data():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

def transform_data(data):
    return [{"user_id": d["id"], "full_name": d["name"]} for d in data]

def load_data(transformed):
    print(f"Loading {len(transformed)} records...")
    return True

# Add steps with dependencies
workflow.add_step(StepConfig(
    name="extract",
    func=extract_data,
    retries=2
))

workflow.add_step(StepConfig(
    name="transform", 
    func=transform_data,
    depends_on=["extract"],
    timeout=30.0
))

workflow.add_step(StepConfig(
    name="load",
    func=load_data,
    depends_on=["transform"],
    retries=3
))

# Execute workflow
result = workflow.run()
print(f"Status: {result['status']}")
print(f"Duration: {result['duration']:.2f}s")

# Get step results
for step_name, step_result in result['steps'].items():
    print(f"{step_name}: {step_result['status']}")
```

#### Scheduler
```python
from scheduler import Scheduler, Task, CronExpression

# Create scheduler
scheduler = Scheduler(daemon=True)

# Define tasks
def daily_report():
    print("Generating daily report...")

def cleanup_temp_files():
    print("Cleaning up temp files...")

# Schedule tasks
scheduler.add_task(Task(
    name="daily-report",
    func=daily_report,
    cron="0 9 * * *",  # 9 AM daily
    enabled=True
))

scheduler.add_task(Task(
    name="hourly-cleanup",
    func=cleanup_temp_files,
    interval=3600,  # Every hour
    enabled=True
))

# Start scheduler
scheduler.start()

# Check scheduler status
status = scheduler.get_status()
print(f"Running: {status['running']}")
print(f"Tasks: {len(status['tasks'])}")

# Stop scheduler
scheduler.stop()
```

#### Audit Logging
```python
from audit import AuditLog, AuditLevel, AuditCategory

# Create audit log
log = AuditLog(log_dir="data/audit", retention_days=90)

# Log events
log.log(
    action="user.login",
    actor="alice",
    resource="auth",
    category=AuditCategory.AUTH,
    level=AuditLevel.INFO,
    ip_address="1.2.3.4",
    user_agent="Mozilla/5.0..."
)

log.log(
    action="data.delete",
    actor="alice",
    resource="users/123",
    category=AuditCategory.DATA,
    level=AuditLevel.WARNING
)

# Query builder
results = (log.query()
    .actor("alice")
    .category(AuditCategory.AUTH)
    .last_hours(24)
    .execute())

for entry in results:
    print(f"{entry.timestamp}: {entry.action} by {entry.actor}")

# Get failures only
failures = log.query().failures_only().last_days(7).execute()

# Get security events
security = log.get_security_events(hours=24)

# Export
json_str = log.export_json()
csv_str = log.export_csv()

# Verify integrity
result = log.verify_integrity()
print(f"Integrity rate: {result['integrity_rate']:.2%}")

# Get statistics
stats = log.get_stats()
print(f"Total entries: {stats['total']}")
print(f"By level: {stats['by_level']}")
```

#### Vector Stores
```python
from vectorstores import InMemoryVectorStore, FAISSVectorStore

# In-memory vector store
store = InMemoryVectorStore()

# Add documents
documents = [
    {"text": "Machine learning is a subset of AI", "metadata": {"source": "ml-book"}},
    {"text": "Deep learning uses neural networks", "metadata": {"source": "dl-paper"}},
    {"text": "Natural language processing analyzes text", "metadata": {"source": "nlp-tutorial"}}
]

for doc in documents:
    store.add(doc["text"], doc["metadata"])

# Search
results = store.search("What is machine learning?", top_k=2)
for result in results:
    print(f"Score: {result['score']:.4f}")
    print(f"Text: {result['text']}")
    print(f"Metadata: {result['metadata']}")
    print()

# FAISS-backed store (for large datasets)
faiss_store = FAISSVectorStore(dimension=384)
faiss_store.add(["doc1", "doc2", "doc3"])
results = faiss_store.search("query", top_k=2)
```

#### Knowledge Graph
```python
from knowledge import KnowledgeGraph, Entity, Relation

# Create knowledge graph
kg = KnowledgeGraph()

# Add entities
kg.add_entity(Entity(id="e1", type="person", name="Alice", properties={"age": 30}))
kg.add_entity(Entity(id="e2", type="org", name="Acme Corp", properties={"industry": "tech"}))
kg.add_entity(Entity(id="e3", type="product", name="Widget"))

# Add relations
kg.add_relation(Relation(source="e1", target="e2", type="works_at", properties={"since": 2020}))
kg.add_relation(Relation(source="e2", target="e3", type="produces"))

# Query
results = kg.query(entity_type="person", relation_type="works_at")
for entity in results:
    print(f"{entity.name} ({entity.type})")

# Get neighbors
neighbors = kg.get_neighbors("e1", depth=2)
print(f"Neighbors of Alice: {[n.name for n in neighbors]}")

# Find path
paths = kg.find_path("e1", "e3")
for path in paths:
    print(f"Path: {' -> '.join([node.name for node in path])}")
```

#### Session Management
```python
from sessions import SessionManager, MemoryBackend, FileBackend

# Create session manager with memory backend
manager = SessionManager(backend=MemoryBackend(ttl=3600))

# Create session
session_id = manager.create_session(user_id="alice", data={"role": "admin"})
print(f"Session ID: {session_id}")

# Get session
session = manager.get_session(session_id)
if session:
    print(f"User: {session.data['user_id']}")
    print(f"Role: {session.data['role']}")

# Update session
manager.update_session(session_id, {"last_activity": "2024-01-15"})

# Delete session
manager.delete_session(session_id)

# File backend for persistence
file_manager = SessionManager(
    backend=FileBackend("./sessions", ttl=86400)
)
```

#### Message Queue
```python
from msgqueue import MessageQueue, FileBackend, Task

# Create queue
queue = MessageQueue(backend=FileBackend("./queue"))

# Add tasks
queue.add(Task(
    name="send-email",
    data={"to": "user@example.com", "subject": "Hello"},
    priority=1
))

queue.add(Task(
    name="process-image",
    data={"image_id": "123"},
    priority=2
))

# Process tasks
while True:
    task = queue.get()
    if not task:
        break
    
    print(f"Processing: {task.name}")
    # Process task...
    queue.ack(task.id)

# Queue statistics
stats = queue.get_stats()
print(f"Pending: {stats['pending']}")
print(f"Processing: {stats['processing']}")
print(f"Completed: {stats['completed']}")
```

#### HTTP Client
```python
from httpclient import HTTPClient, RetryConfig, RateLimitConfig

# Create client with retry and rate limiting
client = HTTPClient(
    base_url="https://api.example.com",
    retry_config=RetryConfig(max_retries=3, backoff_factor=2.0),
    rate_limit=RateLimitConfig(rate=100, period=60),
    timeout=30.0
)

# Make requests
response = client.get("/users")
print(f"Status: {response.status_code}")
print(f"Data: {response.json()}")

# POST with JSON
response = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})

# With authentication
response = client.get(
    "/protected",
    headers={"Authorization": "Bearer token123"}
)

# Batch requests
responses = client.batch([
    {"method": "GET", "url": "/users/1"},
    {"method": "GET", "url": "/users/2"},
    {"method": "POST", "url": "/users", "json": {"name": "Bob"}}
])
```

#### Feature Flags
```python
from features import FeatureManager, Feature, PercentageRollout, UserTargeting

# Create feature manager
manager = FeatureManager()

# Define features
manager.add_feature(Feature(
    name="new_dashboard",
    enabled=True,
    rollout=PercentageRollout(percentage=50),  # 50% of users
    segments=["beta-testers", "premium"]
))

manager.add_feature(Feature(
    name="ai_chat",
    enabled=True,
    targeting=UserTargeting(
        user_ids=["alice", "bob"],
        segments=["enterprise"]
    )
))

# Check feature
if manager.is_enabled("new_dashboard", user_id="alice"):
    print("Show new dashboard")
else:
    print("Show old dashboard")

# Get all features
features = manager.get_features()
for feature in features:
    print(f"{feature.name}: {'enabled' if feature.enabled else 'disabled'}")
```

#### Data Storage
```python
from data import DataStore, SQLiteBackend, MemoryBackend

# SQLite backend
store = DataStore(backend=SQLiteBackend("./data/store.db"))

# Store data
store.set("user:123", {"name": "Alice", "email": "alice@example.com"})
store.set("config:api", {"timeout": 30, "retries": 3})

# Get data
user = store.get("user:123")
print(f"User: {user}")

# Search
results = store.search("user:*")
for key, value in results:
    print(f"{key}: {value}")

# TTL (Time To Live)
store.set("temp:data", {"value": 123}, ttl=3600)  # Expires in 1 hour

# Memory backend (for caching)
memory_store = DataStore(backend=MemoryBackend(max_size_mb=100))
```

#### Health Checks
```python
from health import HealthChecker, Check, HealthStatus

# Create health checker
checker = HealthChecker()

# Add checks
checker.add_check(Check(
    name="database",
    func=lambda: check_database_connection(),
    timeout=5.0
))

checker.add_check(Check(
    name="redis",
    func=lambda: check_redis_connection(),
    timeout=2.0
))

checker.add_check(Check(
    name="api",
    func=lambda: check_external_api(),
    timeout=10.0
))

# Run checks
results = checker.run_checks()
for check_name, result in results.items():
    print(f"{check_name}: {result['status']} ({result['latency']:.2f}s)")

# Get overall status
status = checker.get_status()
print(f"Overall: {status['status']}")
```

#### Crypto Utilities
```python
from crypto import (
    sha256, bcrypt_hash, bcrypt_verify,
    jwt_encode, jwt_decode, generate_fernet_key,
    fernet_encrypt, fernet_decrypt, password_strength
)

# Hashing
hash_value = sha256("hello world")
print(f"SHA256: {hash_value}")

# Password hashing
hashed = bcrypt_hash("mypassword")
is_valid = bcrypt_verify("mypassword", hashed)
print(f"Password valid: {is_valid}")

# JWT tokens
token = jwt_encode(
    payload={"user_id": "alice", "role": "admin"},
    secret="my-secret-key",
    expires_in=3600,
    issuer="mito"
)
print(f"Token: {token}")

payload = jwt_decode(token, "my-secret-key", issuer="mito")
print(f"Payload: {payload}")

# Encryption
key = generate_fernet_key()
encrypted = fernet_encrypt("secret data", key)
decrypted = fernet_decrypt(encrypted, key)
print(f"Decrypted: {decrypted}")

# Password strength
result = password_strength("MyStr0ng!Pass123")
print(f"Strength: {result['strength']} ({result['score']}/{result['max_score']})")
print(f"Checks: {result['checks']}")
```

#### Validators
```python
from validators import (
    validate_email, validate_url, validate_ip,
    validate_uuid, validate_credit_card, validate_phone
)

# Email validation
result = validate_email("user@example.com")
print(f"Valid: {result['valid']}")
print(f"Domain: {result.get('domain')}")

# URL validation
result = validate_url("https://example.com/path?query=1")
print(f"Valid: {result['valid']}")
print(f"Scheme: {result.get('scheme')}")
print(f"Host: {result.get('host')}")

# IP validation
result = validate_ip("192.168.1.1")
print(f"Valid: {result['valid']}")
print(f"Type: {result.get('type')}")

# UUID validation
result = validate_uuid("550e8400-e29b-41d4-a716-446655440000")
print(f"Valid: {result['valid']}")

# Credit card validation
result = validate_credit_card("4111111111111111")
print(f"Valid: {result['valid']}")
print(f"Type: {result.get('type')}")

# Phone validation
result = validate_phone("+1-555-123-4567")
print(f"Valid: {result['valid']}")
print(f"Country: {result.get('country')}")
```

#### Formatters
```python
from formatters import TableFormatter, TreeFormatter, ColorFormatter

# Table formatting
table = TableFormatter()
data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "London"},
    {"name": "Charlie", "age": 35, "city": "Paris"}
]
print(table.format(data, headers=["Name", "Age", "City"]))

# Tree formatting
tree = TreeFormatter()
structure = {
    "project": {
        "src": ["main.py", "utils.py"],
        "tests": ["test_main.py"],
        "docs": ["README.md"]
    }
}
print(tree.format(structure))

# Color formatting
color = ColorFormatter()
print(color.red("Error: Something went wrong"))
print(color.green("Success: Operation completed"))
print(color.yellow("Warning: Check your input"))
print(color.blue("Info: Processing..."))
print(color.bold("Bold text"))
print(color.underline("Underlined text"))
```

#### Converters
```python
from converters import (
    xml_to_dict, dict_to_xml,
    hex_to_binary, binary_to_hex,
    temperature_convert, rgb_to_hex
)

# XML conversion
xml_data = "<user><name>Alice</name><age>30</age></user>"
data = xml_to_dict(xml_data)
print(f"XML to Dict: {data}")

# Dict to XML
xml = dict_to_xml({"user": {"name": "Alice", "age": 30}})
print(f"Dict to XML: {xml}")

# Hex/Binary conversion
binary = hex_to_binary("FF")
print(f"FF in binary: {binary}")

hex_value = binary_to_hex("11111111")
print(f"Binary to hex: {hex_value}")

# Temperature conversion
celsius = temperature_convert(100, "celsius", "fahrenheit")
print(f"100°C = {celsius}°F")

# RGB to Hex
hex_color = rgb_to_hex(255, 0, 0)
print(f"RGB(255,0,0) = {hex_color}")
```

---

## 🖥️ API Server

### Starting the Server

```bash
# Using CLI
./mito server --host 0.0.0.0 --port 8000

# Using Python
python -m uvicorn server.api:app --host 0.0.0.0 --port 8000

# With production settings
python -m uvicorn server.api:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Endpoints

#### Root Endpoint
```http
GET /
```
Response:
```json
{
  "name": "Mito API",
  "version": "1.0.0",
  "status": "running"
}
```

#### List Tools
```http
GET /tools
```
Response:
```json
{
  "tools": [
    {"name": "llama", "description": "Llama LLM inference"},
    {"name": "textgen", "description": "Text generation"},
    {"name": "summarize", "description": "Text summarization"},
    {"name": "translate", "description": "Translation"},
    {"name": "qa", "description": "Question answering"},
    {"name": "sentiment", "description": "Sentiment analysis"},
    {"name": "embed", "description": "Text embeddings"},
    {"name": "ocr", "description": "OCR text recognition"},
    {"name": "classify", "description": "Image classification"},
    {"name": "speech", "description": "Speech recognition"},
    {"name": "tts", "description": "Text-to-speech"}
  ]
}
```

#### Text Generation
```http
POST /generate
Content-Type: application/json

{
  "prompt": "The future of AI is",
  "model": "gpt2",
  "max_tokens": 100,
  "temperature": 0.7
}
```

#### Summarization
```http
POST /summarize
Content-Type: application/json

{
  "text": "Long article text here...",
  "max_length": 130
}
```

#### Translation
```http
POST /translate
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "model": "Helsinki-NLP/opus-mt-en-es"
}
```

#### Question Answering
```http
POST /qa
Content-Type: application/json

{
  "question": "What is Python?",
  "context": "Python is a high-level programming language..."
}
```

#### Sentiment Analysis
```http
POST /sentiment
Content-Type: application/json

{
  "text": "This product is amazing!"
}
```

Response:
```json
{
  "sentiment": "positive",
  "score": 0.9876,
  "emotion": "joy"
}
```

#### Text Embeddings
```http
POST /embed
Content-Type: application/json

{
  "text": "Machine learning is fascinating",
  "model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

#### OCR
```http
POST /ocr
Content-Type: multipart/form-data

file: <image_file>
```

#### Image Classification
```http
POST /classify
Content-Type: multipart/form-data

file: <image_file>
```

#### Speech Recognition
```http
POST /speech
Content-Type: multipart/form-data

file: <audio_file>
```

### API Authentication (API key + optional JWT)

The API supports API keys and optional JWT bearer validation:

1. **API Keys** (set `MITO_API_KEY`, send with `X-API-Key`):
```http
GET /tools
X-API-Key: sk_live_abc123
```

2. **JWT Bearer (RS256)**: Enabled when `MITO_JWT_PUBLIC_KEY` is provided (along with optional `MITO_JWT_ISSUER` / `MITO_JWT_AUDIENCE`). Tokens are validated only when API key auth is enabled.
```http
GET /tools
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Token issuance: call `POST /token` with OAuth2PasswordRequestForm fields (username/password). Set `MITO_JWT_PRIVATE_KEY` for RS256 signing or `MITO_JWT_SECRET` for HS256; TTL via `MITO_JWT_TTL` (default 3600s).
Optional credential checks: set `MITO_JWT_PASSWORD` for a shared password or `MITO_JWT_USERS` as a JSON map of username->password. Refresh tokens via `POST /token/refresh` (requires valid bearer) with TTL `MITO_JWT_REFRESH_TTL` (default 86400s).

### Rate Limiting

The API includes built-in rate limiting:
- Default: 120 requests per minute per key (or `anonymous`)
- Configurable via the `MITO_RATE_LIMIT` environment variable
- Returns `429 Too Many Requests` when limit exceeded

### CORS Configuration

CORS is configured in `mito.yaml`:
```yaml
api:
  cors_origins:
    - "https://app.example.com"
    - "http://localhost:3000"
```

### Middleware Stack

The API includes these middleware components:
1. **CORS Middleware** - Cross-origin resource sharing
2. **Rate Limiting Middleware** - Request throttling
3. **Authentication (MITO_API_KEY + optional JWT) Middleware** - API key validation with optional RS256 JWT verification when `MITO_JWT_PUBLIC_KEY` is set
4. **Security Headers Middleware** - XSS, CSRF protection
5. **Request ID Middleware** - Unique request tracking
6. **Logging Middleware** - Request/response logging
7. **Error Handling Middleware** - Centralized error handling

---

## 🔌 Integration Plugins

### Plugin Categories (276 Total)

#### Communication (12)
- GitHub - Repository management, issues, pull requests
- Slack - Team messaging, channels, webhooks
- Discord - Community chat, bots, webhooks
- Telegram - Bot API, messaging, notifications
- Teams - Microsoft Teams integration
- WhatsApp - Business API, messaging
- Matrix - Decentralized communication
- Twilio - SMS, voice, video
- Vonage - Communications APIs
- MessageBird - SMS, voice, WhatsApp
- Bandwidth - Voice, messaging, 911
- Email (SMTP, SendGrid, Resend, Postmark) - Email delivery

#### CRM & Sales (14)
- Salesforce - CRM, opportunities, contacts
- HubSpot - Marketing, sales, service
- Intercom - Customer messaging
- Zendesk - Customer service
- Freshdesk - Help desk software
- Help Scout - Customer support
- Crisp - Live chat, CRM
- Gong - Revenue intelligence
- Clari - Revenue platform
- Outreach - Sales execution
- Salesloft - Sales engagement
- Apollo - Sales intelligence
- ZoomInfo - B2B contact data
- Clearbit - Business intelligence

#### Project Management (12)
- Jira - Issue tracking, agile boards
- Linear - Project management
- Trello - Kanban boards
- Asana - Work management
- Notion - All-in-one workspace
- Confluence - Documentation
- Airtable - Database-spreadsheet hybrid
- ClickUp - Productivity platform
- Monday - Work OS
- Shortcut - Project management
- Height - Project management
- (Duplicate ClickUp removed)

#### DevOps & Monitoring (16)
- GitLab - DevOps platform
- Vercel - Deployment platform
- Sentry - Error tracking
- Datadog - Monitoring & analytics
- PagerDuty - Incident response
- LaunchDarkly - Feature management
- Grafana - Observability
- New Relic - Observability
- Dynatrace - APM
- Honeycomb - Observability
- CircleCI - CI/CD
- Buildkite - CI/CD
- Semaphore - CI/CD
- SonarQube - Code quality
- Codecov - Code coverage
- ArgoCD - GitOps CD

#### Auth & Identity (8)
- Auth0 - authentication (not implemented)
- Okta - Identity management
- Clerk - authentication (not implemented)
- WorkOS - Enterprise SSO
- Stytch - Passwordless auth
- FusionAuth - Identity platform
- SuperTokens - Auth infrastructure

#### Databases (14)
- PostgreSQL - Relational database
- MySQL - Relational database
- MongoDB - Document database
- Redis - In-memory store
- Elasticsearch - Search engine
- Meilisearch - Search engine
- ClickHouse - OLAP database
- InfluxDB - Time series database
- Cassandra - Wide-column store
- CockroachDB - Distributed SQL
- PlanetScale - MySQL platform
- Neon - Serverless Postgres
- SQLite - Embedded database

#### Vector Databases (6)
- Pinecone - Vector database
- Weaviate - Vector database
- Qdrant - Vector database
- ChromaDB - Embedding database
- Voyage AI - Embedding models
- FAISS - Similarity search

#### AI/ML (18)
- OpenAI - GPT models
- Anthropic - Claude models
- Mistral - Mistral models
- Cohere - Cohere models
- Groq - Groq inference
- Together - Together AI
- Ollama - Local models
- Fireworks - Fireworks AI
- Replicate - ML models
- HuggingFace - Model hub
- Stability AI - Image generation
- ElevenLabs - Voice AI
- AssemblyAI - Speech-to-text
- Deepgram - Speech AI
- Perplexity - AI search
- Anyscale - Ray platform

#### Payments (8)
- Stripe - Payment processing
- PayPal - Payments
- Square - Payments
- Adyen - Payments
- Razorpay - Payments
- Paddle - SaaS payments
- LemonSqueezy - Merchant of record

#### Cloud Infrastructure (20)
- **AWS (10+)**: S3, Lambda, SNS, SQS, EC2, ECS, RDS, ECR, Secrets Manager
- **GCP (6+)**: Functions, Pub/Sub, BigQuery, Cloud Run, GCS, GCR
- **Azure (4+)**: Functions, Service Bus, Cosmos DB, Blob Storage
- **Others**: DigitalOcean, Heroku, Cloudflare, Supabase, Firebase, MinIO

#### CMS & Content (6)
- Contentful - Headless CMS
- Strapi - Headless CMS
- Sanity - Content platform
- Prismic - Headless CMS
- Storyblok - Headless CMS

#### Analytics (6)
- Mixpanel - Product analytics
- Amplitude - Digital analytics
- PostHog - Product OS
- Heap - Product analytics
- Segment - Customer data

#### ETL & Data (4)
- Fivetran - Data integration
- Stitch - Data pipeline
- Airbyte - Data integration
- Meltano - Data integration

#### Workflow (4)
- Zapier - Automation
- n8n - Workflow automation
- Make - Automation platform
- Windmill - Workflow engine

#### Security (4)
- Snyk - Security scanning
- Trivy - Security scanner
- Semgrep - Static analysis
- Veracode - Application security

#### Messaging (4)
- Kafka - Event streaming
- RabbitMQ - Message broker
- NATS - Messaging system
- Pulsar - Messaging

#### Testing (4)
- Playwright - E2E testing
- Cypress - E2E testing
- BrowserStack - Testing platform
- LambdaTest - Testing platform

#### File Storage (4)
- Dropbox - Cloud storage
- Box - Cloud storage
- OneDrive - Microsoft storage
- Google Drive - Google storage

#### Maps (4)
- Mapbox - Maps
- Google Maps - Maps
- HERE - Maps
- MapTiler - Maps

#### Legal (4)
- DocuSign - E-signatures
- HelloSign - E-signatures
- PandaDoc - Document automation
- Ironclad - Contract management

#### Accounting (4)
- QuickBooks - Accounting
- Xero - Accounting
- FreshBooks - Accounting
- Wave - Accounting

#### Social (5)
- Twitter - Social media
- Instagram - Social media
- LinkedIn - Professional network
- Reddit - Social news
- TikTok - Short video

#### Shipping (4)
- Shippo - Shipping API
- EasyPost - Shipping API
- ShipEngine - Shipping API
- Flexport - Logistics

#### HR (4)
- Gusto - Payroll & HR
- Rippling - Workforce management
- Deel - Global HR
- Remote - Remote work platform

### Plugin Usage Example

```python
from plugins import PluginManager

# Create plugin manager
manager = PluginManager(plugin_dirs=["./plugins", "~/.mito/plugins"])

# Discover plugins
manager.discover()

# Install a plugin
manager.install("github")

# Enable plugin
manager.enable("github")

# Get plugin info
info = manager.get_info("github")
print(f"Version: {info.metadata.version}")
print(f"State: {info.state}")

# Use plugin
plugin = manager.get_plugin("github")
repos = plugin.list_repos()
```

---

## ⚙️ Configuration System

### Configuration Files

Mito uses YAML configuration files with environment variable overrides.

#### Default Configuration (`mito.yaml`)
```yaml
version: "1.0.0"
profile: "default"

model:
  default_model: "gpt2"
  llama_model: "model.gguf"
  llama_ctx: 2048
  llama_threads: 4
  temperature: 0.7
  max_tokens: 256

api:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  cors_origins: ["*"]
  api_keys: []
  rate_limit: 100
  timeout: 30
  max_request_size: 10485760

storage:
  models_dir: "./models"
  data_dir: "./data"
  cache_dir: "./.cache"
  vector_store_path: "./data/vectorstore.json"
  max_cache_size_mb: 1024

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: null
  max_size_mb: 100
  backup_count: 5

observability:
  enable_metrics: true
  metrics_port: 9090
  enable_tracing: false
  trace_sample_rate: 0.1
  health_check_interval: 30
```

### Environment Variable Overrides

All configuration values can be overridden with environment variables using the pattern `MITO_<SECTION>_<KEY>`:

```bash
# Override API port
export MITO_API_PORT=9000

# Override model settings
export MITO_MODEL_DEFAULT_MODEL=llama2
export MITO_MODEL_TEMPERATURE=0.8

# Override logging
export MITO_LOGGING_LEVEL=DEBUG

# Override storage
export MITO_STORAGE_DATA_DIR=/var/data/mito
```

### Configuration Profiles

Mito supports multiple configuration profiles:

```bash
# Create profile directory
mkdir -p profiles

# Create production profile
cat > profiles/production.yaml << EOF
api:
  port: 80
  workers: 8
  cors_origins:
    - "https://app.example.com"
  rate_limit: 1000

model:
  llama_threads: 16
  max_tokens: 1024

logging:
  level: "WARNING"
  file: "/var/log/mito.log"
EOF

# Load profile in code
from config import ConfigManager
manager = ConfigManager("mito.yaml")
manager.load_profile("production")
```

### Configuration Validation

```python
from config import ConfigSchema, create_default_schema

# Create schema with validation rules
schema = create_default_schema()

# Add custom rules
schema.add_rule("api.port", rule_type="int", min_val=1, max_val=65535, required=True)
schema.add_rule("model.temperature", rule_type="float", min_val=0.0, max_val=2.0)
schema.add_rule("logging.level", rule_type="str", allowed=["DEBUG", "INFO", "WARNING", "ERROR"])

# Validate configuration
manager = ConfigManager("mito.yaml", schema=schema)
config = manager.load()

errors = manager.validate()
if errors:
    print(f"Configuration errors: {errors}")
else:
    print("Configuration is valid!")
```

### Hot Reload

```python
from config import ConfigManager

manager = ConfigManager("mito.yaml")

# Define callback for config changes
def on_config_change(config):
    print(f"Config changed to version {config.version}")
    # Re-initialize components with new config

# Register callback
manager.on_change(on_config_change)

# Start watching for changes
manager.start_watching(interval=2.0)

# Config changes will trigger callbacks automatically
# Stop watching when done
manager.stop_watching()
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_ai_modules.py -v

# Run with coverage
pytest tests/ --cov=python --cov=agents --cov=config

# Run C++ tests
make test

# Run integration tests
pytest tests/ -m integration

# Run performance tests
pytest tests/ -m performance
```

### Test Structure

```
tests/
├── test_ai_modules.py      # AI module import and structure tests
├── test_infrastructure.py  # Infrastructure module tests
├── test_plugins.py         # Plugin system tests
└── test_server.py          # API server tests
```

### Test Coverage

The test suite covers:
- **230+ test cases** across all modules
- **AI Module Imports**: Validates all AI module imports and quick functions
- **Agent Framework**: Tests agent creation, tool usage, and evaluation
- **Configuration**: Tests config loading, validation, and environment overrides
- **Event System**: Tests event publishing, subscription, and persistence
- **Crypto Utilities**: Tests hashing, encryption, and token generation
- **Validators**: Tests email, URL, IP, UUID validation
- **API Server**: Tests all REST endpoints

### Writing Tests

```python
import pytest
from python.ai import SentimentAnalyzer

class TestSentiment:
    def test_positive_sentiment(self):
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze("I love this product!")
        assert result['label'] == 'positive'
        assert result['score'] > 0.7
    
    def test_negative_sentiment(self):
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze("This is terrible.")
        assert result['label'] == 'negative'
        assert result['score'] > 0.7
    
    def test_quick_sentiment(self):
        from python.ai import quick_sentiment
        result = quick_sentiment("Amazing!")
        assert 'label' in result
        assert 'score' in result
```

### Continuous Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=python --cov=agents --cov=config --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 🐳 Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Build C++ components
RUN make

# Create necessary directories
RUN mkdir -p models data logs

# Set environment variables
ENV MITO_API_PORT=8000
ENV MITO_MODEL_LLAMA_MODEL=/models/model.gguf

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "server.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  mito-api:
    build: .
    ports:
      - "8000:8000"
      - "9090:9090"  # Metrics port
    volumes:
      - ./models:/models
      - ./data:/data
      - ./logs:/var/log/mito
    environment:
      - MITO_API_PORT=8000
      - MITO_MODEL_LLAMA_MODEL=/models/model.gguf
      - MITO_LOGGING_FILE=/var/log/mito/mito.log
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mito
      - POSTGRES_USER=mito
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  redis-data:
  postgres-data:
```

### Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mito-api
  labels:
    app: mito
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mito
  template:
    metadata:
      labels:
        app: mito
    spec:
      containers:
      - name: mito
        image: mito:latest
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 9090
          name: metrics
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2"
        env:
        - name: MITO_API_PORT
          value: "8000"
        - name: MITO_MODEL_LLAMA_MODEL
          value: "/models/model.gguf"
        volumeMounts:
        - name: models
          mountPath: /models
        - name: data
          mountPath: /data
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: mito-models-pvc
      - name: data
        persistentVolumeClaim:
          claimName: mito-data-pvc

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mito-service
spec:
  selector:
    app: mito
  ports:
  - port: 80
    targetPort: 8000
    name: http
  - port: 9090
    targetPort: 9090
    name: metrics
  type: LoadBalancer

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mito-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: mito.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mito-service
            port:
              name: http

---
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mito-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mito-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Terraform

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

# ECS Cluster
resource "aws_ecs_cluster" "mito" {
  name = "mito-cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "mito" {
  family                   = "mito-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048
  
  container_definitions = jsonencode([
    {
      name      = "mito"
      image     = "mito:latest"
      cpu       = 1024
      memory    = 2048
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
      environment = [
        { name = "MITO_API_PORT", value = "8000" }
      ]
    }
  ])
}

# ECS Service
resource "aws_ecs_service" "mito" {
  name            = "mito-service"
  cluster         = aws_ecs_cluster.mito.id
  task_definition = aws_ecs_task_definition.mito.arn
  desired_count   = 3
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets         = var.subnet_ids
    security_groups = [aws_security_group.mito.id]
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.mito.arn
    container_name   = "mito"
    container_port   = 8000
  }
}

# Application Load Balancer
resource "aws_lb" "mito" {
  name               = "mito-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.mito.id]
  subnets            = var.subnet_ids
}

resource "aws_lb_target_group" "mito" {
  name        = "mito-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "mito" {
  load_balancer_arn = aws_lb.mito.arn
  port              = 80
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.mito.arn
  }
}

# Security Group
resource "aws_security_group" "mito" {
  name        = "mito-sg"
  description = "Security group for Mito API"
  vpc_id      = var.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Monitoring and Observability

#### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
REQUESTS = Counter('mito_requests_total', 'Total API requests')
REQUEST_LATENCY = Histogram('mito_request_duration_seconds', 'Request latency')
ACTIVE_REQUESTS = Gauge('mito_active_requests', 'Active requests')

# Start metrics server
start_http_server(9090)

# Use in API endpoints
@app.get("/")
async def root():
    with REQUEST_LATENCY.time():
        REQUESTS.inc()
        ACTIVE_REQUESTS.inc()
        try:
            return {"status": "ok"}
        finally:
            ACTIVE_REQUESTS.dec()
```

#### Health Checks

```python
from health import HealthChecker, Check

checker = HealthChecker()

# Add checks
checker.add_check(Check(
    name="database",
    func=lambda: check_db_connection(),
    timeout=5.0
))

checker.add_check(Check(
    name="redis",
    func=lambda: check_redis_connection(),
    timeout=2.0
))

# Health endpoint
@app.get("/health")
async def health():
    results = checker.run_checks()
    overall = "healthy" if all(r['status'] == 'healthy' for r in results.values()) else "unhealthy"
    return {"status": overall, "checks": results}
```

---

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/mito.git
cd mito

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v

# Format code
black .

# Type checking
mypy python/ agents/ config/

# Linting
flake8 python/ agents/ config/
```

### Code Style

We follow these standards:
- **Python**: PEP 8 with Black formatting
- **Type Hints**: Required for all public APIs
- **Docstrings**: Google style for all modules, classes, and functions
- **Comments**: Minimal, only when necessary for clarity

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request with a clear description

### Issue Reporting

When reporting issues, please include:
- Mito version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

### Development Roadmap

**v1.1.0** (Planned)
- Additional LLM providers (Google Gemini, Cohere v2)
- Enhanced RAG with chunking and reranking
- Streaming API endpoints
- WebSocket support for real-time updates

**v1.2.0** (Planned)
- Fine-tuning support for custom models
- Model marketplace integration
- Advanced workflow features (sub-workflows, conditional branching)
- Enhanced monitoring with OpenTelemetry

**v2.0.0** (Future)
- Rust core for performance-critical components
- Distributed agent coordination
- Advanced caching strategies
- Multi-modal AI support (vision + language)

---

## 📄 License

MIT License

Copyright (c) 2024 Mito Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

<p align="center">
  Built with Python, C++, Transformers, and llama.cpp
</p>

<p align="center">
  <a href="https://github.com/yourusername/mito">GitHub</a> •
  <a href="https://github.com/yourusername/mito/issues">Issues</a> •
  <a href="https://github.com/yourusername/mito/wiki">Documentation</a>
</p>