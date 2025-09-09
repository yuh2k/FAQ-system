import uuid
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dotenv import load_dotenv

from database import get_db, init_db
from models import ChatSession, ChatMessage, Ticket
from schemas import ChatRequest, ChatResponse, TicketResponse
from knowledge_base_service import KnowledgeBaseService
from ai_service import AIService

load_dotenv()

app = FastAPI(title="Customer FAQ System", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
kb_service = KnowledgeBaseService()
ai_service = AIService()

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Customer FAQ System API", "version": "1.0.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """Chat endpoint"""
    
    # Generate or use existing session_id
    session_id = request.session_id or str(uuid.uuid4())
    
    # Create or get chat session
    chat_session = None
    if not request.session_id:
        chat_session = ChatSession(
            session_id=session_id,
            user_contact=request.user_contact
        )
        db.add(chat_session)
        await db.flush()  # Get the new session
    else:
        # Get existing session
        result = await db.execute(select(ChatSession).where(ChatSession.session_id == session_id))
        chat_session = result.scalar_one_or_none()
        
        if not chat_session:
            # Session doesn't exist, create it
            chat_session = ChatSession(
                session_id=session_id,
                user_contact=request.user_contact
            )
            db.add(chat_session)
            await db.flush()
    
    # 1. Search in knowledge base first
    kb_answer, kb_found, _ = kb_service.search_knowledge_base(request.message)
    
    # 2. Prepare session state for AI service
    session_state = {
        'unclear_message_count': chat_session.unclear_message_count,
        'guidance_stage': chat_session.guidance_stage
    }
    
    # 3. Generate AI response
    ai_response, needs_ticket, is_unclear_intent = await ai_service.generate_response(
        request.message, kb_answer, kb_found, session_state
    )
    
    # 4. Update session state if unclear intent was detected
    if is_unclear_intent:
        chat_session.unclear_message_count += 1
        if chat_session.unclear_message_count >= 3:
            chat_session.guidance_stage = 'escalated'
        elif chat_session.unclear_message_count >= 1:
            chat_session.guidance_stage = 'guiding'
    else:
        # Reset unclear count on clear message
        chat_session.unclear_message_count = 0
        chat_session.guidance_stage = 'normal'
    
    # 5. Save conversation record
    chat_message = ChatMessage(
        session_id=session_id,
        message=request.message,
        response=ai_response,
        is_from_kb=kb_found
    )
    db.add(chat_message)
    
    # 6. Create ticket if needed
    ticket_created = False
    ticket_id = None
    
    if needs_ticket or ai_service.should_create_ticket(request.message, ai_response, kb_found):
        ticket = Ticket(
            session_id=session_id,
            user_question=request.message,
            user_contact=request.user_contact,
            ai_attempted_response=ai_response
        )
        db.add(ticket)
        await db.flush()  # Get ticket ID
        ticket_created = True
        ticket_id = ticket.id
        
        # Add ticket information to response
        ticket_message = ai_service.get_ticket_created_message(ticket_id)
        ai_response += f"\n\n{ticket_message}"
    
    await db.commit()
    
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        is_from_kb=kb_found,
        ticket_created=ticket_created,
        ticket_id=ticket_id
    )

@app.get("/tickets")
async def get_tickets(db: AsyncSession = Depends(get_db)):
    """Get all tickets"""
    result = await db.execute(select(Ticket).order_by(Ticket.created_at.desc()))
    tickets = result.scalars().all()
    return [TicketResponse.from_orm(ticket) for ticket in tickets]

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific ticket"""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return TicketResponse.from_orm(ticket)

@app.put("/tickets/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: int, 
    status: str,
    db: AsyncSession = Depends(get_db)
):
    """Update ticket status"""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if status not in ["open", "in_progress", "closed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    ticket.status = status
    ticket.updated_at = datetime.now()
    await db.commit()
    
    return {"message": "Ticket status updated successfully"}

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get chat history"""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = result.scalars().all()
    
    return [
        {
            "message": msg.message,
            "response": msg.response,
            "is_from_kb": msg.is_from_kb,
            "created_at": msg.created_at
        }
        for msg in messages
    ]

@app.get("/sessions/{email}")
async def get_user_sessions(email: str, db: AsyncSession = Depends(get_db)):
    """Get all sessions for a user by email"""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_contact == email)
        .order_by(ChatSession.created_at.desc())
    )
    sessions = result.scalars().all()
    
    return [
        {
            "session_id": session.session_id,
            "created_at": session.created_at,
            "updated_at": session.created_at,  # ChatSession doesn't have updated_at field
            "message_count": len(session.messages) if session.messages else 0,
            "last_message": session.messages[-1].message if session.messages else None
        }
        for session in sessions
    ]

@app.get("/knowledge-base")
async def get_knowledge_base():
    """Get knowledge base content"""
    return {"qa_pairs": kb_service.get_all_qa_pairs()}

@app.get("/config/knowledge-bases")
async def get_available_knowledge_bases():
    """Get list of available knowledge bases"""
    return {"available_kbs": kb_service.get_available_knowledge_bases()}

@app.post("/config/switch-kb/{kb_name}")
async def switch_knowledge_base(kb_name: str):
    """Switch to a different knowledge base"""
    try:
        kb_service.switch_knowledge_base(kb_name)
        return {"message": f"Switched to knowledge base: {kb_name}", "qa_pairs": len(kb_service.get_all_qa_pairs())}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to switch knowledge base: {str(e)}")

@app.post("/config/reload")
async def reload_configurations():
    """Reload all configurations"""
    try:
        kb_service.reload_config()
        ai_service.reload_config()
        return {"message": "Configurations reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload config: {str(e)}")

@app.get("/config/status")
async def get_config_status():
    """Get current configuration status"""
    from config_loader import config
    
    kb_config = config.get_knowledge_base_config()
    ai_settings = config.get_ai_settings()
    
    return {
        "current_kb": kb_service.kb_name or "primary",
        "qa_pairs_loaded": len(kb_service.get_all_qa_pairs()),
        "similarity_threshold": kb_config.get('similarity_threshold'),
        "ai_provider": "local_ai",
        "ai_model": ai_settings.get('model'),
        "available_kbs": kb_service.get_available_knowledge_bases(),
        "provider_status": ai_service.get_provider_status()
    }

@app.get("/config/ai-providers")
async def get_ai_providers():
    """Get available AI providers"""
    return ai_service.get_provider_status()

@app.get("/config/ai-status")
async def get_ai_status():
    """Get AI service status"""
    return ai_service.get_provider_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)