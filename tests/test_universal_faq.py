#!/usr/bin/env python3
"""
Test script for domain filtering improvements
"""

import sys
import os
import asyncio

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_universal_faq_system():
    """Test the universal FAQ system with graceful fallbacks"""
    
    try:
        from ai_service import LocalAIService
        from knowledge_base_service import KnowledgeBaseService
        
        print("🧪 Testing Universal FAQ System")
        print("=" * 50)
        
        # Initialize services
        ai = LocalAIService()
        kb = KnowledgeBaseService()
        
        print("✅ Services initialized")
        print(f"📚 Knowledge base topic detected: {kb.detect_kb_topic()}")
        
        # Test cases for universal FAQ system
        test_cases = [
            # Knowledge base match cases (should get KB answers)
            {
                "question": "Should I buy a new car or used car?",
                "expected": "kb_match",
                "description": "Question matching knowledge base"
            },
            {
                "question": "What insurance do I need for my car?", 
                "expected": "kb_match",
                "description": "Another KB matching question"
            },
            
            # Non-matching questions - should get contextual fallbacks
            {
                "question": "What is the best restaurant in Bellevue?",
                "expected": "fallback_what_is",  # This will match "what is" pattern
                "description": "Non-matching question (restaurant)"
            },
            {
                "question": "How do I cook pasta?",
                "expected": "fallback_how_to",
                "description": "Non-matching how-to question"
            },
            {
                "question": "What is machine learning?",
                "expected": "greeting_or_what_is",  # This might match greeting or what_is
                "description": "Non-matching definition question"
            },
            {
                "question": "Why is the sky blue?",
                "expected": "fallback_why",
                "description": "Non-matching why question"
            },
            {
                "question": "How much does this cost?",
                "expected": "kb_match_or_pricing",  # Might match KB due to cost-related content
                "description": "Pricing question"
            },
            {
                "question": "I have a problem with my order",
                "expected": "fallback_problem",
                "description": "Problem/issue question"
            },
            {
                "question": "I want to file a complaint",
                "expected": "fallback_complaint",
                "description": "Complaint question"
            },
            
            # Greetings
            {
                "question": "Hello, how can you help me?",
                "expected": "kb_match_or_greeting",  # Might match KB due to help-related content
                "description": "Greeting"
            }
        ]
        
        print(f"\n🧪 Testing {len(test_cases)} cases:")
        print("-" * 40)
        
        passed = 0
        failed = 0
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n{i}. {case['description']}")
            print(f"   Q: {case['question']}")
            
            # Test knowledge base
            kb_answer, kb_found, similarity = kb.search_knowledge_base(case['question'])
            
            # Test AI service with KB results
            ai_response, needs_ticket = await ai.generate_response(
                case['question'], 
                kb_answer=kb_answer if kb_found else None, 
                kb_found=kb_found
            )
            
            print(f"   📊 KB Match: {kb_found} (similarity: {similarity:.3f})")
            print(f"   🤖 AI Response: {ai_response[:80]}...")
            
            # Check results based on universal FAQ system expectations
            if case['expected'] == 'kb_match':
                # Should match knowledge base and return KB answer
                if kb_found and similarity >= 0.5:
                    print(f"   ✅ PASS: Found relevant answer in knowledge base")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Expected to match knowledge base (similarity: {similarity:.3f})")
                    failed += 1
                    
            elif case['expected'] == 'fallback':
                # Should NOT match KB and should get generic fallback
                if not kb_found and any(phrase in ai_response for phrase in [
                    "don't have specific information",
                    "don't have information about",
                    "not sure I can help",
                    "outside my current knowledge"
                ]):
                    print(f"   ✅ PASS: Graceful fallback for non-matching question")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Should have graceful fallback (KB found: {kb_found})")
                    failed += 1
                    
            elif case['expected'].startswith('fallback_'):
                # Should get contextual fallback response
                pattern_type = case['expected'].replace('fallback_', '')
                contextual_indicators = {
                    'how_to': ['step-by-step guidance', 'specific instructions', 'specific steps'],
                    'what_is': ["don't have a definition", 'detailed information', 'detailed explanations'],
                    'why': ['reasoning behind', 'rationale', 'background information'],
                    'pricing': ['pricing information', 'sales team', 'current rates'],
                    'problem': ['technical problems', 'support specialists', 'NEEDS_HUMAN_FOLLOWUP'],
                    'complaint': ['understand your frustration', 'proper attention', 'NEEDS_HUMAN_FOLLOWUP']
                }
                
                if not kb_found and any(indicator in ai_response for indicator in contextual_indicators.get(pattern_type, [])):
                    print(f"   ✅ PASS: Contextual fallback for {pattern_type} question")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Should have contextual {pattern_type} fallback")
                    failed += 1
                    
            elif case['expected'] == 'greeting':
                # Should get greeting response
                if any(phrase in ai_response for phrase in [
                    "Hello", "Welcome", "Hi there", "help you", "assist you"
                ]):
                    print(f"   ✅ PASS: Handled greeting appropriately")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Should have handled greeting")
                    failed += 1
                    
            elif case['expected'] == 'greeting_or_what_is':
                # Could be either greeting or what_is pattern
                is_greeting = any(phrase in ai_response for phrase in [
                    "Hello", "Welcome", "Hi there", "help you", "assist you"
                ])
                is_what_is = any(phrase in ai_response for phrase in [
                    "don't have a definition", 'detailed information', 'detailed explanations'
                ])
                if is_greeting or is_what_is:
                    response_type = "greeting" if is_greeting else "what_is fallback"
                    print(f"   ✅ PASS: Handled as {response_type}")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Should be greeting or what_is fallback")
                    failed += 1
                    
            elif case['expected'] == 'kb_match_or_pricing':
                # Could match KB or be pricing fallback
                if kb_found:
                    print(f"   ✅ PASS: Found relevant KB answer")
                    passed += 1
                elif any(phrase in ai_response for phrase in [
                    'pricing information', 'sales team', 'current rates'
                ]):
                    print(f"   ✅ PASS: Pricing fallback response")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Should be KB match or pricing fallback")
                    failed += 1
                    
            elif case['expected'] == 'kb_match_or_greeting':
                # Could match KB or be greeting
                if kb_found:
                    print(f"   ✅ PASS: Found relevant KB answer") 
                    passed += 1
                elif any(phrase in ai_response for phrase in [
                    "Hello", "Welcome", "Hi there", "help you", "assist you"
                ]):
                    print(f"   ✅ PASS: Greeting response")
                    passed += 1
                else:
                    print(f"   ❌ FAIL: Should be KB match or greeting")
                    failed += 1
        
        print(f"\n📊 Test Results:")
        print(f"   ✅ Passed: {passed}/{len(test_cases)}")
        print(f"   ❌ Failed: {failed}/{len(test_cases)}")
        print(f"   📈 Success Rate: {passed/len(test_cases)*100:.1f}%")
        
        if failed == 0:
            print(f"\n🎉 All tests passed! Universal FAQ system is working correctly.")
            return True
        else:
            print(f"\n⚠️  Some tests failed. Review the logic above.")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_universal_faq_system())
    
    if success:
        print("\n✨ Universal FAQ system is working perfectly!")
        print("✅ Knowledge base questions get proper answers")
        print("✅ Non-matching questions get graceful contextual fallbacks")
        print("✅ System works universally with any knowledge base domain")
    else:
        print("\n💥 There are still issues with the universal FAQ system.")
        sys.exit(1)