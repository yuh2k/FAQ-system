import React from 'react';
import { Avatar, Card, Tag, Typography, Button, Space } from 'antd';
import { UserOutlined, RobotOutlined, BookOutlined, ExclamationCircleOutlined, FileTextOutlined, CloseOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { Message } from '../types';

const { Text, Paragraph } = Typography;

interface MessageBubbleProps {
  message: Message;
  onChoiceButtonClick?: (choice: string) => void;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onChoiceButtonClick }) => {
  const isUser = message.sender === 'user';
  
  // Parse choice buttons from message content
  const parseChoiceButtons = (content: string) => {
    const startMarker = '**CHOICE_BUTTONS_START**';
    const endMarker = '**CHOICE_BUTTONS_END**';
    
    if (!content.includes(startMarker) || !content.includes(endMarker)) {
      return { hasButtons: false, messageContent: content, buttons: [] };
    }
    
    const startIndex = content.indexOf(startMarker);
    const endIndex = content.indexOf(endMarker);
    
    const beforeButtons = content.substring(0, startIndex).trim();
    const buttonSection = content.substring(startIndex + startMarker.length, endIndex).trim();
    const afterButtons = content.substring(endIndex + endMarker.length).trim();
    
    const buttons = buttonSection.split('\n').filter(line => line.trim()).map(line => {
      const [action, label, description] = line.split('|');
      return { action: action.trim(), label: label.trim(), description: description.trim() };
    });
    
    return {
      hasButtons: true,
      messageContent: beforeButtons + (afterButtons ? '\n\n' + afterButtons : ''),
      buttons
    };
  };
  
  const { hasButtons, messageContent, buttons } = !isUser ? parseChoiceButtons(message.content) : { hasButtons: false, messageContent: message.content, buttons: [] };
  
  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: 16,
      alignItems: 'flex-start'
    }}>
      {!isUser && (
        <Avatar 
          icon={<RobotOutlined />} 
          style={{ 
            backgroundColor: '#1890ff',
            marginRight: 8,
            flexShrink: 0
          }} 
        />
      )}
      
      <div style={{ maxWidth: '70%' }}>
        <Card
          size="small"
          style={{
            backgroundColor: isUser ? '#1890ff' : '#f6f6f6',
            color: isUser ? 'white' : 'black',
            borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
            border: 'none',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}
          styles={{
            body: { 
              padding: '8px 12px',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }
          }}
        >
          {isUser ? (
            <Paragraph 
              style={{ 
                margin: 0, 
                color: 'white',
                fontSize: '14px',
                lineHeight: '1.5'
              }}
            >
              {message.content}
            </Paragraph>
          ) : (
            <div 
              style={{ 
                margin: 0,
                color: 'rgba(0, 0, 0, 0.85)',
                fontSize: '14px',
                lineHeight: '1.5'
              }}
            >
              <ReactMarkdown
                components={{
                  p: ({ children }) => <p style={{ margin: '0 0 8px 0' }}>{children}</p>,
                  ul: ({ children }) => <ul style={{ margin: '0 0 8px 0', paddingLeft: '16px' }}>{children}</ul>,
                  ol: ({ children }) => <ol style={{ margin: '0 0 8px 0', paddingLeft: '16px' }}>{children}</ol>,
                  li: ({ children }) => <li style={{ margin: '2px 0' }}>{children}</li>,
                  strong: ({ children }) => <strong style={{ fontWeight: 600 }}>{children}</strong>,
                  em: ({ children }) => <em style={{ fontStyle: 'italic' }}>{children}</em>,
                  h1: ({ children }) => <h1 style={{ fontSize: '16px', margin: '0 0 8px 0', fontWeight: 600 }}>{children}</h1>,
                  h2: ({ children }) => <h2 style={{ fontSize: '15px', margin: '0 0 6px 0', fontWeight: 600 }}>{children}</h2>,
                  h3: ({ children }) => <h3 style={{ fontSize: '14px', margin: '0 0 4px 0', fontWeight: 600 }}>{children}</h3>,
                }}
              >
                {messageContent}
              </ReactMarkdown>
              
              {hasButtons && buttons.length > 0 && (
                <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid #f0f0f0' }}>
                  <Space direction="vertical" style={{ width: '100%' }}>
                    {buttons.map((button, index) => (
                      <Button
                        key={index}
                        type={button.action === 'CREATE_TICKET' ? 'primary' : 'default'}
                        icon={button.action === 'CREATE_TICKET' ? <FileTextOutlined /> : <CloseOutlined />}
                        onClick={() => onChoiceButtonClick?.(button.action.toLowerCase())}
                        style={{
                          width: '100%',
                          height: 'auto',
                          padding: '8px 12px',
                          textAlign: 'left',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'flex-start'
                        }}
                      >
                        <div>
                          <div style={{ fontWeight: 600 }}>{button.label}</div>
                          <div style={{ fontSize: '12px', opacity: 0.8, marginTop: '2px' }}>
                            {button.description}
                          </div>
                        </div>
                      </Button>
                    ))}
                  </Space>
                </div>
              )}
            </div>
          )}
          
          {!isUser && (
            <div style={{ marginTop: 8, display: 'flex', gap: 4, flexWrap: 'wrap' }}>
              {message.isFromKB && (
                <Tag 
                  icon={<BookOutlined />} 
                  color="green"
                >
                  From KB
                </Tag>
              )}
              {message.ticketCreated && (
                <Tag 
                  icon={<ExclamationCircleOutlined />} 
                  color="orange"
                >
                  Ticket #{message.ticketId}
                </Tag>
              )}
            </div>
          )}
        </Card>
        
        <Text 
          type="secondary" 
          style={{ 
            fontSize: '12px',
            marginTop: 4,
            display: 'block',
            textAlign: isUser ? 'right' : 'left'
          }}
        >
          {message.timestamp.toLocaleTimeString()}
        </Text>
      </div>
      
      {isUser && (
        <Avatar 
          icon={<UserOutlined />} 
          style={{ 
            backgroundColor: '#52c41a',
            marginLeft: 8,
            flexShrink: 0
          }} 
        />
      )}
    </div>
  );
};

export default MessageBubble;