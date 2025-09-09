#!/usr/bin/env python3
"""
Test script to verify button choice functionality works correctly.
Tests both create_ticket and end_chat button choices after 3-round guidance.
"""

import asyncio
import aiohttp
import json
import sys

BASE_URL = "http://localhost:8000"

async def test_button_choices():
    """Test that button choices (create_ticket/end_chat) work correctly"""
    
    async with aiohttp.ClientSession() as session:
        print("🧪 Testing Button Choice Functionality")
        print("=" * 50)
        
        # Test 1: Test create_ticket button choice
        print("\n1️⃣ Testing 'create_ticket' button choice...")
        
        # Start a new conversation with unclear messages to trigger guidance
        session_id = None
        user_contact = "test_button@example.com"
        
        # Send 3 unclear messages to reach choice stage
        unclear_messages = [
            "I need help",
            "What?",
            "Something"
        ]
        
        for i, message in enumerate(unclear_messages):
            print(f"   Sending unclear message {i+1}: '{message}'")
            
            payload = {
                "message": message,
                "user_contact": user_contact,
                "session_id": session_id
            }
            
            async with session.post(f"{BASE_URL}/chat", json=payload) as resp:
                if resp.status != 200:
                    print(f"❌ Error sending message: {resp.status}")
                    return False
                
                data = await resp.json()
                session_id = data["session_id"]
                print(f"   AI Response: {data['response'][:100]}...")
                
                # Check if choice buttons appear after 3rd message
                if i == 2 and "CHOICE_BUTTONS_START" in data['response']:
                    print("   ✅ Choice buttons appeared after 3 unclear messages")
                    break
        
        # Now test the create_ticket button choice
        print("\n   Testing 'create_ticket' button choice...")
        
        payload = {
            "message": "create_ticket",
            "user_contact": user_contact,
            "session_id": session_id
        }
        
        async with session.post(f"{BASE_URL}/chat", json=payload) as resp:
            if resp.status != 200:
                print(f"❌ Error with create_ticket choice: {resp.status}")
                return False
            
            data = await resp.json()
            
            if data.get("ticket_created"):
                print(f"   ✅ Ticket created successfully: #{data.get('ticket_id')}")
            else:
                print(f"   ❌ Ticket was not created")
                print(f"   Response: {data['response']}")
                return False
        
        # Test 2: Test end_chat button choice
        print("\n2️⃣ Testing 'end_chat' button choice...")
        
        # Start another conversation
        session_id = None
        
        # Send 3 unclear messages again
        unclear_messages_2 = ["Help", "Info", "Tell me"]
        for i, message in enumerate(unclear_messages_2):
            print(f"   Sending unclear message {i+1}: '{message}'")
            
            payload = {
                "message": message,
                "user_contact": user_contact,
                "session_id": session_id
            }
            
            async with session.post(f"{BASE_URL}/chat", json=payload) as resp:
                if resp.status != 200:
                    print(f"❌ Error sending message: {resp.status}")
                    return False
                
                data = await resp.json()
                session_id = data["session_id"]
                
                if i == 2 and "CHOICE_BUTTONS_START" in data['response']:
                    print("   ✅ Choice buttons appeared after 3 unclear messages")
                    break
        
        # Test the end_chat button choice
        print("\n   Testing 'end_chat' button choice...")
        
        payload = {
            "message": "end_chat",
            "user_contact": user_contact,
            "session_id": session_id
        }
        
        async with session.post(f"{BASE_URL}/chat", json=payload) as resp:
            if resp.status != 200:
                print(f"❌ Error with end_chat choice: {resp.status}")
                return False
            
            data = await resp.json()
            
            # Check if conversation ended appropriately
            if "conversation" in data['response'].lower() and ("end" in data['response'].lower() or "thank" in data['response'].lower()):
                print("   ✅ Conversation ended appropriately")
                print(f"   Response: {data['response']}")
            else:
                print(f"   ❌ Conversation did not end properly")
                print(f"   Response: {data['response']}")
                return False
        
        print("\n🎉 All button choice tests passed!")
        return True

async def main():
    """Main test function"""
    try:
        success = await test_button_choices()
        if success:
            print("\n✅ Button choice functionality is working correctly!")
            sys.exit(0)
        else:
            print("\n❌ Button choice functionality has issues!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())