#!/usr/bin/env python3
"""
Test script to verify end_chat functionality
"""

import asyncio
import aiohttp
import json

async def test_end_chat():
    """Test end_chat button choice"""
    
    async with aiohttp.ClientSession() as session:
        print("🧪 Testing End Chat Functionality")
        print("=" * 40)
        
        # Step 1: Create session and trigger choice buttons
        session_id = None
        user_contact = "end_chat_test@example.com"
        
        # Send 3 unclear messages to trigger choice
        for i, message in enumerate(["help", "what", "info"]):
            print(f"Sending unclear message {i+1}: '{message}'")
            
            payload = {
                "message": message,
                "user_contact": user_contact,
                "session_id": session_id
            }
            
            async with session.post("http://localhost:8000/chat", json=payload) as resp:
                if resp.status != 200:
                    print(f"❌ Error: {resp.status}")
                    return False
                
                data = await resp.json()
                session_id = data["session_id"]
                
                if i == 2 and "CHOICE_BUTTONS_START" in data['response']:
                    print("✅ Choice buttons appeared!")
                    break
        
        # Step 2: Test end_chat choice
        print(f"\nTesting 'end_chat' choice with session_id: {session_id}")
        
        payload = {
            "message": "end_chat",
            "user_contact": user_contact,
            "session_id": session_id
        }
        
        async with session.post("http://localhost:8000/chat", json=payload) as resp:
            if resp.status != 200:
                print(f"❌ Error: {resp.status}")
                return False
            
            data = await resp.json()
            
            print(f"Chat ended: {data.get('chat_ended', False)}")
            print(f"Ticket created: {data.get('ticket_created', False)}")
            print(f"Response: {data['response'][:150]}...")
            
            if data.get('chat_ended'):
                print("✅ Chat ended successfully!")
                
                # Step 3: Test that further messages are handled properly
                print("\n🔍 Testing chat after end_chat...")
                
                payload = {
                    "message": "Can I send more messages?",
                    "user_contact": user_contact,
                    "session_id": session_id
                }
                
                async with session.post("http://localhost:8000/chat", json=payload) as resp:
                    if resp.status != 200:
                        print(f"❌ Error: {resp.status}")
                        return False
                    
                    data2 = await resp.json()
                    print(f"After end_chat - Chat ended: {data2.get('chat_ended', False)}")
                    print(f"After end_chat - Response: {data2['response'][:100]}...")
                
                return True
            else:
                print("❌ Chat did not end!")
                return False

async def main():
    try:
        success = await test_end_chat()
        if success:
            print("\n🎉 End chat functionality is working!")
        else:
            print("\n💥 End chat functionality is broken!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())