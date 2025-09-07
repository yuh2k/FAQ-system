# Customer FAQ System API Guide

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required. The system uses local AI - no external API keys needed.

---

## 📱 Chat APIs

### 1. Send Chat Message
Start a conversation or continue existing session.

**Endpoint:** `POST /chat`

**curl:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Should I buy a new car or used car?",
    "user_contact": "user@example.com"
  }'
```

**Response:**
```json
{
  "response": "This depends on your budget and needs. New cars come with warranties...",
  "session_id": "uuid-here",
  "is_from_kb": true,
  "ticket_created": false,
  "ticket_id": null
}
```

### 2. Continue Conversation
Use existing session_id to maintain context.

**curl:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What about financing options?",
    "session_id": "your-session-id-here",
    "user_contact": "user@example.com"
  }'
```

### 3. Trigger Ticket Creation
Send a complaint or complex query to test ticket creation.

**curl:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to file a complaint about my recent car purchase",
    "user_contact": "complaint@example.com"
  }'
```

**Expected Response (with ticket):**
```json
{
  "response": "I understand your concern about your recent car purchase...",
  "session_id": "uuid-here",
  "is_from_kb": false,
  "ticket_created": true,
  "ticket_id": 1
}
```

### 4. Get Chat History
Retrieve conversation history for a session.

**curl:**
```bash
curl -X GET "http://localhost:8000/chat/history/your-session-id-here"
```

---

## 🎫 Ticket Management APIs

### 1. Get All Tickets
List all support tickets in the system.

**curl:**
```bash
curl -X GET "http://localhost:8000/tickets"
```

**Response:**
```json
[
  {
    "id": 1,
    "session_id": "uuid-here",
    "user_question": "I want to file a complaint",
    "user_contact": "user@example.com",
    "status": "open",
    "ai_attempted_response": "I understand your concern...",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

### 2. Get Specific Ticket
Retrieve details for a single ticket.

**curl:**
```bash
curl -X GET "http://localhost:8000/tickets/1"
```

### 3. Update Ticket Status
Change ticket status (open, in_progress, closed).

**curl:**
```bash
curl -X PUT "http://localhost:8000/tickets/1/status?status=in_progress"
```

**Response:**
```json
{
  "message": "Ticket status updated successfully"
}
```

---

## 📚 Knowledge Base APIs

### 1. View Knowledge Base Content
Get all Q&A pairs currently loaded.

**curl:**
```bash
curl -X GET "http://localhost:8000/knowledge-base"
```

**Response:**
```json
{
  "qa_pairs": [
    {
      "question": "Should I buy a new car or used car?",
      "answer": "This depends on your budget and needs..."
    }
  ]
}
```

### 2. Get Available Knowledge Bases
See what knowledge bases are configured.

**curl:**
```bash
curl -X GET "http://localhost:8000/config/knowledge-bases"
```

**Response:**
```json
{
  "available_kbs": ["automotive_en", "automotive_cn", "electronics"]
}
```

---

## ⚙️ Configuration APIs

### 1. Switch Knowledge Base
Change to a different knowledge base (e.g., Chinese version).

**curl:**
```bash
curl -X POST "http://localhost:8000/config/switch-kb/automotive_cn"
```

**Response:**
```json
{
  "message": "Switched to knowledge base: automotive_cn",
  "qa_pairs": 15
}
```

### 2. Reload Configuration
Reload all config files without restarting server.

**curl:**
```bash
curl -X POST "http://localhost:8000/config/reload"
```

**Response:**
```json
{
  "message": "Configurations reloaded successfully"
}
```

### 3. Get Configuration Status
Check current system configuration.

**curl:**
```bash
curl -X GET "http://localhost:8000/config/status"
```

**Response:**
```json
{
  "current_kb": "automotive_en",
  "qa_pairs_loaded": 50,
  "similarity_threshold": 0.3,
  "ai_model": "gpt-3.5-turbo",
  "available_kbs": ["automotive_en", "automotive_cn"]
}
```

---

## 🏠 System APIs

### 1. Health Check
Verify server is running.

**curl:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Customer FAQ System API",
  "version": "1.0.0"
}
```

---

## 🧪 Testing Scenarios

### Complete Chat Flow Test
```bash
# 1. Start conversation
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need help with car buying", "user_contact": "test@example.com"}'

# 2. Ask knowledge base question  
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Should I buy new or used?", "session_id": "YOUR_SESSION_ID", "user_contact": "test@example.com"}'

# 3. Create ticket with complaint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a legal dispute with the dealer", "session_id": "YOUR_SESSION_ID", "user_contact": "test@example.com"}'

# 4. Check tickets created
curl -X GET "http://localhost:8000/tickets"
```

### Configuration Testing
```bash
# 1. Check current status
curl -X GET "http://localhost:8000/config/status"

# 2. Switch to Chinese knowledge base
curl -X POST "http://localhost:8000/config/switch-kb/automotive_cn"

# 3. Test with Chinese question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "买新车还是二手车好？", "user_contact": "test@example.com"}'

# 4. Switch back to English
curl -X POST "http://localhost:8000/config/switch-kb/automotive_en"
```

---

## 🔧 Configuration Files

### Knowledge Base Config
Edit `server/config/knowledge_base_config.yaml` to:
- Change similarity threshold
- Add new knowledge bases
- Modify urgent keywords
- Set fallback responses

### AI Prompts Config  
Edit `server/config/ai_prompts_config.yaml` to:
- Customize system prompts
- Change AI model settings
- Modify response templates
- Adjust ticket creation logic

### Adding New Knowledge Base
1. Create new file in `server/config/knowledge_bases/`
2. Update `knowledge_base_config.yaml` to include it
3. Use switch API to activate it

---

## 🐞 Troubleshooting

**Common Issues:**

1. **500 Error on /chat**
   - Verify config files are valid YAML
   - Check database permissions

2. **Empty Knowledge Base**
   - Check file paths in config
   - Ensure Q&A format is correct (**Q:** ... **A:** ...)

3. **Config Not Loading**
   - Restart server or use `/config/reload`
   - Check YAML syntax

**Debug Endpoints:**
- `GET /config/status` - Check current config
- `GET /docs` - Interactive API documentation
- Server logs will show config loading details

---

Ready to test! Start the server and try these APIs with Postman or curl. 🚀