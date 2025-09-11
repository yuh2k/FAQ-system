import re
import random
import aiohttp
import json
from typing import Tuple, Dict, Any
from config_loader import config

class LocalAIService:
    """Generic local AI service for FAQ systems"""
    
    def __init__(self):
        # Load configuration
        self.ai_settings = config.get_ai_settings()
        self.prompts = config.get_ai_prompts()
        self.response_templates = config.get_response_templates()
        self.ticket_logic = config.get_ticket_logic()
        
        self.ollama_url = "http://localhost:11434"
        self.model_name = "deepseek-r1:1.5b"
        
        self.greeting_responses = [
            "Hello! I'm here to help answer your questions. What can I assist you with today?",
            "Welcome! I'm your FAQ assistant. How can I help you?",
            "Hi there! I'm ready to help with your questions. What would you like to know?"
        ]
        
        self.fallback_responses = [
            "I don't have specific information about that in my knowledge base. Could you try rephrasing your question or ask about something else I might be able to help with?",
            "I'm not sure I can help with that particular question. You might want to contact support for more specific assistance.",
            "That's outside my current knowledge. Is there something else I can help you with?",
            "I don't have information about that topic. Please try asking a different question or contact customer service for further help."
        ]
        
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

    async def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API to generate response"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                }
                
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        raw_response = result.get("response", "").strip()
                        # Filter out <think> sections from R1 model
                        return self._clean_r1_response(raw_response)
                    else:
                        print(f"Ollama API error: {response.status}")
                        return None
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None

    def _clean_r1_response(self, response: str) -> str:
        """Remove <think> sections from DeepSeek-R1 model responses"""
        if not response:
            return response
            
        # Remove <think>...</think> blocks
        import re
        cleaned = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        
        # Clean up extra whitespace
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  # Multiple newlines to double
        cleaned = cleaned.strip()
        
        return cleaned

    async def generate_response(self, user_message: str, kb_answer: str = None, kb_found: bool = False, 
                              session_state: dict = None) -> Tuple[str, bool, bool]:
        """
        Generate AI response using LLM with knowledge base integration
        Returns: (response_content, needs_ticket, is_unclear_intent)
        """
        
        # Initialize session state if not provided
        if session_state is None:
            session_state = {
                'unclear_message_count': 0,
                'guidance_stage': 'normal'
            }
        
        # PRIORITY CHECK: AI-powered human help intent detection
        human_help_needed = await self._detect_human_help_intent(user_message)
        
        
        if human_help_needed:
            direct_help_response = self._get_direct_help_response()
            return direct_help_response, True, False  # Force immediate ticket creation
        
        # Check if this is an unclear intent message
        is_unclear_intent = self._is_unclear_intent(user_message, kb_found)
        
        
        # Handle user choice after 3 unclear messages
        if session_state['guidance_stage'] == 'waiting_for_choice':
            if self._user_wants_ticket(user_message):
                response = "I'll create a support ticket for you right now. A customer service representative will review our conversation and contact you to provide personalized assistance."
                # Reset session state after ticket creation
                session_state['guidance_stage'] = 'normal'
                session_state['unclear_message_count'] = 0
                return response, True, False  # Create ticket
            elif self._user_wants_to_end_chat(user_message):
                response = "I understand. Thank you for using our service! Feel free to start a new conversation anytime with a more specific question."
                # Set special status to indicate chat ended
                session_state['guidance_stage'] = 'ended'
                session_state['unclear_message_count'] = 0
                return response, False, False  # End chat, no ticket
            else:
                # User didn't give clear choice, ask again
                response = "Please let me know clearly: would you like me to **create a support ticket** or **end this conversation**?"
                return response, False, True
        
        # Handle 3-message guidance system
        if is_unclear_intent and session_state['guidance_stage'] != 'escalated':
            unclear_count = session_state['unclear_message_count'] + 1
            session_state['unclear_message_count'] = unclear_count  # Update the session state
            
            if unclear_count >= 3:
                # After 3 unclear messages, give user choice
                response = self._get_choice_message()
                session_state['guidance_stage'] = 'waiting_for_choice'  # Set state to wait for choice
                return response, False, True  # Don't force ticket, let user choose
            else:
                # Provide guidance
                response = self._get_guidance_message(user_message, unclear_count)
                session_state['guidance_stage'] = 'guiding'  # Set guidance stage
                return response, False, True
        
        if kb_found and kb_answer:
            # Knowledge base found an answer, use LLM to enhance it
            prompt = f"""You are a helpful customer service assistant. A customer asked: "{user_message}"

I found this information in our knowledge base: {kb_answer}

Please provide a helpful, professional response that incorporates this knowledge base information. Keep your response concise and friendly. Do not mention that you're using a knowledge base."""
            
            llm_response = await self._call_ollama(prompt)
            if llm_response:
                # Clean the response to remove technical markers
                cleaned_response = self._clean_technical_markers(llm_response)
                needs_ticket = self._check_needs_ticket_robust(llm_response, user_message)
                return cleaned_response, needs_ticket, False
            else:
                # Fallback to enhanced KB answer if LLM fails
                enhanced_response = self._enhance_kb_answer(user_message, kb_answer)
                return enhanced_response, False, False
        else:
            # No knowledge base match, use LLM for general response
            prompt = f"""You are a helpful customer service assistant. A customer asked: "{user_message}"

I don't have specific information about this in my knowledge base. Please provide a helpful, professional response that:
1. Acknowledges their question politely
2. Explains that you don't have specific information about this topic
3. Suggests they contact customer support for detailed help if it seems like a technical issue or complaint
4. Keep the response concise and friendly

CRITICAL: NEVER add "NEEDS_HUMAN_FOLLOWUP" unless the customer EXPLICITLY asks for:
- "speak to human", "talk to human", "human representative"
- "customer service", "customer support"
- "manager", "supervisor"
- "file complaint", "complaint about YOUR service"

DO NOT add "NEEDS_HUMAN_FOLLOWUP" for:
- Any technical questions ("how do I...", "what is...", "help with...")
- Product recommendations ("which car...", "best oil...")  
- General informational requests
- Simple greetings ("hello", "hi")
- Problems that don't explicitly mention YOUR company's fault

If the message seems like a simple greeting (hello, hi, etc.), respond with a friendly greeting and ask how you can help (no ticket needed)."""
            
            llm_response = await self._call_ollama(prompt)
            if llm_response:
                # Clean the response to remove technical markers
                cleaned_response = self._clean_technical_markers(llm_response)
                needs_ticket = self._check_needs_ticket_robust(llm_response, user_message)
                return cleaned_response, needs_ticket, False
            else:
                # Fallback to template responses if LLM fails
                fallback_response = self._generate_smart_fallback(user_message)
                needs_ticket = self._check_needs_ticket_robust(fallback_response, user_message)
                return fallback_response, needs_ticket, False

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

    def _check_needs_ticket_robust(self, ai_response: str, user_message: str = "") -> bool:
        """Robust check for ticket creation - catches all NEEDS_HUMAN_FOLLOWUP cases"""
        
        # First priority: If AI explicitly says needs human followup, ALWAYS create ticket
        if "NEEDS_HUMAN_FOLLOWUP" in ai_response.upper():
            return True
            
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
    
    def _check_needs_ticket(self, ai_response: str, user_message: str = "") -> bool:
        """Legacy method for backward compatibility"""
        return self._check_needs_ticket_robust(ai_response, user_message)

    def _is_unclear_intent(self, user_message: str, kb_found: bool) -> bool:
        """Check if user message has unclear intent"""
        
        
        # If KB found an answer, intent is clear
        if kb_found:
            return False
            
        user_lower = user_message.lower().strip()
        
        # Check for greeting patterns - these are not unclear
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings']
        # Use word boundary check to avoid false matches like "hi" in "something"
        import re
        greeting_pattern = r'\b(' + '|'.join(re.escape(greeting) for greeting in greetings) + r')\b'
        if re.search(greeting_pattern, user_lower):
            return False
        
        # Check for clear complaint/problem patterns - these need tickets but are not unclear
        problem_patterns = ['complaint', 'problem', 'issue', 'broken', 'not working', 'defective']
        if any(pattern in user_lower for pattern in problem_patterns):
            return False
        
        # Patterns that indicate unclear intent
        unclear_patterns = [
            # Very short/vague messages
            len(user_message.strip()) < 10,
            # Single word questions
            len(user_message.split()) <= 2,
            # Vague questions
            any(pattern in user_lower for pattern in [
                'what', 'how', 'why', 'when', 'where', 'help', 'info', 'question',
                'tell me', 'i need', 'can you', 'do you'
            ]) and len(user_message.split()) <= 5,
            # Very general questions without context
            user_lower in ['what?', 'how?', 'why?', 'help', 'info', 'question', 'anything', 'something']
        ]
        
        
        return any(unclear_patterns)

    def _get_guidance_message(self, user_message: str, unclear_count: int) -> str:
        """Get guidance message based on unclear message count"""
        
        messages = {
            1: """I'd like to help you! Could you please be more specific about what you're looking for? 

For example, you can ask me about:
• Car buying advice (new vs used, financing options)
• Car selling tips and best practices  
• Insurance guidance and coverage options
• Maintenance and repair questions
• Electric vehicle information

What specific topic would you like to know about?""",

            2: """I'm still not quite sure what specific information you need. Let me help guide you with some common questions I can answer:

**Car Buying:** "Should I buy a new or used car?" or "What financing options are available?"
**Car Selling:** "When is the best time to sell my car?" or "How do I prepare my car for sale?"
**Insurance:** "What insurance coverage do I need?" or "How to choose the right insurance?"

Could you try asking a more specific question about one of these topics?""",

            3: """I want to make sure you get the help you need. Since I'm having trouble understanding exactly what you're looking for, let me connect you with a human customer service representative who can better assist you.

They'll be able to have a more detailed conversation and provide personalized guidance for your specific situation."""
        }
        
        return messages.get(unclear_count, messages[3])

    def _get_choice_message(self) -> str:
        """Get message offering user choice after 3 unclear messages"""
        return """I'm having difficulty understanding your specific needs. I'd like to help you better. 

You have two options:

**CHOICE_BUTTONS_START**
CREATE_TICKET|Create Support Ticket|A human customer service representative will review our conversation and contact you personally
END_CHAT|End Conversation|Close this chat and try again later with a more specific question
**CHOICE_BUTTONS_END**"""

    def _get_escalation_message(self) -> str:
        """Get message when escalating to human support after 3 unclear messages"""  
        return """I understand you're looking for help, but I'm having difficulty understanding your specific needs. To ensure you get the best assistance possible, I'm creating a support ticket for you.

A customer service representative will review your conversation and reach out to provide personalized help. They'll be able to ask follow-up questions and guide you to the right solution.

Thank you for your patience, and we'll have someone assist you shortly."""

    async def _detect_human_help_intent(self, user_message: str) -> bool:
        """
        Use AI to detect if user wants human help/customer service
        """
        
        # First check with fallback keywords (fast path)
        if self._has_human_help_keywords(user_message):
            return True
        
        # Use simplified AI for semantic intent detection
        intent_prompt = f"""Does this message EXPLICITLY ask for human customer service staff?
Message: "{user_message}"

Only respond YES if message EXPLICITLY contains:
- "speak to human", "talk to human", "human representative"
- "customer service", "customer support" 
- "manager", "supervisor"
- "transfer me", "escalate"

Respond NO for:
- Technical questions ("how do I...", "what is...", "help with...")
- Product questions ("which car...", "best oil...")
- General informational requests
- Simple greetings ("hello", "hi")

Answer: YES or NO only"""

        try:
            ai_intent = await self._call_ollama(intent_prompt)
            if ai_intent and "YES" in ai_intent.strip().upper():
                return True
        except Exception:
            # If AI fails, fall back to keyword detection
            pass
        
        return False

    def _has_human_help_keywords(self, user_message: str) -> bool:
        """Fallback keyword detection for human help requests - only exact phrases"""
        user_lower = user_message.lower().strip()
        
        # Only very explicit phrases that absolutely mean human contact
        explicit_human_phrases = [
            'human help', 'customer service', 'customer support', 
            'talk to human', 'speak to human', 'speak with human',
            'want to speak to a human', 'i want to speak to a human',
            'real person', 'live person', 'actual person',
            'speak to agent', 'talk to agent', 'customer agent', 'support agent',
            'transfer me', 'escalate this', 'escalate my', 'speak to manager', 
            'talk to manager', 'supervisor', 'escalate to manager',
            'bot is not helpful', 'ai cannot help', 'ai is not helping',
            'bot cannot help', 'need real help', 'this bot is useless'
        ]
        
        return any(phrase in user_lower for phrase in explicit_human_phrases)

    def _clean_technical_markers(self, response: str) -> str:
        """Remove technical markers that users shouldn't see"""
        if not response:
            return response
        
        # Remove NEEDS_HUMAN_FOLLOWUP and similar markers
        cleaned = response
        
        # Remove technical markers (case insensitive)
        technical_markers = [
            'NEEDS_HUMAN_FOLLOWUP',
            'NEEDS_HUMAN FOLLOWUP', 
            'TICKET_REQUIRED',
            'ESCALATE_NOW'
        ]
        
        for marker in technical_markers:
            # Remove the marker and any surrounding whitespace/punctuation
            import re
            # Match the marker with optional surrounding whitespace and punctuation
            pattern = rf'\s*\.?\s*{re.escape(marker)}\s*\.?\s*'
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up extra whitespace and newlines
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)  # Multiple newlines
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces
        cleaned = cleaned.strip()
        
        return cleaned

    def _requests_human_help_directly(self, user_message: str) -> bool:
        """
        Detect if user explicitly requests human help using semantic patterns
        Uses both exact phrases and semantic understanding
        """
        user_lower = user_message.lower().strip()
        
        # Direct human help keywords and phrases
        direct_help_patterns = [
            # Explicit human requests
            'human help', 'need human', 'want human', 'talk to human', 'speak to human',
            'human assistance', 'human support', 'real person', 'actual person',
            'live person', 'speak to someone', 'talk to someone', 'connect me to someone',
            
            # Agent/representative requests  
            'customer service', 'customer support', 'support agent', 'customer agent',
            'service representative', 'customer representative', 'support rep',
            'speak to agent', 'talk to agent', 'connect to agent',
            
            # Transfer/escalation requests
            'transfer me', 'escalate', 'escalate this', 'escalate my issue',
            'need to escalate', 'can you escalate', 'please escalate',
            
            # Urgent help requests
            'need assistance right now', 'need help immediately', 'urgent assistance',
            'immediate help', 'emergency help', 'help me now', 'need help asap',
            'this is urgent', 'urgent matter', 'critical issue',
            
            # Dissatisfaction with AI
            'this bot is not helpful', 'ai is not helping', 'bot cannot help',
            'need real help', 'this is not working', 'bot is useless',
            'ai cannot understand', 'you are not understanding',
            
            # Manager/supervisor requests
            'speak to manager', 'talk to manager', 'manager please',
            'supervisor', 'speak to supervisor', 'escalate to manager',
        ]
        
        # Check for direct pattern matches
        for pattern in direct_help_patterns:
            if pattern in user_lower:
                return True
        
        # Semantic analysis for human help requests
        # Check for combinations of help-seeking words
        help_words = ['help', 'assist', 'support', 'service']
        human_words = ['human', 'person', 'agent', 'representative', 'someone', 'manager', 'supervisor']
        urgency_words = ['now', 'immediately', 'urgent', 'asap', 'emergency', 'critical']
        
        # Pattern: help + human words
        if any(hw in user_lower for hw in help_words) and any(hm in user_lower for hm in human_words):
            return True
            
        # Pattern: urgency + help/assistance
        if any(uw in user_lower for uw in urgency_words) and any(hw in user_lower for hw in help_words):
            return True
        
        # Pattern: "I need to" + human/support words
        if 'i need to' in user_lower and any(hw in user_lower for hw in human_words + ['support', 'service']):
            return True
            
        # Pattern: "Can I" + human interaction
        if any(phrase in user_lower for phrase in ['can i talk', 'can i speak', 'can i get', 'may i speak']):
            if any(hw in user_lower for hw in human_words):
                return True
        
        return False

    def _get_direct_help_response(self) -> str:
        """Get response for direct human help requests"""
        return """I understand you'd like to speak with a human representative. I'm creating a priority support ticket for you right now.

A customer service agent will reach out to you shortly to provide the personal assistance you need. They'll have full context of our conversation and will be able to help resolve your specific situation.

Thank you for reaching out, and we'll have someone contact you soon."""

    def _user_wants_ticket(self, user_message: str) -> bool:
        """Check if user wants to create a support ticket"""
        user_lower = user_message.lower().strip()
        
        # Check for button action first
        if user_lower == 'create_ticket':
            return True
            
        ticket_phrases = [
            'create ticket', 'support ticket', 'ticket', 'yes ticket',
            'create support', 'yes create', 'option 1', '1',
            'human help', 'customer service', 'contact support'
        ]
        return any(phrase in user_lower for phrase in ticket_phrases)
    
    def _user_wants_to_end_chat(self, user_message: str) -> bool:
        """Check if user wants to end the conversation"""
        user_lower = user_message.lower().strip()
        
        # Check for button action first
        if user_lower == 'end_chat':
            return True
            
        end_phrases = [
            'end conversation', 'close chat', 'end chat', 'no thanks',
            'no ticket', 'option 2', '2', 'end this', 'close this',
            'goodbye', 'bye', 'quit', 'exit', 'cancel'
        ]
        return any(phrase in user_lower for phrase in end_phrases)

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