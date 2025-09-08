# FAQ System 🤖

Smart AI customer service system with session memory and intelligent ticket management.

## Key Features

- **🧠 AI Chat** - Smart responses using local LLM (DeepSeek-R1) + knowledge base
- **💾 Session Memory** - Resume conversations from any device using email
- **🎫 Smart Tickets** - AI automatically creates tickets when human help needed
- **📱 Mobile Friendly** - Responsive design with mobile navigation
- **🔍 Smart Guidance** - 3-round guidance system with user choice

## Quick Start

### Prerequisites
- Python 3.8+ & Node.js 16+
- [Ollama](https://ollama.ai) installed

### Setup (5 minutes)

```bash
# 1. Start Ollama & download AI model
ollama serve
ollama pull deepseek-r1:1.5b

# 2. Backend setup
cd server && python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate  
pip install -r requirements.txt && python run.py

# 3. Frontend setup (new terminal)
cd frontend && npm install && npm start
```

**Access:** http://localhost:3000

## How It Works

1. **Enter Email** - System checks for previous conversations
2. **Choose Session** - Continue old conversation or start fresh  
3. **Chat** - AI provides smart responses using knowledge base
4. **Smart Ticketing** - Creates tickets only when explicitly requested or after guidance

### Smart Features
- **Session Memory** - All conversations saved and retrievable by email
- **3-Round Guidance System**:
  - **Round 1-3**: AI guides unclear questions with examples and suggestions
  - **After Round 3**: User chooses between creating ticket or ending chat
  - **Only explicit requests** like "speak to human" create immediate tickets
- **Mobile Responsive** - Works great on phones with bottom navigation  
- **Knowledge Base** - Browse Q&A database for common questions

## Testing

```bash
# Run all tests
cd tests && python run_all.py

# Run specific test suites
python tests/test_api.py           # API endpoint tests
python tests/test_ai_logic.py      # AI business logic tests  
python tests/test_integration.py   # Integration workflow tests
```

**Test Coverage:**
- ✅ API endpoints and HTTP handling
- ✅ AI intent detection and response logic
- ✅ 3-round guidance system with user choice
- ✅ Ticket creation workflows
- ✅ Session management
- ✅ Complete user interaction flows

## API

- **Chat**: `POST /chat` - Send message, get AI response
- **Sessions**: `GET /sessions/{email}` - Get user's conversation history
- **Tickets**: `GET /tickets` - List support tickets
- **API Docs**: http://localhost:8000/docs

## Troubleshooting

**AI not responding:** Check `ollama serve` and `ollama pull deepseek-r1:1.5b`  
**Database issues:** Delete `server/faq_system.db` to reset  
**Frontend errors:** Run `npm install` in frontend directory