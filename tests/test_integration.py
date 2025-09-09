#!/usr/bin/env python3
"""
Integration tests for complete workflows
"""

import asyncio
import aiohttp
import json

class IntegrationTests:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        
    def log(self, message, status="PASS"):
        symbol = "✅" if status == "PASS" else "❌"
        print(f"{symbol} {message}")
        if status == "PASS":
            self.passed += 1
        else:
            self.failed += 1
    
    async def test_complete_workflows(self):
        """Test complete user workflows"""
        print("Testing integration workflows...")
        
        async with aiohttp.ClientSession() as session:
            # Workflow 1: Normal technical question
            try:
                payload = {"message": "What oil should I use in winter?", "user_contact": "workflow1@test.com"}
                async with session.post(f"{self.base_url}/chat", json=payload) as resp:
                    result = await resp.json()
                    if not result.get("ticket_created", False):
                        self.log("Technical question workflow: no ticket")
                    else:
                        self.log("Technical question workflow: unexpected ticket", "FAIL")
            except Exception as e:
                self.log(f"Technical workflow error: {e}", "FAIL")
            
            # Workflow 2: Direct human request
            try:
                payload = {"message": "I want customer service", "user_contact": "workflow2@test.com"}
                async with session.post(f"{self.base_url}/chat", json=payload) as resp:
                    result = await resp.json()
                    if result.get("ticket_created", False):
                        self.log("Human request workflow: creates ticket")
                    else:
                        self.log("Human request workflow: no ticket created", "FAIL")
            except Exception as e:
                self.log(f"Human request workflow error: {e}", "FAIL")
            
            # Workflow 3: Multi-round conversation
            try:
                session_id = None
                messages = ["help", "I need", "something"]
                
                for i, msg in enumerate(messages):
                    payload = {"message": msg, "user_contact": "workflow3@test.com"}
                    if session_id:
                        payload["session_id"] = session_id
                    
                    async with session.post(f"{self.base_url}/chat", json=payload) as resp:
                        result = await resp.json()
                        session_id = result.get("session_id")
                        
                        if i == 2:  # Third message should show choice buttons
                            if "CHOICE_BUTTONS_START" in result.get("response", ""):
                                self.log("Multi-round workflow: shows choices")
                            else:
                                self.log("Multi-round workflow: no choices shown", "FAIL")
                        
            except Exception as e:
                self.log(f"Multi-round workflow error: {e}", "FAIL")
        
        return self.passed, self.failed

async def main():
    integration_tests = IntegrationTests()
    passed, failed = await integration_tests.test_complete_workflows()
    print(f"\nIntegration Tests: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)