# Customer FAQ System 🤖

AI-powered customer service system with intelligent conversation management and smart ticket creation.

## Features

- **🤖 Intelligent AI Chat** - Local DeepSeek model with conversation memory
- **📝 Smart Ticket Creation** - Context-aware support escalation 
- **🔄 3-Round Guidance** - Progressive assistance with button choices
- **💾 Session Management** - Persistent conversation history by email
- **📚 Knowledge Base** - Automatic Q&A search and retrieval
- **📱 Responsive Design** - Mobile-optimized interface

## One-Click Setup

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 16+](https://nodejs.org/)
- [Ollama](https://ollama.ai/) - Local AI service

### Installation
```bash
# Clone and setup everything automatically
./setup.sh

# Start the system
./start.sh
```

**Access:** http://localhost:3000

### Manual Setup
See [TECHNICAL.md](TECHNICAL.md) for detailed installation instructions.

## Usage

1. **Enter Email** - System loads your conversation history
2. **Select Session** - Continue existing chat or start new one
3. **Interactive Chat** - AI provides smart responses using knowledge base
4. **Smart Resolution** - System guides unclear requests through 3 rounds
5. **Choice Actions** - Create support ticket or end conversation

## System Behavior

### Intelligent Routing
- **Direct Answers** - Knowledge base search for common questions
- **Guided Assistance** - 3-round help for unclear requests
- **Smart Escalation** - Automatic ticket creation for complex issues

### Button-Based Choices
After 3 unclear messages, users get clickable options:
- **Create Ticket** - Human agent escalation
- **End Chat** - Close conversation gracefully

## Quick Commands

```bash
# Start system
./start.sh

# Stop all services  
./stop.sh

# Run tests
python tests/run_all.py

# View logs
tail -f server/logs/*.log
```

## API Access

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000  
- **API Docs:** http://localhost:8000/docs

## Project Structure

```
FAQ-system/
├── setup.sh              # One-click setup
├── start.sh / stop.sh     # Service control
├── frontend/              # React.js app
├── server/                # FastAPI backend
├── tests/                 # Test suite
├── README.md              # This file
└── TECHNICAL.md           # Detailed documentation
```

## Documentation

- **[TECHNICAL.md](TECHNICAL.md)** - Comprehensive technical guide
- **[tests/README.md](tests/README.md)** - Testing documentation
- **API Docs** - http://localhost:8000/docs (when running)

## Key Technologies

- **Frontend:** React + TypeScript + Ant Design
- **Backend:** FastAPI + SQLAlchemy + SQLite  
- **AI:** Ollama + DeepSeek-R1 model
- **Knowledge Base:** TF-IDF similarity matching

## Troubleshooting

**AI not responding?**
```bash
# Check Ollama
ollama serve
ollama pull deepseek-r1:1.5b
```

**Services not starting?**
```bash
# Check ports
lsof -i :3000,8000,11434

# Restart everything
./stop.sh && ./start.sh
```

**Need help?** See [TECHNICAL.md](TECHNICAL.md) for detailed troubleshooting.

---

*Built for intelligent customer service automation*