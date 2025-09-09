#!/usr/bin/env python3
"""
AI service logic tests
"""

import sys
import os
import asyncio

# Add server app to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server', 'app'))

class AILogicTests:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        
    def log(self, message, status="PASS"):
        symbol = "✅" if status == "PASS" else "❌"
        print(f"{symbol} {message}")
        if status == "PASS":
            self.passed += 1
        else:
            self.failed += 1
    
    async def test_ai_logic(self):
        """Test AI service business logic"""
        print("Testing AI logic...")
        
        try:
            from ai_service import LocalAIService
            ai = LocalAIService()
            
            # Test 1: Greeting doesn't create ticket
            response, needs_ticket, unclear = await ai.generate_response(
                "hello", None, False, {'unclear_message_count': 0, 'guidance_stage': 'normal'}
            )
            if not needs_ticket:
                self.log("Greeting doesn't create ticket")
            else:
                self.log("Greeting incorrectly creates ticket", "FAIL")
            
            # Test 2: Technical question doesn't create ticket
            response, needs_ticket, unclear = await ai.generate_response(
                "What oil should I use?", None, False, 
                {'unclear_message_count': 0, 'guidance_stage': 'normal'}
            )
            if not needs_ticket:
                self.log("Technical question doesn't create ticket")
            else:
                self.log("Technical question incorrectly creates ticket", "FAIL")
            
            # Test 3: Human request creates ticket
            response, needs_ticket, unclear = await ai.generate_response(
                "I want to speak to a human", None, False,
                {'unclear_message_count': 0, 'guidance_stage': 'normal'}
            )
            if needs_ticket:
                self.log("Human request creates ticket")
            else:
                self.log("Human request doesn't create ticket", "FAIL")
            
            # Test 4: 3-round guidance
            response3, ticket3, unclear3 = await ai.generate_response(
                "something", None, False, {'unclear_message_count': 2, 'guidance_stage': 'normal'}
            )
            if "CHOICE_BUTTONS_START" in response3:
                self.log("3rd round shows choice buttons")
            else:
                self.log("3rd round doesn't show choice buttons", "FAIL")
            
            # Test 5: Button choices
            choice_state = {'unclear_message_count': 3, 'guidance_stage': 'waiting_for_choice'}
            
            response_ticket, ticket_choice, _ = await ai.generate_response(
                "create_ticket", None, False, choice_state
            )
            if ticket_choice:
                self.log("CREATE_TICKET button works")
            else:
                self.log("CREATE_TICKET button doesn't work", "FAIL")
            
            response_end, ticket_end, _ = await ai.generate_response(
                "end_chat", None, False, choice_state
            )
            if not ticket_end:
                self.log("END_CHAT button works")
            else:
                self.log("END_CHAT button doesn't work", "FAIL")
                
        except Exception as e:
            self.log(f"AI logic test error: {e}", "FAIL")
        
        return self.passed, self.failed

async def main():
    ai_tests = AILogicTests()
    passed, failed = await ai_tests.test_ai_logic()
    print(f"\nAI Logic Tests: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)