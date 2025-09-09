# FAQ System Tests

Organized test suite for the FAQ system.

## Test Structure

```
tests/
├── run_all.py              # Run all test suites
├── test_api.py             # API endpoint tests
├── test_ai_logic.py        # AI service logic tests
├── test_integration.py     # Complete workflow tests
├── test_main.py            # Main application tests
├── test_universal_faq.py   # Universal FAQ functionality tests
├── test_end_chat.py        # End chat functionality tests
├── test_button_choices.py  # Button choice handling tests
├── simple_button_test.py   # Simple button interaction tests
├── debug_ai_service.py     # AI service debugging utilities
├── demo_example.py         # Demo and example scripts
└── README.md               # This file
```

## Running Tests

### All Tests
```bash
python tests/run_all.py
```

### Individual Test Suites
```bash
# Core functionality tests
python tests/test_api.py           # Test API endpoints
python tests/test_ai_logic.py      # Test AI business logic
python tests/test_integration.py   # Test complete workflows

# Feature-specific tests
python tests/test_end_chat.py      # Test end chat functionality
python tests/test_button_choices.py # Test button interactions
python tests/simple_button_test.py # Test simple button workflow

# Development tools
python tests/debug_ai_service.py   # Debug AI service
python tests/demo_example.py       # Run demo examples
```

## Test Categories

### Core Tests
- **API Tests** (`test_api.py`) - Root endpoint, chat endpoint, tickets endpoint, error handling
- **AI Logic Tests** (`test_ai_logic.py`) - Greeting handling, technical questions, human requests, 3-round guidance system
- **Integration Tests** (`test_integration.py`) - Complete workflows, multi-round conversations, end-to-end experiences
- **Main Tests** (`test_main.py`) - Main application functionality
- **Universal FAQ Tests** (`test_universal_faq.py`) - Universal FAQ system functionality

### Feature Tests
- **End Chat Tests** (`test_end_chat.py`) - Chat ending functionality, session state management
- **Button Choice Tests** (`test_button_choices.py`) - Button interaction handling, choice processing
- **Simple Button Tests** (`simple_button_test.py`) - Basic button workflow testing

### Development Tools
- **Debug AI Service** (`debug_ai_service.py`) - AI service debugging and troubleshooting
- **Demo Examples** (`demo_example.py`) - Example usage and demonstrations

## Requirements

- Server must be running on `http://localhost:8000`
- Ollama service must be running with `deepseek-r1:1.5b` model
- All dependencies installed (`aiohttp` for HTTP tests)

## Expected Results

All tests should pass when the system is working correctly:
- API endpoints respond properly
- AI intent detection works as expected
- User workflows complete successfully
- Button interactions work correctly
- Chat ending functionality works
- No unintended ticket creation occurs