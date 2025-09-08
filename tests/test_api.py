#!/usr/bin/env python3
"""
API endpoint tests
"""

import asyncio
import aiohttp
import json

class APITests:
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
    
    async def test_endpoints(self):
        """Test all API endpoints"""
        print("Testing API endpoints...")
        
        async with aiohttp.ClientSession() as session:
            # Test root endpoint
            try:
                async with session.get(f"{self.base_url}/") as resp:
                    if resp.status == 200:
                        self.log("Root endpoint accessible")
                    else:
                        self.log(f"Root endpoint failed: {resp.status}", "FAIL")
            except Exception as e:
                self.log(f"Root endpoint error: {e}", "FAIL")
            
            # Test chat endpoint
            try:
                payload = {"message": "hello", "user_contact": "test@api.com"}
                async with session.post(f"{self.base_url}/chat", json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if "response" in result and "session_id" in result:
                            self.log("Chat endpoint working")
                        else:
                            self.log("Chat endpoint missing fields", "FAIL")
                    else:
                        self.log(f"Chat endpoint failed: {resp.status}", "FAIL")
            except Exception as e:
                self.log(f"Chat endpoint error: {e}", "FAIL")
            
            # Test tickets endpoint
            try:
                async with session.get(f"{self.base_url}/tickets") as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if isinstance(result, list):
                            self.log("Tickets endpoint working")
                        else:
                            self.log("Tickets endpoint wrong format", "FAIL")
                    else:
                        self.log(f"Tickets endpoint failed: {resp.status}", "FAIL")
            except Exception as e:
                self.log(f"Tickets endpoint error: {e}", "FAIL")
        
        return self.passed, self.failed

async def main():
    api_tests = APITests()
    passed, failed = await api_tests.test_endpoints()
    print(f"\nAPI Tests: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)