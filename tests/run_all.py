#!/usr/bin/env python3
"""
Run all tests
"""

import asyncio
import sys
import os

# Import test modules
from test_api import APITests
from test_integration import IntegrationTests

# Add path for AI tests
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server', 'app'))
from test_ai_logic import AILogicTests

async def run_all_tests():
    """Run all test suites"""
    print("🚀 Running FAQ System Test Suite")
    print("=" * 50)
    
    total_passed = 0
    total_failed = 0
    
    # API Tests
    print("\n1. API Tests")
    print("-" * 30)
    try:
        api_tests = APITests()
        passed, failed = await api_tests.test_endpoints()
        total_passed += passed
        total_failed += failed
        print(f"API Tests: {passed} passed, {failed} failed")
    except Exception as e:
        print(f"❌ API tests failed: {e}")
        total_failed += 1
    
    # AI Logic Tests
    print("\n2. AI Logic Tests")
    print("-" * 30)
    try:
        ai_tests = AILogicTests()
        passed, failed = await ai_tests.test_ai_logic()
        total_passed += passed
        total_failed += failed
        print(f"AI Logic Tests: {passed} passed, {failed} failed")
    except Exception as e:
        print(f"❌ AI logic tests failed: {e}")
        total_failed += 1
    
    # Integration Tests
    print("\n3. Integration Tests")
    print("-" * 30)
    try:
        integration_tests = IntegrationTests()
        passed, failed = await integration_tests.test_complete_workflows()
        total_passed += passed
        total_failed += failed
        print(f"Integration Tests: {passed} passed, {failed} failed")
    except Exception as e:
        print(f"❌ Integration tests failed: {e}")
        total_failed += 1
    
    # Final Results
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")
    
    success_rate = total_passed / (total_passed + total_failed) * 100 if (total_passed + total_failed) > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if total_failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"\n⚠️ {total_failed} tests failed")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)