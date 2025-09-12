# Customer FAQ System

AI-powered customer service system with intelligent conversation management and smart ticket creation.

[Demo Video](https://drive.google.com/file/d/1tcsHSpg03Jon2r29Gen__UDoJVO4yhw0/view?usp=sharing)

## Features

- **🤖 Intelligent AI Chat** - Local DeepSeek model with conversation memory and context awareness
- **📝 Smart Ticket Creation** - Context-aware support escalation with full conversation history
- **💾 Session Management** - Persistent conversation history by email with read-only mode for ended sessions
- **📚 Comprehensive Knowledge Base** - 70+ automotive Q&A pairs with TF-IDF similarity matching
- **📱 Responsive Design** - Mobile-optimized interface with session history and status indicators
- **🔍 Session History** - View and continue previous conversations with visual status indicators
- **⚡ Auto-Start Services** - Ollama AI service management with automatic model checking
- **🛡️ Plain Text Knowledge Base** - Simple text format for easy knowledge base maintenance

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

## Usage Guide

### Getting Started
1. **Launch System** - Run `./start.sh` to start all services
2. **Open Browser** - Navigate to http://localhost:3000
3. **Enter Email** - System automatically loads your conversation history
4. **Choose Session** - Select existing session or start a new conversation

### Chat Features

#### 🤖 Intelligent Responses
- **Knowledge Base Search** - System automatically searches 70+ automotive Q&A pairs
- **Direct Answers** - Get instant responses for common questions about car buying, selling, insurance, maintenance, and electric vehicles
- **Context Awareness** - AI remembers conversation history and provides relevant follow-up responses

#### 🔄 3-Round Guidance System
When your question is unclear, the system provides:
1. **First Round** - AI asks clarifying questions to understand your need
2. **Second Round** - Provides more specific guidance based on your response  
3. **Third Round** - Offers final assistance attempt with actionable choices

#### 📝 Smart Ticket Creation
After 3 rounds of unclear communication:
- **Create Ticket Button** - Escalates to human support with full conversation context
- **End Chat Button** - Gracefully closes conversation
- **Automatic Detection** - System can also auto-create tickets for complex issues

### Session Management

#### 📱 Persistent Conversations
- **Email-Based** - All conversations linked to your email address
- **Session History** - View and continue previous conversations
- **Read-Only Mode** - Ended sessions display conversation but prevent new messages
- **Status Indicators** - Clear visual feedback for session state (active, ended, ticket created)

#### 🔍 Session Features
- **Session List** - See all your previous conversations with timestamps
- **Message Count** - Quick overview of conversation length
- **Last Message Preview** - See the most recent message in each session
- **Ticket Status** - Visual indicators when support tickets have been created

### Knowledge Base Content

The system includes comprehensive automotive knowledge covering:
- **Car Buying** - New vs used, financing, negotiation, documentation
- **Car Selling** - Timing, valuation, preparation, avoiding scams
- **Insurance** - Coverage types, choosing providers, claims process  
- **Financing** - Loan options, credit requirements, refinancing
- **Maintenance** - Service schedules, finding mechanics, common repairs
- **Electric Vehicles** - Charging, range, incentives, maintenance differences
- **Safety & Technology** - ADAS features, recalls, reliability research
- **Practical Tips** - Test driving, negotiations, paperwork, budgeting

### Example Use Cases

**New Car Buyer:**
- "Should I buy new or used?" → Gets comprehensive comparison
- "What documents do I need?" → Receives complete checklist
- "How do I negotiate price?" → Gets step-by-step strategy

**Car Maintenance:**
- "When should I change my oil?" → Gets specific mileage recommendations
- "My brakes are squealing" → Gets troubleshooting guidance and safety advice
- "How do I find a good mechanic?" → Receives verification tips and questions to ask

**Electric Vehicle Interest:**
- "Are EVs worth buying now?" → Gets decision framework based on driving patterns
- "How much does charging cost?" → Receives cost breakdown and calculators
- "Can I install home charging?" → Gets installation guidance and cost estimates

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
```

## API Access

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000  
- **API Docs:** http://localhost:8000/docs

## API Endpoints

### Core Chat API
- `POST /chat` - Send chat message and get AI response
- `GET /chat/history/{session_id}` - Get chat history for a session
- `GET /sessions/{email}` - Get all sessions for a user email

### Ticket Management
- `GET /tickets` - Get all support tickets
- `GET /tickets/{ticket_id}` - Get specific ticket details
- `PUT /tickets/{ticket_id}/status` - Update ticket status

### Knowledge Base
- `GET /knowledge-base` - Get all Q&A pairs from knowledge base
- `GET /config/knowledge-bases` - List available knowledge bases
- `POST /config/switch-kb/{kb_name}` - Switch to different knowledge base

### Configuration & Status
- `GET /config/status` - Get system configuration status
- `GET /config/ai-status` - Get AI service status
- `POST /config/reload` - Reload all configurations

### Debug Endpoints
- `GET /debug/db-info` - Database connection information
- `GET /debug/raw-sessions/{email}` - Raw session data for debugging

## Project Structure

```
FAQ-system/
├── setup.sh              # One-click setup script
├── start.sh               # Service startup script  
├── frontend/              # React.js frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── SessionHistory.tsx
│   │   │   └── UserEmailForm.tsx
│   │   ├── services/      # API service layer
│   │   ├── types/         # TypeScript type definitions
│   │   └── App.tsx        # Main application component
│   ├── package.json       # Dependencies and scripts
│   └── public/            # Static assets
├── server/                # FastAPI backend application
│   ├── app/               # Application code
│   │   ├── main.py        # FastAPI application and routes
│   │   ├── models.py      # SQLAlchemy database models
│   │   ├── schemas.py     # Pydantic request/response schemas
│   │   ├── database.py    # Database configuration
│   │   ├── ai_service.py  # AI conversation logic
│   │   ├── knowledge_base_service.py  # Knowledge base search
│   │   └── config_loader.py  # Configuration management
│   ├── config/            # Configuration files
│   │   ├── ai_prompts_config.yaml    # AI prompts and responses
│   │   ├── knowledge_base_config.yaml # Knowledge base settings
│   │   └── knowledge_bases/          # Knowledge base files
│   │       └── automotive_en.txt     # Automotive Q&A content
│   ├── requirements.txt   # Python dependencies
│   ├── .env               # Environment variables
│   └── run.py            # Application entry point
├── tests/                 # Test suite
├── faq_system.db         # SQLite database file
├── README.md             # This documentation
└── TECHNICAL.md          # Detailed technical documentation
```

## Documentation

- **[TECHNICAL.md](TECHNICAL.md)** - Comprehensive technical guide
- **[tests/README.md](tests/README.md)** - Testing documentation
- **API Docs** - http://localhost:8000/docs (when running)

## Key Technologies

- **Frontend:** React 18 + TypeScript + Ant Design 5.x + React Router
- **Backend:** FastAPI + SQLAlchemy (Async) + SQLite + Pydantic
- **AI Service:** Ollama + DeepSeek-R1:1.5b model with fallback responses
- **Knowledge Base:** TF-IDF vectorization + Cosine similarity matching + Plain text format
- **Session Management:** Email-based persistent sessions with SQLite storage
- **Configuration:** YAML-based configuration with hot reloading
- **Development:** Python 3.8+ + Node.js 16+ + TypeScript + ESLint

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
