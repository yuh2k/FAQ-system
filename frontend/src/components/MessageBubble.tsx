import React from 'react';
import { Avatar, Card, Tag, Typography } from 'antd';
import { UserOutlined, RobotOutlined, BookOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { Message } from '../types';

const { Text, Paragraph } = Typography;

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  
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
          bodyStyle={{ 
            padding: '8px 12px',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word'
          }}
        >
          <Paragraph 
            style={{ 
              margin: 0, 
              color: isUser ? 'white' : 'rgba(0, 0, 0, 0.85)',
              fontSize: '14px',
              lineHeight: '1.5'
            }}
          >
            {message.content}
          </Paragraph>
          
          {/* AI Message metadata */}
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