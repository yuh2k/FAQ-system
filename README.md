# FAQ System 🤖

Smart AI customer service system with session memory and intelligent ticket management.


## Quick Start

### Prerequisites
- Python 3.8+ & Node.js 16+
- [Ollama](https://ollama.ai) installed

### Setup (5 minutes)

```bash
# 1. Start Ollama & download AI model
ollama serve
ollama pull deepseek-r1:1.5b


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



