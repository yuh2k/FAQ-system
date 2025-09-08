# FAQ System 🤖💬

An intelligent customer service system with AI chat, knowledge base, and automatic ticket management.

## Quick Start

### Requirements
- Python 3.8+
- Node.js 16+
- Ollama (for AI features)

### Installation

1. **Install Ollama and pull the AI model:**
```bash
# Install Ollama (https://ollama.ai)
ollama serve
ollama pull deepseek-r1:1.5b
```

2. **Start the backend:**
```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

3. **Start the frontend (new terminal):**
```bash
cd frontend
npm install
npm start
```

### Access
- **Web App**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## How to Use

### Web Interface
1. Open http://localhost:3000 in your browser
2. Enter your email to start chatting
3. Navigate between:
   - **Chat Support** - Ask questions and get AI responses
   - **Support Tickets** - View and manage created tickets  
   - **Knowledge Base** - Browse available Q&A content

### Key Features
- **Smart Responses** - AI uses knowledge base + local LLM for accurate answers
- **Robust Ticket Creation** - Guaranteed ticket creation when AI says "NEEDS_HUMAN_FOLLOWUP"
- **3-Message Guidance** - Guides unclear user questions with 3 attempts before escalating to ticket
- **Session Memory** - Chat history and guidance state preserved across conversations
- **Multi-language** - Switch between different knowledge bases via API

### Testing
```bash
# Test system functionality
cd server
python demo_example.py
```

## Configuration

Knowledge bases and AI prompts can be customized via files in `server/config/`:
- Switch knowledge bases: `POST /knowledge-base/switch/{kb_name}`
- Reload config: `POST /config/reload`

## Documentation

- **Technical Details**: See [TECHNICAL.md](TECHNICAL.md)  
- **API Reference**: http://localhost:8000/docs (when running)

## Troubleshooting

**Ollama not responding:**
- Ensure Ollama is running: `ollama serve`
- Check if model is pulled: `ollama pull deepseek-r1:1.5b`

**Database errors:**
- Delete `faq_system.db` to reset database
- Check file permissions on the database file
