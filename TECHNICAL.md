# Technical Documentation

Comprehensive technical guide for the Customer FAQ System.

## Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React.js      │    │   FastAPI       │    │   SQLite        │
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
- React.js 18+ with TypeScript
- Ant Design UI components
- Axios for HTTP requests
- React hooks for state management

**Backend:**
- FastAPI (Python) with async/await
- SQLAlchemy ORM with async support
- Pydantic for data validation
- SQLite database

**AI Service:**
- Ollama local inference server
- DeepSeek-R1 1.5B parameter model
- Custom prompt engineering
- Vector similarity search

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

**Adding Knowledge Bases** (`server/config/knowledge_bases/`):
```
# Format:
Q: What is your return policy?
A: return policy allows returns within 30 days of purchase.
```

**AI Prompts Configuration** (`server/config/ai_prompts.yaml`):
```yaml
system_prompt: |
  You are a helpful customer service assistant. Always be polite and professional.
  
guidance_prompts:
  round_1: "I'd like to help you! Could you please be more specific about what you're looking for?"
  round_2: "I'm still not quite sure how to help. Could you provide more details?"
  round_3: "I'm having difficulty understanding your specific needs. You have two options:"
  
choice_buttons: |
  **CHOICE_BUTTONS_START**
  CREATE_TICKET|Create a support ticket - I'll connect you with a human agent
  END_CHAT|End this conversation - I'll close our chat session
  **CHOICE_BUTTONS_END**
```

#### Frontend Configuration

**API Configuration** (`frontend/src/services/api.ts`):
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

**Theme Configuration** (`frontend/src/App.tsx`):
```typescript
const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
  },
};
```

## Development Guide

### Project Structure

```
FAQ-system/
├── setup.sh                     # One-click setup script
├── start.sh                     # Start all services
├── stop.sh                      # Stop all services
├── README.md                    # Main documentation
├── TECHNICAL.md                 # This file
│
├── frontend/                    # React.js application
│   ├── public/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── SessionHistory.tsx
│   │   │   └── TicketList.tsx
│   │   ├── services/           # API services
│   │   │   └── api.ts
│   │   ├── types/              # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx             # Main app component
│   │   └── index.tsx           # Entry point
│   ├── package.json
│   └── tsconfig.json
│
├── server/                      # FastAPI application
│   ├── app/
│   │   ├── main.py             # FastAPI app and routes
│   │   ├── ai_service.py       # AI logic and conversation handling
│   │   ├── models.py           # SQLAlchemy database models
│   │   ├── schemas.py          # Pydantic request/response schemas
│   │   ├── database.py         # Database configuration
│   │   ├── knowledge_base_service.py # Knowledge base operations
│   │   └── config_loader.py    # Configuration loading
│   ├── config/
│   │   ├── config.yaml         # System configuration
│   │   ├── ai_prompts.yaml     # AI prompting configuration
│   │   └── knowledge_bases/    # Q&A knowledge base files
│   │       ├── automotive_en.txt
│   │       └── general_en.txt
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                  # Server startup script
│   └── migrate_db.py           # Database migration script
│
└── tests/                      # Test suite
    ├── test_api.py             # API endpoint tests
    ├── test_ai_logic.py        # AI service tests
    ├── test_integration.py     # Integration tests
    ├── test_end_chat.py        # End chat functionality tests
    ├── test_button_choices.py  # Button interaction tests
    ├── run_all.py              # Test runner
    └── README.md               # Test documentation
```

### Database Schema

#### Tables

**chat_sessions**
```sql
CREATE TABLE chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR NOT NULL UNIQUE,
    user_contact VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    unclear_message_count INTEGER DEFAULT 0,
    guidance_stage VARCHAR DEFAULT 'normal'
);
```

**chat_messages**
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    is_from_kb BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
);
```

**tickets**
```sql
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR NOT NULL,
    user_question TEXT NOT NULL,
    user_contact VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'open',
    ai_attempted_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
);
```

### API Documentation

#### Authentication
No authentication required for this demo system.

#### Request/Response Format
All API requests and responses use JSON format.

#### Error Handling
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

#### Rate Limiting
No rate limiting implemented in current version.

### Adding New Features

#### Adding New API Endpoint
1. Define Pydantic schema in `server/app/schemas.py`
2. Add route handler in `server/app/main.py`
3. Add database operations if needed
4. Create frontend service function in `frontend/src/services/api.ts`
5. Add tests in appropriate test file

#### Adding New React Component
1. Create component in `frontend/src/components/`
2. Add TypeScript types in `frontend/src/types/index.ts`
3. Import and use in parent component
4. Add styling as needed

#### Modifying AI Behavior
1. Update prompts in `server/config/ai_prompts.yaml`
2. Modify logic in `server/app/ai_service.py`
3. Test with `tests/test_ai_logic.py`

#### Adding New Knowledge Base
1. Create new file in `server/config/knowledge_bases/`
2. Use format: `Question|Answer` per line
3. Switch via API: `POST /config/switch-kb/{kb_name}`

### Testing

#### Test Categories

**Unit Tests:**
- Individual function testing
- Mock external dependencies
- Fast execution

**Integration Tests:**
- Component interaction testing
- Database operations
- API endpoint testing

**End-to-End Tests:**
- Complete user workflows
- Browser automation (if needed)
- Full system testing

#### Running Tests

**All Tests:**
```bash
python tests/run_all.py
```

**Specific Test Categories:**
```bash
# API tests
python tests/test_api.py

# AI logic tests
python tests/test_ai_logic.py

# Integration tests
python tests/test_integration.py

# Feature-specific tests
python tests/test_end_chat.py
python tests/test_button_choices.py
```

**With Coverage:**
```bash
pip install pytest-cov
pytest tests/ --cov=server/app --cov-report=html
```

### Deployment

#### Production Considerations

**Backend:**
- Use production ASGI server (Gunicorn + Uvicorn)
- Configure proper database (PostgreSQL)
- Set up environment variables
- Configure logging
- Set up monitoring

**Frontend:**
- Build production bundle: `npm run build`
- Serve with nginx or similar
- Configure proper base URL
- Set up CDN for static assets

**AI Service:**
- Consider GPU acceleration for better performance
- Set up model caching
- Configure resource limits

#### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost/dbname
OLLAMA_BASE_URL=http://localhost:11434
AI_MODEL=deepseek-r1:1.5b

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## Troubleshooting

### Common Issues

#### Ollama Issues
```bash
# Check if Ollama is running
pgrep -f "ollama serve"

# Check available models
ollama list

# Check Ollama logs
journalctl -u ollama

# Restart Ollama
pkill ollama && ollama serve
```

#### Backend Issues
```bash
# Check Python version
python3 --version

# Check if virtual environment is activated
which python

# Check installed packages
pip list

# Check database file permissions
ls -la faq_system.db

# View backend logs
tail -f server/logs/app.log
```

#### Frontend Issues
```bash
# Check Node.js version
node --version

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
lsof -i :3000
```

#### Database Issues
```bash
# Recreate database
rm faq_system.db
python server/app/database.py

# Check database schema
sqlite3 faq_system.db ".schema"

# View table contents
sqlite3 faq_system.db "SELECT * FROM chat_sessions LIMIT 5;"
```

### Performance Optimization

#### Backend Optimization
- Use database connection pooling
- Implement caching for knowledge base queries
- Optimize AI model loading
- Add request compression

#### Frontend Optimization
- Implement lazy loading for components
- Use React.memo for expensive components
- Optimize bundle size
- Add service worker for caching

#### AI Service Optimization
- Use GPU acceleration if available
- Implement model quantization
- Add response caching
- Optimize prompt length

### Security Considerations

#### Input Validation
- Sanitize all user inputs
- Validate email formats
- Limit message length
- Prevent SQL injection

#### API Security
- Add rate limiting
- Implement authentication
- Use HTTPS in production
- Validate request origins

#### Data Privacy
- Encrypt sensitive data
- Implement data retention policies
- Add user data deletion capabilities
- Follow GDPR compliance

### Monitoring and Logging

#### Application Monitoring
- Add health check endpoints
- Monitor response times
- Track error rates
- Monitor resource usage

#### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

#### Metrics Collection
- Request/response metrics
- AI model performance
- Database query performance
- User interaction patterns
