#!/bin/bash

# FAQ System Startup Script
# This script starts both backend and frontend services

echo "🚀 Starting FAQ System..."
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

if command_exists ollama; then
    echo -e "${GREEN}✅ Ollama is installed${NC}"
else
    echo -e "${YELLOW}⚠️  Ollama is not installed (AI will use fallback responses)${NC}"
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"

# Check if ports are available
if port_in_use 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use (Backend)${NC}"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if port_in_use 3000; then
    echo -e "${YELLOW}⚠️  Port 3000 is already in use (Frontend)${NC}"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install backend dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
cd server
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}Installing Python packages...${NC}"
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from example...${NC}"
    cp .env.example .env
fi

echo -e "${GREEN}✅ Backend setup complete${NC}"

# Install frontend dependencies
echo -e "${BLUE}Installing frontend dependencies...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing npm packages...${NC}"
    npm install
else
    echo -e "${GREEN}✅ Frontend dependencies already installed${NC}"
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from example...${NC}"
    cp .env.example .env
fi

echo -e "${GREEN}✅ Frontend setup complete${NC}"

# Check and start Ollama service for AI
echo -e "${BLUE}Checking AI service (Ollama)...${NC}"
if command_exists ollama; then
    # Check if Ollama is already running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama is already running${NC}"
    else
        echo -e "${YELLOW}🤖 Starting Ollama service for AI...${NC}"
        ollama serve > /dev/null 2>&1 &
        OLLAMA_PID=$!
        
        # Wait for Ollama to start
        echo -e "${YELLOW}⏳ Waiting for Ollama to start...${NC}"
        for i in {1..30}; do
            if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
                echo -e "${GREEN}✅ Ollama service started successfully${NC}"
                break
            fi
            sleep 1
        done
        
        # Check if Ollama started successfully
        if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo -e "${RED}❌ Failed to start Ollama service${NC}"
            echo -e "${YELLOW}⚠️  The system will use fallback AI responses${NC}"
        fi
    fi
    
    # Check if required model is available
    if curl -s http://localhost:11434/api/tags 2>/dev/null | grep -q "deepseek-r1:1.5b"; then
        echo -e "${GREEN}✅ AI model (deepseek-r1:1.5b) is available${NC}"
    else
        echo -e "${YELLOW}⚠️  AI model (deepseek-r1:1.5b) not found${NC}"
        echo -e "${YELLOW}💡 To install it, run: ollama pull deepseek-r1:1.5b${NC}"
        echo -e "${YELLOW}⚠️  The system will use fallback AI responses${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama is not installed. AI will use fallback responses${NC}"
    echo -e "${YELLOW}💡 To install Ollama, visit: https://ollama.ai${NC}"
fi

# Start services
echo -e "${BLUE}Starting services...${NC}"
echo "=========================="

# Start backend in background
echo -e "${YELLOW}🔧 Starting backend server on http://localhost:8000${NC}"
cd ../server
source venv/bin/activate
python run.py &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${YELLOW}⏳ Waiting for backend to start...${NC}"
sleep 5

# Check if backend started successfully
if ! port_in_use 8000; then
    echo -e "${RED}❌ Backend failed to start${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo -e "${GREEN}✅ Backend server running (PID: $BACKEND_PID)${NC}"

# Start frontend
echo -e "${YELLOW}🎨 Starting frontend server on http://localhost:3000${NC}"
cd ../frontend
npm start &
FRONTEND_PID=$!

# Wait for frontend to start
echo -e "${YELLOW}⏳ Waiting for frontend to start...${NC}"
sleep 10

echo ""
echo "🎉 FAQ System is now running!"
echo "=============================="
echo -e "🔧 Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "🎨 Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "📚 API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo "💡 Tips:"
echo "   • The frontend will automatically open in your browser"
echo "   • Use Ctrl+C to stop both services"
echo "   • Check the README.md files for more information"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    # Only kill Ollama if we started it
    if [ ! -z "$OLLAMA_PID" ]; then
        echo -e "${YELLOW}🤖 Stopping Ollama service...${NC}"
        kill $OLLAMA_PID 2>/dev/null
    fi
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for user to stop
wait
