#!/usr/bin/env python3
"""
Demo script showing the Customer FAQ System capabilities
Run this after starting the server to see example interactions
"""

import requests
import json
import time

SERVER_URL = "http://localhost:8000"

def test_knowledge_base_search():
    """Test knowledge base search functionality"""
    print("🔍 Testing Knowledge Base Search")
    print("=" * 40)
    
    test_questions = [
        "Should I buy a new car or used car?",
        "What insurance coverage do I need?",
        "How do I get the best financing rate?",
        "When is the best time to sell my car?",
        "What are the signs I need car repair?",
        "Are electric cars worth buying?",
    ]
    
    for question in test_questions:
        try:
            response = requests.post(f"{SERVER_URL}/chat", json={
                "message": question,
                "user_contact": "demo@example.com"
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n❓ Q: {question}")
                print(f"🤖 A: {data['response'][:100]}...")
                print(f"📊 From KB: {data['is_from_kb']}")
                print(f"🎫 Ticket Created: {data['ticket_created']}")
                print("-" * 40)
            else:
                print(f"❌ Error for question: {question}")
                
        except Exception as e:
            print(f"❌ Failed to connect to server: {e}")
            print("Make sure the server is running on http://localhost:8000")
            break
            
        time.sleep(1)  # Be nice to the API

def test_ticket_creation():
    """Test ticket creation with complaint"""
    print("\n🎫 Testing Ticket Creation")
    print("=" * 40)
    
    complaint_message = "I want to file a complaint about my recent car purchase. The car has engine problems."
    
    try:
        response = requests.post(f"{SERVER_URL}/chat", json={
            "message": complaint_message,
            "user_contact": "complaint@example.com"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"❓ Complaint: {complaint_message}")
            print(f"🤖 Response: {data['response']}")
            print(f"🎫 Ticket Created: {data['ticket_created']}")
            if data['ticket_created']:
                print(f"🆔 Ticket ID: {data['ticket_id']}")
        
    except Exception as e:
        print(f"❌ Error testing ticket creation: {e}")

def show_knowledge_base_stats():
    """Show knowledge base statistics"""
    print("\n📚 Knowledge Base Statistics")
    print("=" * 40)
    
    try:
        response = requests.get(f"{SERVER_URL}/knowledge-base")
        if response.status_code == 200:
            data = response.json()
            qa_pairs = data['qa_pairs']
            print(f"📊 Total Q&A pairs: {len(qa_pairs)}")
            
            # Count by category
            categories = {}
            for qa in qa_pairs:
                # Simple category detection from question content
                question = qa['question'].lower()
                if 'buy' in question or 'purchase' in question:
                    category = 'Car Buying'
                elif 'sell' in question:
                    category = 'Car Selling'
                elif 'insurance' in question:
                    category = 'Insurance'
                elif 'financing' in question or 'loan' in question:
                    category = 'Financing'
                elif 'maintenance' in question or 'repair' in question:
                    category = 'Maintenance'
                elif 'electric' in question or 'hybrid' in question:
                    category = 'Electric/Hybrid'
                else:
                    category = 'Other'
                    
                categories[category] = categories.get(category, 0) + 1
            
            print("\n📋 Categories:")
            for category, count in sorted(categories.items()):
                print(f"  • {category}: {count} questions")
                
    except Exception as e:
        print(f"❌ Error getting knowledge base stats: {e}")

if __name__ == "__main__":
    print("🚗 Customer FAQ System Demo")
    print("=" * 50)
    print("Make sure to start the server first:")
    print("cd server && python run.py")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{SERVER_URL}/")
        if response.status_code == 200:
            print("✅ Server is running!")
            
            show_knowledge_base_stats()
            test_knowledge_base_search()
            test_ticket_creation()
            
            print("\n🎉 Demo complete!")
            print("Visit http://localhost:8000/docs to explore the API")
        else:
            print("❌ Server not responding correctly")
    except:
        print("❌ Cannot connect to server. Please start it first:")
        print("cd server && python run.py")