# Technical Documentation

Core technical guide for the Customer FAQ System.

## Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React 18      │    │   FastAPI       │    │   SQLite        │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│   (Port 3000)   │    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Ollama        │
                       │   AI Service    │
                       │   (Port 11434)  │
                       └─────────────────┘
```

### Technology Stack

**Frontend:**
- React 18 + TypeScript + Ant Design 5.x
- Session management with email-based history
- Real-time chat interface with status indicators
- Read-only mode for ended sessions

**Backend:**
- FastAPI with async SQLAlchemy + SQLite
- Session persistence and ticket management
- TF-IDF knowledge base search (70+ Q&A pairs)
- 3-round guidance system with smart escalation

**AI Service:**
- Ollama + DeepSeek-R1:1.5b model
- Context-aware conversation memory
- Automatic service startup and health checking
- Fallback responses when AI unavailable

**Knowledge Base:**
- Plain text format (Q: / A: structure)
- Automotive domain with 8 major categories
- TF-IDF vectorization + cosine similarity matching
- Hot-reloadable configuration

## Detailed Setup Instructions

### Prerequisites Installation

#### Python 3.8+
```bash
# macOS (using Homebrew)
brew install python

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows
# Download from https://www.python.org/downloads/
```

#### Node.js 16+
```bash
# macOS (using Homebrew)
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows
# Download from https://nodejs.org/
```

#### Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download/windows
```

### Manual Setup Process

#### 1. Ollama Setup
```bash
# Start Ollama service
ollama serve

# Download the AI model (in another terminal)
ollama pull deepseek-r1:1.5b

# Verify installation
ollama list
```

#### 2. Backend Setup
```bash
# Navigate to project
cd FAQ-system/server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python app/database.py

# Start server
python run.py
```

#### 3. Frontend Setup
```bash
# Navigate to frontend (new terminal)
cd FAQ-system/frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Configuration

#### Backend Configuration

**Database Configuration** (`server/app/database.py`):
```python
DATABASE_URL = "sqlite+aiosqlite:///./faq_system.db"
```

**CORS Configuration** (`server/app/main.py`):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**AI Service Configuration** (`server/config/config.yaml`):
```yaml
ai_service:
  provider: "local_ai"
  model: "deepseek-r1:1.5b"
  base_url: "http://localhost:11434"
  max_tokens: 500
  temperature: 0.7
```

#### Knowledge Base Configuration

**Plain Text Format** (`server/config/knowledge_bases/automotive_en.txt`):
```
Q: Should I buy a new car or a used car?
A: This depends on your budget and needs. New cars come with warranties and no usage history, but are more expensive and depreciate quickly.

Q: What documents do I need to buy a car?
A: For personal purchases, you need driver's license, ID, proof of residence, and income proof for financing.
```

**Knowledge Base Features:**
- 70+ automotive Q&A pairs covering 8 major categories
- TF-IDF similarity matching with configurable threshold
- Support for multiple knowledge bases with hot switching
- Plain text format for easy maintenance

## Development Guide

### Project Structure

```
FAQ-system/
├── start.sh                    # Start all services (auto-starts Ollama)
├── setup.sh                    # One-click setup script
├── README.md                   # User documentation
├── TECHNICAL.md                # This technical guide
├── faq_system.db              # SQLite database
│
├── frontend/                   # React 18 + TypeScript application
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ChatInterface.tsx      # Main chat interface
│   │   │   ├── MessageBubble.tsx      # Individual message display
│   │   │   ├── SessionHistory.tsx     # Session list and history
│   │   │   └── UserEmailForm.tsx      # Email input form
│   │   ├── services/api.ts     # API communication layer
│   │   ├── types/index.ts      # TypeScript type definitions
│   │   └── App.tsx             # Main application component
│   └── package.json            # Dependencies and scripts
│
├── server/                     # FastAPI backend application
│   ├── app/                    # Application code
│   │   ├── main.py             # API routes and FastAPI app
│   │   ├── ai_service.py       # AI conversation logic
│   │   ├── knowledge_base_service.py  # Q&A search and matching
│   │   ├── models.py           # Database models (sessions, messages, tickets)
│   │   ├── schemas.py          # Request/response schemas
│   │   ├── database.py         # Database configuration
│   │   └── config_loader.py    # Configuration management
│   ├── config/                 # Configuration files
│   │   ├── ai_prompts_config.yaml     # AI prompts and responses
│   │   ├── knowledge_base_config.yaml # Knowledge base settings
│   │   └── knowledge_bases/           # Knowledge base files
│   │       └── automotive_en.txt      # 70+ automotive Q&A pairs
│   ├── requirements.txt        # Python dependencies
│   ├── .env                   # Environment variables
│   └── run.py                 # Server startup script
│
└── tests/                     # Test suite
    ├── test_api.py            # API endpoint tests
    ├── test_ai_logic.py       # AI service tests
    ├── test_integration.py    # Integration tests
    └── run_all.py             # Test runner
```

### Database Schema

**Core Tables:**
- `chat_sessions` - Email-based session management with guidance state tracking
- `chat_messages` - Message history with knowledge base source tracking  
- `tickets` - Support ticket creation with full conversation context

**Key Features:**
- Email-based session persistence
- 3-round guidance system tracking (`unclear_message_count`, `guidance_stage`)
- Knowledge base hit tracking (`is_from_kb`)
- Session status management (`is_active`, read-only for ended sessions)
- Support ticket escalation with conversation context

### API Endpoints

**Core Chat Functions:**
- `POST /chat` - Send message, get AI response, auto-create tickets
- `GET /chat/history/{session_id}` - Load conversation history with session status
- `GET /sessions/{email}` - Get all user sessions with metadata

**Ticket Management:**
- `GET /tickets` - List all support tickets  
- `PUT /tickets/{ticket_id}/status` - Update ticket status

**Knowledge Base:**
- `GET /knowledge-base` - Get all Q&A pairs (70+ automotive entries)
- `POST /config/switch-kb/{kb_name}` - Switch knowledge base
- `GET /config/status` - System configuration and AI status

**Features:**
- No authentication (demo system)
- JSON request/response format
- Automatic Ollama service health checking
- Session-based conversation persistence

### Core Components

**AI Service (`ai_service.py`):**
- 3-round guidance system with escalation logic
- DeepSeek-R1:1.5b integration with fallback responses
- Context-aware conversation memory
- Automatic ticket creation for unresolved issues

**Knowledge Base (`knowledge_base_service.py`):**
- TF-IDF vectorization + cosine similarity matching
- Plain text Q&A format support
- Hot-swappable knowledge bases
- Configurable similarity threshold

**Session Management:**
- Email-based persistent sessions
- Read-only mode for ended sessions
- Visual status indicators (active, ended, has ticket)
- Full conversation history with metadata

**Frontend Features:**
- Real-time chat interface with typing indicators
- Session history browser with search
- Choice buttons for guided interactions
- Responsive design with mobile optimization

## Troubleshooting

### Quick Fixes

**AI not responding:**
```bash
# Check Ollama status
curl -s http://localhost:11434/api/tags

# Restart Ollama (auto-handled by start.sh)
./start.sh
```

**Service startup issues:**
```bash
# Check ports
lsof -i :3000,8000,11434

# Restart everything
./start.sh
```

**Database issues:**
```bash
# Check database file
ls -la faq_system.db

# View recent sessions
sqlite3 faq_system.db "SELECT * FROM chat_sessions ORDER BY created_at DESC LIMIT 5;"
```

**Frontend build issues:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### System Status Checks

**Backend health:** `GET http://localhost:8000/config/status`
**Knowledge base:** `GET http://localhost:8000/knowledge-base` 
**AI service:** `GET http://localhost:8000/config/ai-status`

### Development Tips

- Use `python tests/run_all.py` to run all tests
- Check logs in browser console for frontend issues  
- Backend runs in debug mode by default
- Knowledge base changes require `POST /config/reload`
- Sessions persist across restarts via SQLite database
