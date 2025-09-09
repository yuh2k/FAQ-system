#!/bin/bash

# Customer FAQ System - One-Click Setup
# ==============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                Customer FAQ System Setup                     ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
}

print_step() {
    echo -e "\n${YELLOW}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists python3; then
        missing_deps+=("Python 3.8+")
    fi
    
    if ! command_exists node; then
        missing_deps+=("Node.js 16+")
    fi
    
    if ! command_exists npm; then
        missing_deps+=("npm")
    fi
    
    if ! command_exists ollama; then
        missing_deps+=("Ollama")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing prerequisites:"
        for dep in "${missing_deps[@]}"; do
            echo -e "  ${RED}- $dep${NC}"
        done
        echo -e "\n${YELLOW}Please install the missing dependencies and run this script again.${NC}"
        echo -e "${BLUE}Installation guides:${NC}"
        echo -e "  - Python: https://www.python.org/downloads/"
        echo -e "  - Node.js: https://nodejs.org/"
        echo -e "  - Ollama: https://ollama.ai/"
        exit 1
    fi
    
    print_success "All prerequisites found"
}

# Setup Ollama and AI model
setup_ollama() {
    print_step "Setting up Ollama and AI model..."
    
    # Check if Ollama is running
    if ! pgrep -f "ollama serve" > /dev/null; then
        print_info "Starting Ollama service..."
        ollama serve &
        sleep 3
    else
        print_success "Ollama service already running"
    fi
    
    # Check if model exists
    if ! ollama list | grep -q "deepseek-r1:1.5b"; then
        print_info "Downloading DeepSeek model (this may take a few minutes)..."
        ollama pull deepseek-r1:1.5b
    else
        print_success "DeepSeek model already installed"
    fi
    
    print_success "Ollama setup complete"
}

# Setup Python backend
setup_backend() {
    print_step "Setting up Python backend..."
    
    cd server
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip install -q -r requirements.txt
    
    print_success "Backend setup complete"
    
    cd ..
}

# Setup Node.js frontend
setup_frontend() {
    print_step "Setting up Node.js frontend..."
    
    cd frontend
    
    # Install dependencies
    print_info "Installing Node.js dependencies..."
    npm install --silent
    
    print_success "Frontend setup complete"
    
    cd ..
}

# Create start script
create_start_script() {
    print_step "Creating start script..."
    
    cat > start.sh << 'EOF'
#!/bin/bash

# Customer FAQ System - Start Script
# ==================================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                Starting FAQ System                           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"

# Check if Ollama is running
if ! pgrep -f "ollama serve" > /dev/null; then
    print_info "Starting Ollama service..."
    ollama serve &
    sleep 3
fi

# Start backend
print_info "Starting backend server..."
cd server
source venv/bin/activate
python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
print_info "Waiting for backend to initialize..."
sleep 5

# Start frontend
print_info "Starting frontend development server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
print_success "FAQ System is starting up!"
echo -e "${GREEN}Frontend: ${NC}http://localhost:3000"
echo -e "${GREEN}Backend:  ${NC}http://localhost:8000"
echo -e "${GREEN}API Docs: ${NC}http://localhost:8000/docs"
echo ""
print_warning "Press Ctrl+C to stop all services"

# Wait for interrupt
trap 'echo -e "\n${YELLOW}Stopping services...${NC}"; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait
EOF

    chmod +x start.sh
    print_success "Start script created"
}

# Create stop script
create_stop_script() {
    print_step "Creating stop script..."
    
    cat > stop.sh << 'EOF'
#!/bin/bash

# Customer FAQ System - Stop Script
# =================================

echo "🛑 Stopping FAQ System services..."

# Kill Node.js processes (frontend)
pkill -f "node.*start" 2>/dev/null

# Kill Python processes (backend)
pkill -f "python.*run.py" 2>/dev/null

# Kill any remaining processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null

echo "✅ All services stopped"
EOF

    chmod +x stop.sh
    print_success "Stop script created"
}

# Run tests
run_tests() {
    print_step "Running system tests..."
    
    # Start backend for testing
    cd server
    source venv/bin/activate
    python run.py &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    sleep 5
    
    # Run tests
    if python tests/test_api.py; then
        print_success "Basic system tests passed"
    else
        print_error "System tests failed"
    fi
    
    # Clean up
    kill $BACKEND_PID 2>/dev/null
}

# Main setup process
main() {
    print_header
    
    check_prerequisites
    setup_ollama
    setup_backend
    setup_frontend
    create_start_script
    create_stop_script
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    Setup Complete! 🎉                       ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    echo -e "  ${GREEN}./start.sh${NC}  - Start the entire system"
    echo -e "  ${GREEN}./stop.sh${NC}   - Stop all services"
    echo ""
    echo -e "${BLUE}Access URLs:${NC}"
    echo -e "  Frontend: ${GREEN}http://localhost:3000${NC}"
    echo -e "  Backend:  ${GREEN}http://localhost:8000${NC}"
    echo -e "  API Docs: ${GREEN}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Run ${GREEN}./start.sh${NC} to start the system"
    echo -e "  2. Open ${GREEN}http://localhost:3000${NC} in your browser"
    echo -e "  3. Enter your email and start chatting!"
    echo ""
}

# Run main function
main "$@"