# Customer FAQ System 🤖

A comprehensive AI-powered customer service system with intelligent conversation management, session memory, and smart ticket creation capabilities.

## Features

### Core Functionality
- **Intelligent Chat Interface** - AI-powered conversational assistant using local DeepSeek model
- **Session Management** - Persistent conversation history linked to user email
- **Knowledge Base Integration** - Automatic search and retrieval from configurable Q&A database
- **Smart Ticket Creation** - Context-aware support ticket generation with human escalation
- **3-Round Guidance System** - Progressive user assistance with choice-based resolution

### Advanced Features
- **Button-Based Interactions** - Clickable choices for ticket creation or chat ending
- **Chat Interface Control** - Automatic disabling after chat completion or ticket creation
- **Responsive Design** - Mobile-optimized interface with intuitive navigation
- **Multiple Knowledge Bases** - Switchable knowledge base configurations
- **Real-time Status** - Live AI service and configuration status monitoring

## Quick Start

### Prerequisites
- **Python 3.8+** - For backend API
- **Node.js 16+** - For frontend React application
- **Ollama** - Local AI inference engine ([Download here](https://ollama.ai))

### 1. Setup Ollama and AI Model
```bash
# Start Ollama service
ollama serve

# Download the AI model (in another terminal)
ollama pull deepseek-r1:1.5b
```

### 2. Backend Setup
```bash
# Navigate to project root
cd FAQ-system

# Setup Python virtual environment
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python run.py
```

Backend will be available at: http://localhost:8000

### 3. Frontend Setup
```bash
# Open new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm start
```

Frontend will be available at: http://localhost:3000

## How to Use

### User Workflow
1. **Enter Email Address** - System identifies user and loads conversation history
2. **Select Session** - Choose to continue existing conversation or start new one
3. **Interactive Chat** - Engage with AI assistant for questions and support
4. **Smart Resolution** - System guides unclear requests through 3-round assistance
5. **Choice-Based Actions** - Select to create support ticket or end conversation

### System Behavior
- **Immediate Ticket Creation** - For explicit human contact requests
- **Guided Assistance** - For unclear intents, provides 3 rounds of guidance
- **Knowledge Base Search** - Automatic search for relevant Q&A content
- **Session Persistence** - All conversations saved and retrievable by email

## Project Structure

```
FAQ-system/
├── frontend/                 # React.js frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API service functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── ...
│   └── package.json
│
├── server/                  # FastAPI backend application
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── ai_service.py   # AI logic and conversation handling
│   │   ├── models.py       # Database models (SQLAlchemy)
│   │   ├── schemas.py      # Pydantic request/response schemas
│   │   ├── database.py     # Database configuration and connection
│   │   └── ...
│   ├── config/             # Configuration files
│   │   ├── knowledge_bases/ # Q&A knowledge base files
│   │   ├── ai_prompts.yaml # AI prompting configuration
│   │   └── config.yaml     # System configuration
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Server startup script
│
├── tests/                  # Comprehensive test suite
│   ├── test_api.py         # API endpoint tests
│   ├── test_ai_logic.py    # AI service logic tests
│   ├── test_integration.py # End-to-end integration tests
│   ├── test_end_chat.py    # Chat ending functionality tests
│   ├── test_button_choices.py # Button interaction tests
│   └── run_all.py          # Test runner script
│
└── README.md               # This file
```

## API Endpoints

### Chat Endpoints
- `POST /chat` - Send message and receive AI response
- `GET /chat/history/{session_id}` - Retrieve conversation history

### Session Management
- `GET /sessions/{email}` - Get user's conversation sessions

### Ticket Management
- `GET /tickets` - List all support tickets
- `GET /tickets/{ticket_id}` - Get specific ticket details
- `PUT /tickets/{ticket_id}/status` - Update ticket status

### Knowledge Base
- `GET /knowledge-base` - Get current knowledge base content
- `GET /config/knowledge-bases` - List available knowledge bases
- `POST /config/switch-kb/{kb_name}` - Switch to different knowledge base

### System Configuration
- `GET /config/status` - Get system configuration status
- `POST /config/reload` - Reload configuration files
- `GET /config/ai-status` - Get AI service status

## Testing

### Run All Tests
```bash
# Run comprehensive test suite
python tests/run_all.py
```

### Run Specific Tests
```bash
# Test API endpoints
python tests/test_api.py

# Test AI logic
python tests/test_ai_logic.py

# Test end chat functionality
python tests/test_end_chat.py

# Test button interactions
python tests/test_button_choices.py
```

### Test Requirements
- Backend server running on http://localhost:8000
- Ollama service running with deepseek-r1:1.5b model
- All Python dependencies installed

## Configuration

### Knowledge Base Configuration
- Edit files in `server/config/knowledge_bases/`
- Supports multiple knowledge bases with auto-switching
- Q&A format with automatic similarity matching

### AI Configuration
- Modify `server/config/ai_prompts.yaml` for custom AI behavior
- Adjust conversation logic and response templates
- Configure ticket creation thresholds and user guidance

### System Configuration
- Update `server/config/config.yaml` for system settings
- Database configuration and connection settings
- API configuration and CORS settings

## Development

### Adding New Features
1. **Backend Changes** - Modify files in `server/app/`
2. **Frontend Changes** - Update React components in `frontend/src/`
3. **Database Changes** - Update models in `server/app/models.py`
4. **Add Tests** - Create tests in `tests/` directory

### Database Management
```bash
# Initialize database
python server/app/database.py

# Run migrations (if needed)
python server/migrate_db.py
```

## Troubleshooting

### Common Issues

**AI not responding / getting fallback responses:**
- Ensure Ollama service is running: `ollama serve`
- Verify model is downloaded: `ollama pull deepseek-r1:1.5b`
- Check AI service status: `GET /config/ai-status`

**Database errors:**
- Check if database file exists and is writable
- Ensure proper file permissions
- Review database logs in server output

**Frontend not connecting to backend:**
- Verify backend is running on http://localhost:8000
- Check CORS configuration in `server/app/main.py`
- Ensure no firewall blocking connections

**Tests failing:**
- Ensure both Ollama and backend server are running
- Verify all dependencies are installed
- Check test requirements in `tests/README.md`

## License

This project is for educational and demonstration purposes.