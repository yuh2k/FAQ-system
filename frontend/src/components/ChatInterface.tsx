import React, { useState, useRef, useEffect } from 'react';
import { Input, Button, Card, Space, Alert, Typography, Spin } from 'antd';
import { SendOutlined, ClearOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { Message } from '../types';
import { sendMessage } from '../services/api';
import MessageBubble from './MessageBubble';

const { Title } = Typography;

interface ChatInterfaceProps {
  userContact: string;
  sessionId: string | null;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ userContact, sessionId: propSessionId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [chatDisabled, setChatDisabled] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load session messages when propSessionId changes
  useEffect(() => {
    if (propSessionId) {
      setSessionId(propSessionId);
      loadSessionHistory(propSessionId);
    } else {
      // New session - show welcome message and reset states
      const welcomeMessage: Message = {
        id: 'welcome',
        content: 'Hello! I\'m your AI assistant. I can help answer questions about automotive topics. How can I assist you today?',
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
      setSessionId('');
      setChatDisabled(false);
    }
  }, [propSessionId]);

  const loadSessionHistory = async (sessionIdToLoad: string) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/chat/history/${sessionIdToLoad}`);
      if (response.ok) {
        const history = await response.json();
        const loadedMessages: Message[] = [];
        
        history.forEach((item: any, index: number) => {
          // Add user message
          loadedMessages.push({
            id: `loaded-user-${index}`,
            content: item.message,
            sender: 'user',
            timestamp: new Date(item.created_at),
          });
          
          // Add AI response
          loadedMessages.push({
            id: `loaded-ai-${index}`,
            content: item.response,
            sender: 'ai',
            timestamp: new Date(item.created_at),
          });
        });
        
        setMessages(loadedMessages);
      } else {
        throw new Error('Failed to load session history');
      }
    } catch (error) {
      console.error('Error loading session history:', error);
      setError('Failed to load conversation history');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (overrideMessage?: string) => {
    const messageToSend = overrideMessage || inputValue.trim();
    if (!messageToSend) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: messageToSend,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    if (!overrideMessage) {
      setInputValue('');
    }
    setLoading(true);
    setError('');

    try {
      const response = await sendMessage({
        message: messageToSend,
        user_contact: userContact,
        session_id: sessionId || undefined,
      });

      if (!sessionId) {
        setSessionId(response.session_id);
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        sender: 'ai',
        timestamp: new Date(),
        isFromKB: response.is_from_kb,
        ticketCreated: response.ticket_created,
        ticketId: response.ticket_id || undefined,
      };

      setMessages(prev => [...prev, aiMessage]);

      if (response.ticket_created) {
        setChatDisabled(true);
        setError(`A support ticket #${response.ticket_id} has been created for further assistance. The conversation has been ended.`);
      }

    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setSessionId('');
    setError('');
    
    const welcomeMessage: Message = {
      id: 'welcome-new',
      content: 'Chat cleared. How can I help you?',
      sender: 'ai',
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  };

  const handleChoiceButtonClick = async (choice: string) => {
    // Send the choice as a message
    await handleSendMessage(choice);
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Card size="small" style={{ marginBottom: 16, flexShrink: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Title level={4} style={{ margin: 0 }}>
            💬 AI Customer Support
          </Title>
          <Space>
            {sessionId && (
              <Typography.Text type="secondary" style={{ fontSize: '12px' }}>
                Session: {sessionId.slice(0, 8)}...
              </Typography.Text>
            )}
            <Button 
              icon={<ClearOutlined />} 
              onClick={handleClearChat}
              type="text"
              size="small"
            >
              Clear
            </Button>
          </Space>
        </div>
      </Card>

      {error && (
        <Alert
          message={error}
          type={error.includes('ticket') ? 'info' : 'error'}
          closable
          onClose={() => setError('')}
          style={{ marginBottom: 16, flexShrink: 0 }}
        />
      )}

      <Card 
        style={{ 
          flex: 1, 
          marginBottom: 16,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        }}
        styles={{
          body: { 
            flex: 1, 
            overflowY: 'auto', 
            padding: '16px',
            maxHeight: 'calc(70vh - 200px)'
          }
        }}
      >
        <div>
          {messages.map((message) => (
            <MessageBubble 
              key={message.id} 
              message={message} 
              onChoiceButtonClick={handleChoiceButtonClick}
            />
          ))}
          {loading && (
            <div style={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center', marginBottom: 16 }}>
              <Spin size="small" style={{ marginRight: 8 }} />
              <Typography.Text type="secondary">AI is typing...</Typography.Text>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </Card>

      <Card size="small" style={{ flexShrink: 0 }}>
        {chatDisabled ? (
          <div style={{ textAlign: 'center', padding: '16px' }}>
            <CheckCircleOutlined style={{ fontSize: '24px', color: '#52c41a', marginBottom: '8px' }} />
            <Typography.Text strong style={{ display: 'block', marginBottom: '4px' }}>
              Conversation Ended
            </Typography.Text>
            <Typography.Text type="secondary" style={{ fontSize: '12px' }}>
              A support ticket has been created. Our team will contact you soon.
            </Typography.Text>
          </div>
        ) : (
          <>
            <Space.Compact style={{ width: '100%' }}>
              <Input.TextArea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
                autoSize={{ minRows: 1, maxRows: 4 }}
                disabled={loading}
                style={{ resize: 'none' }}
              />
              <Button 
                type="primary" 
                icon={<SendOutlined />}
                onClick={() => handleSendMessage()}
                loading={loading}
                disabled={!inputValue.trim()}
                style={{ height: 'auto', minHeight: '32px' }}
              >
                Send
              </Button>
            </Space.Compact>
            <Typography.Text 
              type="secondary" 
              style={{ fontSize: '11px', marginTop: 4, display: 'block' }}
            >
              Powered by AI • Knowledge Base Integration • Auto Ticket Creation
            </Typography.Text>
          </>
        )}
      </Card>
    </div>
  );
};

export default ChatInterface;