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
- Node.js 16+ and npm
- No external AI API required (uses local AI)

### 🚀 One-Click Startup (Recommended)

```bash
# Clone the project
git clone <repository-url>
cd FAQ-system

# Start both backend and frontend
./start-system.sh
```

This script will:
- ✅ Check all prerequisites
- ✅ Install backend dependencies (Python packages)
- ✅ Install frontend dependencies (npm packages)
- ✅ Start backend server on http://localhost:8000
- ✅ Start frontend server on http://localhost:3000
- ✅ Open the application in your browser

### Manual Installation (Alternative)

If you prefer to set up manually:

#### Backend Setup
```bash
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

#### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm start
```

### Access the Application

- 🎨 **Frontend UI**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000  
- 📚 **API Documentation**: http://localhost:8000/docs

### Test the System

```bash
# Test universal FAQ system
cd server
python test_universal_faq.py

# Run demo example
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

### Technology Stack

#### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM database operations
- **SQLite**: Lightweight database
- **Local AI**: Keyword-based intelligent responses (no external API)
- **scikit-learn**: Knowledge base similarity matching

#### Frontend
- **React 18**: Modern UI library with TypeScript
- **Ant Design 5**: Beautiful and professional UI components
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing

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
FAQ-system/
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatInterface.tsx     # Main chat UI
│   │   │   ├── MessageBubble.tsx     # Message components
│   │   │   ├── TicketList.tsx        # Ticket management
│   │   │   └── KnowledgeBaseView.tsx # KB browser
│   │   ├── services/
│   │   │   └── api.ts       # Backend API client
│   │   ├── types/
│   │   │   └── index.ts     # TypeScript interfaces
│   │   └── App.tsx          # Main application
│   ├── package.json         # Frontend dependencies
│   └── README.md           # Frontend documentation
├── server/                  # Python Backend
│   ├── app/
│   │   ├── main.py         # FastAPI main application
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # Data models
│   │   ├── schemas.py      # API schemas
│   │   ├── ai_service.py   # AI service
│   │   ├── knowledge_base_service.py  # Knowledge base service
│   │   └── config_loader.py # Configuration management
│   ├── config/             # External configuration files
│   │   ├── knowledge_base_config.yaml    # KB settings
│   │   ├── ai_prompts_config.yaml       # AI prompts
│   │   └── knowledge_bases/ # Knowledge base files
│   ├── tests/              # Test files
│   ├── requirements.txt    # Python dependencies
│   ├── run.py             # Backend startup script
│   └── API_GUIDE.md       # Detailed API documentation
├── start-system.sh         # One-click startup script
└── README.md              # Project documentation
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