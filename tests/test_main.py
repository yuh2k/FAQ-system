import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import app
from database import Base, get_db
from models import ChatSession, ChatMessage, Ticket

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_faq_system.db"

@pytest_asyncio.fixture
async def test_db():
    """Create test database"""
    engine = create_async_engine(TEST_DATABASE_URL)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async def override_get_db():
        async with TestSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(test_db):
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Customer FAQ System API"
    assert data["version"] == "1.0.0"

@pytest.mark.asyncio
async def test_knowledge_base_endpoint(client: AsyncClient):
    """Test knowledge base endpoint"""
    response = await client.get("/knowledge-base")
    assert response.status_code == 200
    data = response.json()
    assert "qa_pairs" in data
    assert len(data["qa_pairs"]) > 0

@pytest.mark.asyncio
async def test_chat_endpoint_with_kb_match(client: AsyncClient):
    """Test chat endpoint - knowledge base match"""
    chat_data = {
        "message": "Should I buy a new car or used car?",
        "user_contact": "test@example.com"
    }
    
    response = await client.post("/chat", json=chat_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert isinstance(data["is_from_kb"], bool)
    assert isinstance(data["ticket_created"], bool)

@pytest.mark.asyncio
async def test_chat_endpoint_create_session(client: AsyncClient):
    """Test chat endpoint - create session"""
    chat_data = {
        "message": "Hello",
        "user_contact": "test@example.com"
    }
    
    response = await client.post("/chat", json=chat_data)
    assert response.status_code == 200
    
    data = response.json()
    session_id = data["session_id"]
    
    # Test chat history
    history_response = await client.get(f"/chat/history/{session_id}")
    assert history_response.status_code == 200
    
    history_data = history_response.json()
    assert len(history_data) >= 1
    assert history_data[0]["message"] == "Hello"

@pytest.mark.asyncio
async def test_tickets_endpoint(client: AsyncClient):
    """Test tickets endpoint"""
    # Get initial ticket list (should be empty)
    response = await client.get("/tickets")
    assert response.status_code == 200
    initial_tickets = response.json()
    
    # Send a message that might create a ticket
    chat_data = {
        "message": "I want to file a complaint about this car",
        "user_contact": "complainant@example.com"
    }
    
    chat_response = await client.post("/chat", json=chat_data)
    assert chat_response.status_code == 200
    
    # Check ticket list again
    response = await client.get("/tickets")
    assert response.status_code == 200
    tickets = response.json()
    
    if len(tickets) > len(initial_tickets):
        # If ticket was created, test getting single ticket
        ticket_id = tickets[0]["id"]
        ticket_response = await client.get(f"/tickets/{ticket_id}")
        assert ticket_response.status_code == 200
        
        # Test updating ticket status
        status_update = await client.put(
            f"/tickets/{ticket_id}/status", 
            params={"status": "in_progress"}
        )
        assert status_update.status_code == 200

@pytest.mark.asyncio
async def test_invalid_endpoints(client: AsyncClient):
    """Test invalid endpoints"""
    # Test non-existent ticket
    response = await client.get("/tickets/999999")
    assert response.status_code == 404
    
    # Test invalid status update
    response = await client.put("/tickets/1/status", params={"status": "invalid_status"})
    assert response.status_code in [400, 404]  # Could be 400 or 404 depending on ticket existence