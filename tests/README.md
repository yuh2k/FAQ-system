# FAQ System Tests

Organized test suite for the FAQ system.

## Test Structure

```
tests/
├── run_all.py           # Run all test suites
├── test_api.py          # API endpoint tests
├── test_ai_logic.py     # AI service logic tests
├── test_integration.py  # Complete workflow tests
└── README.md            # This file
```

## Running Tests

### All Tests
```bash
python run_all.py
```

### Individual Test Suites
```bash
python test_api.py           # Test API endpoints
python test_ai_logic.py      # Test AI business logic
python test_integration.py   # Test complete workflows
```

## Test Categories

### API Tests (`test_api.py`)
- Root endpoint accessibility
- Chat endpoint functionality
- Tickets endpoint functionality
- Error handling and validation

### AI Logic Tests (`test_ai_logic.py`) 
- Greeting handling (no ticket creation)
- Technical question handling (no ticket creation)
- Human request detection (immediate ticket creation)
- 3-round guidance system
- Choice button generation and handling

### Integration Tests (`test_integration.py`)
- Complete technical question workflow
- Complete human request workflow  
- Multi-round conversation workflow
- End-to-end user experiences

## Requirements

- Server must be running on `http://localhost:8000`
- Ollama service must be running with `deepseek-r1:1.5b` model
- All dependencies installed (`aiohttp` for HTTP tests)

## Expected Results

All tests should pass when the system is working correctly:
- API endpoints respond properly
- AI intent detection works as expected
- User workflows complete successfully
- No unintended ticket creation occurs