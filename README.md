# Customer FAQ System 🚗💬

An intelligent automotive customer service FAQ system with AI chat and ticket management functionality.

## Product Description

This is a modern customer service system designed specifically for automotive sales scenarios:

### Core Features
- **🤖 Intelligent Q&A**: Smart responses based on knowledge base, covering common automotive sales questions
- **💬 Real-time Chat**: Support for session management, maintaining chat history
- **🎟️ Ticket System**: Automatically creates tickets for human customer service when AI cannot provide answers
- **📚 Knowledge Base**: Professional automotive sales knowledge base with similarity matching
- **🔍 Ticket Management**: Complete ticket viewing and status management functionality

### Technical Features
- **Hybrid Intelligence**: Knowledge base retrieval + AI generation for accurate and human-like responses
- **Auto Escalation**: Smart determination of when human customer service intervention is needed
- **Session Persistence**: Complete conversation history and context management
- **RESTful API**: Standardized interface design, easy for frontend integration

## Quick Start

### Requirements
- Python 3.8+
- No external AI API required (uses local AI)

### Installation Steps

1. **Clone Project**
```bash
git clone <repository-url>
cd FAQ-system
```

2. **Install Dependencies**
```bash
cd server
pip install -r requirements.txt
```

3. **Configure Environment Variables (Optional)**
```bash
cp .env.example .env
# Edit .env file if needed (database URL, etc.)
```

`.env` file content:
```
DATABASE_URL=sqlite+aiosqlite:///./faq_system.db
```

4. **Start Service**
```bash
# Method 1: Using run script (recommended)
python run.py

# Method 2: Direct uvicorn
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Access Service**
- API Documentation: http://localhost:8000/docs
- Service Endpoint: http://localhost:8000

6. **Test Local AI (Optional)**
```bash
# Test the local AI system
cd server
python test_local_ai.py
```

7. **Run Demo (Optional)**
```bash
# Run the demo script to test functionality
python demo_example.py
```

## Configuration System

The system now uses external configuration files for easy customization:

### Configuration Files
- `server/config/knowledge_base_config.yaml` - Knowledge base settings and topics
- `server/config/ai_prompts_config.yaml` - AI prompts and response templates
- `server/config/knowledge_bases/` - Knowledge base content files

### Switching Knowledge Bases
```bash
# Switch to Chinese knowledge base
curl -X POST "http://localhost:8000/config/switch-kb/automotive_cn"

# Switch back to English
curl -X POST "http://localhost:8000/config/switch-kb/automotive_en"
```

### Reloading Configuration
```bash
# Reload configs without restarting server
curl -X POST "http://localhost:8000/config/reload"
```

## Usage Guide

### API Endpoints

#### Chat Interface
```bash
POST /chat
Content-Type: application/json

{
  "message": "Should I buy a new car or used car?",
  "user_contact": "user@example.com",
  "session_id": "optional-session-id"
}
```

Response example:
```json
{
  "response": "This depends on your budget and needs. New cars have warranties...",
  "session_id": "generated-uuid",
  "is_from_kb": true,
  "ticket_created": false,
  "ticket_id": null
}
```

#### Ticket Management
```bash
# Get all tickets
GET /tickets

# Get specific ticket
GET /tickets/{ticket_id}

# Update ticket status
PUT /tickets/{ticket_id}/status?status=in_progress
```

#### Chat History
```bash
GET /chat/history/{session_id}
```

#### Knowledge Base View
```bash
GET /knowledge-base
```

### Testing

Run test suite:
```bash
# In server directory
pytest tests/ -v
```

Test coverage:
- Basic API endpoint testing
- Chat functionality end-to-end testing
- Ticket creation and management testing
- Database integration testing

## System Workflow

```
User Question → Knowledge Base Search → AI Processing → Response Generation
    ↓
If Human Service Needed → Create Ticket → Customer Service Follow-up
```

### Ticket Creation Logic
The system automatically creates tickets in the following situations:
- AI explicitly indicates human follow-up needed
- User question contains complaint, legal, dispute keywords
- Knowledge base cannot match and AI is uncertain about answer

## Knowledge Base Content

Current knowledge base contains automotive sales content in the following areas:
- Car buying advice and considerations
- Car selling best practices and risk prevention
- Car insurance selection guide
- Car loan options comparison
- Maintenance and repair basics
- Electric and hybrid vehicle information
- Safety and technology features

## Technical Architecture

### Backend Technology Stack
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM database operations
- **SQLite**: Lightweight database
- **Local AI**: Keyword-based intelligent responses (no external API)
- **scikit-learn**: Knowledge base similarity matching

### Database Models
- `ChatSession`: Session management
- `ChatMessage`: Chat records
- `Ticket`: Ticket system

### AI Integration
- Knowledge base uses TF-IDF vectorization for semantic matching
- Local keyword-matching AI for intelligent responses
- Template-based responses with context awareness
- No external API dependencies - completely free to run

## Development Notes

### Project Structure
```
server/
├── app/
│   ├── main.py              # FastAPI main application
│   ├── database.py          # Database configuration
│   ├── models.py            # Data models
│   ├── schemas.py           # API schemas
│   ├── ai_service.py        # AI service
│   ├── knowledge_base_service.py  # Knowledge base service
│   └── config_loader.py     # Configuration management
├── config/                  # External configuration files
│   ├── knowledge_base_config.yaml    # KB settings
│   ├── ai_prompts_config.yaml       # AI prompts and templates
│   └── knowledge_bases/             # Knowledge base files
│       ├── automotive_en.txt        # English automotive FAQ
│       ├── automotive_cn.txt        # Chinese automotive FAQ
│       └── electronics_en.txt       # Electronics FAQ (example)
├── tests/                   # Test files
├── requirements.txt         # Dependencies
├── run.py                   # Startup script
├── .env.example            # Environment variable template
└── API_GUIDE.md            # Detailed API documentation
```

### Extension Suggestions
- Add more domain-specific knowledge bases
- Implement real-time message pushing
- Add user authentication system
- Integrate additional AI models
- Add data analytics dashboard

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Check if API Key is correctly set
   - Verify account has sufficient balance

2. **Database Connection Issues**
   - Ensure SQLite file permissions are correct
   - Check DATABASE_URL configuration

3. **Dependency Installation Failures**
   - Use virtual environment: `python -m venv venv && source venv/bin/activate`
   - Upgrade pip: `pip install --upgrade pip`

## Contact Us

For questions or suggestions, please contact us through:
- Create GitHub Issues
- Email project maintainers

---

*This project is for learning and demonstration purposes, showcasing best practices for AI-driven customer service systems.*