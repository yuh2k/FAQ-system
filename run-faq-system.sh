#!/bin/bash

echo "🚀 FAQ System Quick Fix & Start"
echo "==============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Stop any existing processes
echo -e "${YELLOW}Stopping existing processes...${NC}"
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start backend
echo -e "${YELLOW}Starting backend server...${NC}"
cd server
source venv/bin/activate
python run.py &
BACKEND_PID=$!

echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"

# Wait for backend
sleep 3

# Start frontend without the problematic dev server
echo -e "${YELLOW}Starting frontend (simple server)...${NC}"
cd ../frontend

# Create simple server script
cat > serve.js << 'EOF'
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const app = express();

// Proxy API requests to backend
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true,
  pathRewrite: {
    '^/api': ''
  }
}));

// Serve static files
app.use(express.static(path.join(__dirname, 'build')));

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build/index.html'));
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Frontend server running on http://localhost:${PORT}`);
});
EOF

# Install express and proxy middleware
npm install express http-proxy-middleware --save-dev

# Build the React app
npm run build

# Start the server
node serve.js &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo "🎉 FAQ System is running!"
echo "========================"
echo -e "🔧 Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "🎨 Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "📚 API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo "Press Ctrl+C to stop all services"

cleanup() {
    echo -e "\n${YELLOW}Stopping all services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

trap cleanup SIGINT
wait