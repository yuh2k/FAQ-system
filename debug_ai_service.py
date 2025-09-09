#!/usr/bin/env python3
"""
Debug script to test AI service unclear intent detection
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server', 'app'))

from ai_service import AIService

def test_unclear_detection():
    """Test unclear intent detection"""
    
    ai_service = AIService()
    
    test_messages = [
        "I need help",
        "What?", 
        "Something",
        "hello",
        "I have a problem with my car",
        "help me"
    ]
    
    print("🔍 Testing Unclear Intent Detection")
    print("=" * 40)
    
    for message in test_messages:
        is_unclear = ai_service._is_unclear_intent(message, kb_found=False)
        print(f"Message: '{message}' -> Unclear: {is_unclear}")
    
    print("\n🧪 Testing session state flow")
    print("=" * 40)
    
    # Simulate 3-round conversation
    session_state = {
        'unclear_message_count': 0,
        'guidance_stage': 'normal'
    }
    
    for i, message in enumerate(["help", "what", "info"]):
        print(f"\nRound {i+1}: '{message}'")
        print(f"Before - Count: {session_state['unclear_message_count']}, Stage: {session_state['guidance_stage']}")
        
        # Simulate what happens in main.py
        is_unclear = ai_service._is_unclear_intent(message, kb_found=False)
        print(f"Unclear intent detected: {is_unclear}")
        
        if is_unclear:
            session_state['unclear_message_count'] += 1
            if session_state['unclear_message_count'] >= 3:
                session_state['guidance_stage'] = 'waiting_for_choice'
            elif session_state['unclear_message_count'] >= 1:
                session_state['guidance_stage'] = 'guiding'
        else:
            session_state['unclear_message_count'] = 0
            session_state['guidance_stage'] = 'normal'
            
        print(f"After  - Count: {session_state['unclear_message_count']}, Stage: {session_state['guidance_stage']}")

if __name__ == "__main__":
    test_unclear_detection()