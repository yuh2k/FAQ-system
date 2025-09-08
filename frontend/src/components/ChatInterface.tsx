import React, { useState, useRef, useEffect } from 'react';
import { Input, Button, Card, Space, Alert, Typography, Spin } from 'antd';
import { SendOutlined, ClearOutlined } from '@ant-design/icons';
import { Message } from '../types';
import { sendMessage } from '../services/api';
import MessageBubble from './MessageBubble';

const { Title } = Typography;

interface ChatInterfaceProps {
  userContact: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ userContact }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [error, setError] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const welcomeMessage: Message = {
      id: 'welcome',
      content: 'Hello! I\'m your AI assistant. I can help answer questions about automotive topics. How can I assist you today?',
      sender: 'ai',
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);
    setError('');

    try {
      const response = await sendMessage({
        message: inputValue.trim(),
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
        setError(`A support ticket #${response.ticket_id} has been created for further assistance.`);
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
            <MessageBubble key={message.id} message={message} />
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
            onClick={handleSendMessage}
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
      </Card>
    </div>
  );
};

export default ChatInterface;