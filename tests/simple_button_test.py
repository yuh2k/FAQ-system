#!/usr/bin/env python3
"""
Simple test to debug button choice detection
"""

import asyncio
import aiohttp
import json

async def test_button_choice():
    """Test the button choice directly"""
    
    async with aiohttp.ClientSession() as session:
        print("🔍 Testing Button Choice Detection")
        print("=" * 40)
        
        # Step 1: Create a session that's already in waiting_for_choice state
        # We'll do this by sending 3 unclear messages first
        session_id = None
        user_contact = "button_test@example.com"
        
        # Send 3 unclear messages
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
                
                if i == 2:  # After 3rd message
                    print(f"Response: {data['response'][:100]}...")
                    if "CHOICE_BUTTONS_START" in data['response']:
                        print("✅ Choice buttons appeared!")
                        break
                    else:
                        print("❌ Choice buttons didn't appear")
                        return False
        
        # Step 2: Now test the create_ticket choice
        print(f"\nTesting 'create_ticket' choice with session_id: {session_id}")
        
        payload = {
            "message": "create_ticket",
            "user_contact": user_contact,
            "session_id": session_id
        }
        
        async with session.post("http://localhost:8000/chat", json=payload) as resp:
            if resp.status != 200:
                print(f"❌ Error: {resp.status}")
                return False
            
            data = await resp.json()
            
            print(f"Ticket created: {data.get('ticket_created', False)}")
            print(f"Ticket ID: {data.get('ticket_id', 'None')}")
            print(f"Response: {data['response'][:200]}...")
            
            if data.get('ticket_created'):
                print("✅ Button choice worked!")
                return True
            else:
                print("❌ Button choice failed!")
                return False

async def main():
    try:
        success = await test_button_choice()
        if success:
            print("\n🎉 Button choice is working!")
        else:
            print("\n💥 Button choice is broken!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())