# FAQ System Frontend 🚀

A modern React-based frontend for the AI-powered Customer FAQ System, featuring beautiful UI with Ant Design components.

## ✨ Features

### 🤖 **Smart Chat Interface**
- Real-time AI conversation with typing indicators
- Message bubbles with sender avatars
- Knowledge base and ticket creation indicators
- Session management and chat history

### 🎫 **Ticket Management**
- Interactive tickets table with status updates
- Detailed ticket modal with full conversation context
- Real-time status changes (Open → In Progress → Closed)
- Ticket statistics dashboard

### 📚 **Knowledge Base Explorer**
- Browse all Q&A pairs in the system
- Search functionality across questions and answers
- Switch between different knowledge bases
- Real-time knowledge base statistics

### 🎨 **Beautiful UI/UX**
- Clean, modern design with Ant Design
- Responsive layout for desktop and mobile
- Smooth animations and hover effects
- Professional customer service look

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **Ant Design 5** - Beautiful UI components
- **Axios** - HTTP client for API calls
- **React Router** - Client-side routing

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Backend server running on http://localhost:8000

### Installation

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

3. **Open Browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Build for Production
```bash
npm run build
```

## 📱 Application Flow

### 1. **User Onboarding**
- Welcome modal asks for email contact
- Input validation ensures proper email format
- Contact information stored for session

### 2. **Chat Experience**
```
User Question → AI Processing → Response + Metadata
    ↓
- ✅ Knowledge Base Match: Green "From KB" tag
- 🎫 Ticket Created: Orange "Ticket #123" tag  
- 💬 Contextual Response: Smart fallback handling
```

### 3. **Ticket Workflow**
```
Chat Issue → Auto Ticket → Support Dashboard → Status Updates
```

## 🎯 Component Architecture

```
src/
├── components/
│   ├── ChatInterface.tsx      # Main chat UI with message handling
│   ├── MessageBubble.tsx      # Individual message component
│   ├── TicketList.tsx         # Tickets table and management
│   └── KnowledgeBaseView.tsx  # KB browser and search
├── services/
│   └── api.ts                 # All backend API calls
├── types/
│   └── index.ts               # TypeScript interfaces
└── App.tsx                    # Main app with navigation
```

## 🔧 Configuration

### Environment Variables
Create `.env` file in frontend directory:
```bash
REACT_APP_API_URL=http://localhost:8000
```

### Backend Integration
The frontend expects these API endpoints:
- `POST /chat` - Send chat messages
- `GET /tickets` - List all tickets
- `PUT /tickets/{id}/status` - Update ticket status
- `GET /knowledge-base` - Browse Q&A pairs
- `GET /config/knowledge-bases` - List available KBs

## 🎨 UI Features

### Chat Interface
- **Message Types**: User messages (blue) vs AI responses (gray)
- **Metadata Tags**: Knowledge base matches and ticket creation
- **Typing Indicator**: Shows when AI is processing
- **Auto-scroll**: Always shows latest messages
- **Session Info**: Displays current session ID

### Ticket Management
- **Status Colors**: 
  - 🔴 Open (Red)
  - 🟠 In Progress (Orange)  
  - 🟢 Closed (Green)
- **Quick Actions**: View details, update status
- **Search & Filter**: Find tickets by content
- **Statistics**: Real-time ticket counts

### Knowledge Base
- **Search**: Find Q&A pairs by keyword
- **Switch KB**: Change between different knowledge bases
- **Stats**: Total Q&A count and search results
- **Responsive**: Pagination for large knowledge bases

## 📊 Performance

- **Bundle Size**: Optimized with code splitting
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages
- **Responsive**: Works on mobile and desktop
- **Accessibility**: ARIA labels and keyboard navigation

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Generate coverage report
npm test -- --coverage
```

## 🚀 Deployment

### Development
```bash
npm start          # Development server with hot reload
```

### Production
```bash
npm run build      # Creates optimized production build
npm install -g serve
serve -s build     # Serve production build locally
```

### Docker (Optional)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🎯 Key Features Showcase

### 1. **Smart Chat with Context**
```typescript
// Messages show AI capabilities
{
  content: "Based on my knowledge base...",
  isFromKB: true,        // Shows green "From KB" tag
  ticketCreated: false   // No ticket needed
}
```

### 2. **Automatic Ticket Creation**
```typescript
// When AI can't help
{
  content: "I'll connect you with support...",
  ticketCreated: true,   // Shows orange "Ticket #123" tag
  ticketId: 123
}
```

### 3. **Real-time Updates**
- Ticket status changes instantly
- Knowledge base switches seamlessly  
- Chat history persists during session

## 🔍 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

**Ready to chat!** 🤖💬 Start the backend server, then run `npm start` to launch the beautiful frontend interface.