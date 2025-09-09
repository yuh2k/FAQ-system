from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_contact: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    is_from_kb: bool
    ticket_created: bool = False
    ticket_id: Optional[int] = None
    chat_ended: bool = False

class TicketCreate(BaseModel):
    session_id: str
    user_question: str
    user_contact: Optional[str] = None
    ai_attempted_response: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    session_id: str
    user_question: str
    user_contact: Optional[str]
    status: str
    ai_attempted_response: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True