from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    user_contact = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    unclear_message_count = Column(Integer, default=0)
    guidance_stage = Column(String(50), default="normal")  # normal, guiding, escalated
    
    # Relationship to chat messages
    messages = relationship("ChatMessage", foreign_keys="ChatMessage.session_id", primaryjoin="ChatSession.session_id == ChatMessage.session_id")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    message = Column(Text)
    response = Column(Text)
    is_from_kb = Column(Boolean, default=False)  # Whether response came from knowledge base
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    user_question = Column(Text)
    user_contact = Column(String(200))
    status = Column(String(50), default="open")  # open, in_progress, closed
    ai_attempted_response = Column(Text)  # What AI tried to answer
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())