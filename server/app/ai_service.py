import re
import random
from typing import Tuple
from config_loader import config

class LocalAIService:
    """Generic local AI service for FAQ systems"""
    
    def __init__(self):
        # Load configuration
        self.ai_settings = config.get_ai_settings()
        self.prompts = config.get_ai_prompts()
        self.response_templates = config.get_response_templates()
        self.ticket_logic = config.get_ticket_logic()
        
        # Generic response templates
        self.greeting_responses = [
            "Hello! I'm here to help answer your questions. What can I assist you with today?",
            "Welcome! I'm your FAQ assistant. How can I help you?",
            "Hi there! I'm ready to help with your questions. What would you like to know?"
        ]
        
        # Generic fallback responses for when no KB match
        self.fallback_responses = [
            "I don't have specific information about that in my knowledge base. Could you try rephrasing your question or ask about something else I might be able to help with?",
            "I'm not sure I can help with that particular question. You might want to contact support for more specific assistance.",
            "That's outside my current knowledge. Is there something else I can help you with?",
            "I don't have information about that topic. Please try asking a different question or contact customer service for further help."
        ]
        
        # Smart contextual responses based on question patterns
        self.contextual_patterns = {
            'how_to': {
                'patterns': [r'how to', r'how do i', r'how can i', r'steps to'],
                'responses': [
                    "I understand you're looking for step-by-step guidance. While I don't have specific instructions for that in my knowledge base, I'd recommend checking our documentation or contacting support for detailed procedures.",
                    "That sounds like a process question. I don't have those specific steps available, but our support team should be able to walk you through it."
                ]
            },
            'what_is': {
                'patterns': [r'what is', r'what are', r'define', r'explain'],
                'responses': [
                    "I don't have a definition for that in my current knowledge base. You might find more detailed information by contacting our support team.",
                    "That's not something I have information about. For detailed explanations, I'd recommend reaching out to customer service."
                ]
            },
            'why': {
                'patterns': [r'why does', r'why is', r'why would', r'reason'],
                'responses': [
                    "That's a good question about the reasoning behind that. I don't have that background information, but our support team could provide more context.",
                    "I understand you're looking for the rationale. While I don't have those details, customer service could explain the reasoning."
                ]
            },
            'pricing': {
                'patterns': [r'cost', r'price', r'fee', r'charge', r'expensive', r'cheap', r'how much'],
                'responses': [
                    "For pricing information, I'd recommend checking our website or contacting our sales team for the most current rates.",
                    "Pricing questions are best handled by our sales team who can provide current rates and any available discounts."
                ]
            },
            'problem': {
                'patterns': [r'problem', r'issue', r'error', r'bug', r'not working', r'broken'],
                'responses': [
                    "I understand you're experiencing an issue. For technical problems, our support team can provide specific troubleshooting assistance. NEEDS_HUMAN_FOLLOWUP",
                    "That sounds like a technical issue that would be best handled by our support specialists. NEEDS_HUMAN_FOLLOWUP"
                ]
            },
            'complaint': {
                'patterns': [r'complaint', r'dissatisfied', r'unhappy', r'terrible', r'awful', r'worst'],
                'responses': [
                    "I understand your frustration, and I want to make sure this gets proper attention. Let me connect you with someone who can help resolve this. NEEDS_HUMAN_FOLLOWUP",
                    "I'm sorry to hear about your experience. This deserves immediate attention from our customer service team. NEEDS_HUMAN_FOLLOWUP"
                ]
            }
        }

    async def generate_response(self, user_message: str, kb_answer: str = None, kb_found: bool = False) -> Tuple[str, bool]:
        """
        Generate AI response using knowledge base or contextual fallbacks
        Returns: (response_content, needs_ticket)
        """
        
        if kb_found and kb_answer:
            # Knowledge base found an answer, enhance it with context
            enhanced_response = self._enhance_kb_answer(user_message, kb_answer)
            return enhanced_response, False
        
        # No knowledge base match, use smart fallback
        fallback_response = self._generate_smart_fallback(user_message)
        needs_ticket = self._check_needs_ticket(fallback_response, user_message)
        
        return fallback_response, needs_ticket

    def _enhance_kb_answer(self, user_message: str, kb_answer: str) -> str:
        """Enhance knowledge base answers with contextual intros"""
        
        user_lower = user_message.lower()
        
        # Add contextual intro based on question type
        if any(word in user_lower for word in ['should i', 'recommend', 'advice', 'suggest']):
            intro = "Based on the information I have, here's my recommendation: "
        elif any(word in user_lower for word in ['how', 'what', 'when', 'where']):
            intro = "Here's what I can tell you: "
        elif any(word in user_lower for word in ['help', 'assist']):
            intro = "I'd be happy to help. "
        elif any(word in user_lower for word in ['explain', 'understand', 'clarify']):
            intro = "Let me explain: "
        else:
            intro = ""
        
        return f"{intro}{kb_answer}"

    def _generate_smart_fallback(self, user_message: str) -> str:
        """Generate contextually appropriate fallback responses"""
        
        user_lower = user_message.lower()
        
        # Check for greetings first
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings']):
            return random.choice(self.greeting_responses)
        
        # Check for contextual patterns
        for category, data in self.contextual_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_lower):
                    return random.choice(data['responses'])
        
        # No specific pattern matched, use generic fallback
        return random.choice(self.fallback_responses)

    def _check_needs_ticket(self, ai_response: str, user_message: str = "") -> bool:
        """Check if response or message indicates need for ticket"""
        
        # Check AI response for ticket keywords
        response_keywords = self.ticket_logic.get('response_keywords', [])
        for keyword in response_keywords:
            if keyword in ai_response:
                return True
        
        # Check user message for urgent keywords  
        urgent_keywords = self.ticket_logic.get('urgent_user_keywords', [])
        user_lower = user_message.lower()
        
        for keyword in urgent_keywords:
            if keyword.lower() in user_lower:
                return True
                
        return False

    def should_create_ticket(self, user_message: str, ai_response: str, kb_found: bool) -> bool:
        """
        Determine if ticket should be created
        """
        return self._check_needs_ticket(ai_response, user_message)
    
    def get_ticket_created_message(self, ticket_id: int) -> str:
        """Get formatted ticket creation message"""
        template = self.response_templates.get('ticket_created', 
            'I have created a support ticket #{ticket_id} for you. Our team will review your request and get back to you soon.')
        return template.format(ticket_id=ticket_id)
    
    def get_welcome_message(self) -> str:
        """Get a random welcome message"""
        return random.choice(self.greeting_responses)
    
    def get_provider_status(self):
        """Get current provider status"""
        return {
            "current_provider": "local_ai",
            "type": "generic_faq_system",
            "features": [
                "knowledge_base_enhancement",
                "contextual_fallbacks",
                "smart_ticket_creation",
                "greeting_detection",
                "pattern_matching"
            ],
            "contextual_patterns": list(self.contextual_patterns.keys())
        }
    
    def reload_config(self):
        """Reload configuration"""
        config.reload_configs()
        self.ai_settings = config.get_ai_settings()
        self.response_templates = config.get_response_templates()
        self.ticket_logic = config.get_ticket_logic()

# Create alias for backward compatibility
AIService = LocalAIService