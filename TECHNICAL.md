# FAQ System - Technical Documentation

## Architecture Overview

### System Design Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
├─────────────────────────────────────────────────────────────────┤
│  React Frontend (Port 3000)                                    │
│  ├── Chat Interface    ├── Ticket List    ├── Knowledge Base   │
│  └── Message Bubbles   └── Ticket Modal   └── Search/Browse    │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/REST API
┌─────────────────────────▼───────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)                  │
├─────────────────────────────────────────────────────────────────┤
│  API Endpoints:                                                 │
│  ├── /chat              ├── /tickets           ├── /knowledge-base │
│  ├── /chat/history      ├── /tickets/{id}      └── /config      │
│  └── Main Routes        └── Ticket Management                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌─────────────┐  ┌─────────────────┐  ┌──────────────┐
│  Database   │  │   AI Service    │  │ Config Files │
│  (SQLite)   │  │  (Local LLM)    │  │   (YAML)     │
├─────────────┤  ├─────────────────┤  ├──────────────┤
│• Sessions   │  │• Ollama API     │  │• KB Settings │
│• Messages   │  │• DeepSeek Model │  │• AI Prompts  │
│• Tickets    │  │• Response Gen   │  │• Templates   │
└─────────────┘  └─────────┬───────┘  └──────────────┘
                           │
                           ▼
                 ┌─────────────────┐
                 │ Knowledge Base  │
                 │   (TF-IDF)      │
                 ├─────────────────┤
                 │• Automotive Q&A │
                 │• Similarity     │
                 │• Vector Match   │
                 └─────────────────┘
```

### Data Flow
```
User Input → Frontend → API Endpoint → AI Service → Knowledge Base Search
    ↓                                      ↓              ↓
Response ← Frontend ← JSON Response ← LLM Processing ← Similarity Match
    ↓
[If Needs Ticket] → Database → Ticket Creation → Return Ticket ID
```

### System Components
- **Frontend**: React + TypeScript + Ant Design (Port 3000)  
- **Backend**: FastAPI + Python (Port 8000)
- **Database**: SQLite for persistence
- **AI Service**: Ollama local LLM integration  
- **Knowledge Base**: TF-IDF vectorized Q&A matching

### Key Technologies
**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- SQLite (database)
- Ollama (local LLM)
- scikit-learn (text similarity)

**Frontend:**
- React 18 + TypeScript
- Ant Design (UI components)
- Axios (HTTP client)

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama (for AI features)

### Installation
```bash
# 1. Start Ollama
ollama serve

# 2. Pull required model
ollama pull deepseek-r1:1.5b

# 3. Backend setup
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# 4. Frontend setup (new terminal)
cd frontend
npm install
npm start
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## System Design

### Database Schema
```sql
-- Chat sessions
CREATE TABLE chat_sessions (
    id VARCHAR PRIMARY KEY,
    user_contact VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    is_from_kb BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id)
);

-- Support tickets
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR NOT NULL,
    user_contact VARCHAR NOT NULL,
    user_question TEXT NOT NULL,
    ai_attempted_response TEXT NOT NULL,
    status VARCHAR DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id)
);
```

### API Endpoints

#### Core Chat API
```http
POST /chat
{
    "message": "user question",
    "user_contact": "user@email.com",
    "session_id": "optional-uuid"
}
→ {
    "response": "ai response",
    "session_id": "uuid",
    "is_from_kb": boolean,
    "ticket_created": boolean,
    "ticket_id": number|null
}
```

#### Knowledge Base API
```http
GET /knowledge-base
→ {
    "qa_pairs": [{"question": "...", "answer": "..."}],
    "total": number
}

GET /knowledge-base/available
→ {
    "available_kbs": ["automotive_en", "automotive_cn"]
}

POST /knowledge-base/switch/{kb_name}
→ {
    "message": "switched to {kb_name}",
    "success": true
}
```

#### Ticket Management API
```http
GET /tickets
→ [{"id": 1, "status": "open", "user_question": "...", ...}]

GET /tickets/{ticket_id}
→ {"id": 1, "status": "open", "user_question": "...", ...}

PUT /tickets/{ticket_id}/status?status=in_progress
→ {"message": "Ticket status updated", "success": true}
```

#### Chat History API
```http
GET /chat/history/{session_id}
→ [{"message": "...", "response": "...", "created_at": "...", ...}]
```

## AI Service Flow

### Message Processing Pipeline
1. **Input**: User message + context
2. **Knowledge Base Search**: TF-IDF similarity matching
3. **AI Processing**: 
   - If KB match found: Enhance with LLM
   - If no match: Generate contextual fallback
4. **Response Generation**: Format and return
5. **Ticket Creation**: Auto-create if human followup needed

### Knowledge Base Matching
- Uses TF-IDF vectorization
- Cosine similarity threshold: 0.5
- Fallback to contextual patterns if no match

### Ticket Creation Logic
Tickets are created when:
- Response contains "NEEDS_HUMAN_FOLLOWUP"
- User message contains complaint/problem keywords
- Complex issues requiring human expertise

## Configuration

### Environment Variables
```bash
# Server config
OLLAMA_URL=http://localhost:11434
MODEL_NAME=deepseek-r1:1.5b
DATABASE_URL=sqlite:///./faq_system.db

# Frontend config
REACT_APP_API_URL=http://localhost:8000
```

### Knowledge Base Configuration
Located in `server/config/`:
- `knowledge_base_config.yaml` - KB settings
- `ai_prompts_config.yaml` - AI prompts
- `knowledge_bases/` - KB content files

## Development

### File Structure
```
FAQ-system/
├── frontend/src/
│   ├── components/           # React components
│   ├── services/api.ts      # API client
│   ├── types/index.ts       # TypeScript types
│   └── App.tsx              # Main app
├── server/app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB config
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── ai_service.py        # AI logic
│   └── knowledge_base_service.py # KB logic
└── server/config/           # Configuration files
```

### Testing
```bash
# Backend tests
cd server && pytest tests/ -v

# Frontend tests
cd frontend && npm test

# System integration test
cd server && python test_universal_faq.py
```

### Adding New Knowledge Bases
1. Create content file in `server/config/knowledge_bases/`
2. Add configuration in `knowledge_base_config.yaml`
3. Restart server or call `/config/reload`

### Extending AI Capabilities
- Modify `ai_service.py` for new AI logic
- Update `ai_prompts_config.yaml` for new prompts
- Add new contextual patterns in `LocalAIService`