import React, { useState, useEffect } from 'react';
import { Layout, Menu, Input, Button, Modal, Typography, message, List, Card, Tag, Divider } from 'antd';
import { 
  MessageOutlined, 
  FileTextOutlined, 
  BookOutlined, 
  MailOutlined,
  RobotOutlined,
  PlusOutlined,
  HistoryOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import ChatInterface from './components/ChatInterface';
import TicketList from './components/TicketList';
import KnowledgeBaseView from './components/KnowledgeBaseView';
import './App.css';

const { Header, Sider, Content } = Layout;
const { Title, Text } = Typography;

interface Session {
  session_id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  last_message: string | null;
}

const App: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [userContact, setUserContact] = useState('');
  const [sessionModalVisible, setSessionModalVisible] = useState(true);
  const [tempContact, setTempContact] = useState('');
  const [userSessions, setUserSessions] = useState<Session[]>([]);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [sessionStep, setSessionStep] = useState<'email' | 'sessions'>('email');
  const [loading, setLoading] = useState(false);

  const fetchUserSessions = async (email: string) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/sessions/${encodeURIComponent(email)}`);
      if (response.ok) {
        const sessions = await response.json();
        setUserSessions(sessions);
        return sessions;
      }
      return [];
    } catch (error) {
      console.error('Error fetching sessions:', error);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const handleEmailSubmit = async () => {
    if (!tempContact.trim()) {
      message.error('Please enter your email address');
      return;
    }
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(tempContact)) {
      message.error('Please enter a valid email address');
      return;
    }

    const sessions = await fetchUserSessions(tempContact);
    setUserContact(tempContact);
    
    if (sessions.length > 0) {
      setSessionStep('sessions');
    } else {
      // No previous sessions, start new chat
      setSessionModalVisible(false);
      message.success('Welcome to FAQ System! Starting a new conversation.');
    }
  };

  const handleSessionSelect = (sessionId: string) => {
    setSelectedSessionId(sessionId);
    setSessionModalVisible(false);
    message.success('Session loaded successfully!');
  };

  const handleNewSession = () => {
    setSelectedSessionId(null);
    setSessionModalVisible(false);
    message.success('Starting a new conversation!');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const menuItems = [
    {
      key: '1',
      icon: <MessageOutlined />,
      label: 'Chat Support',
      path: '/chat'
    },
    {
      key: '2',
      icon: <FileTextOutlined />,
      label: 'Support Tickets',
      path: '/tickets'
    },
    {
      key: '3',
      icon: <BookOutlined />,
      label: 'Knowledge Base',
      path: '/knowledge-base'
    }
  ];

  const [selectedKey, setSelectedKey] = useState('1');

  return (
    <div className="App">
      <Modal
        title={
          <div style={{ textAlign: 'center' }}>
            <RobotOutlined style={{ fontSize: '24px', marginRight: 8 }} />
            {sessionStep === 'email' ? 'Welcome to FAQ System' : 'Choose Your Session'}
          </div>
        }
        open={sessionModalVisible}
        onOk={sessionStep === 'email' ? handleEmailSubmit : undefined}
        closable={false}
        maskClosable={false}
        okText={sessionStep === 'email' ? 'Continue' : undefined}
        cancelButtonProps={{ style: { display: 'none' } }}
        footer={sessionStep === 'sessions' ? null : undefined}
        width={sessionStep === 'sessions' ? 600 : 400}
        loading={loading}
      >
        {sessionStep === 'email' ? (
          <>
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
              <Text>Please provide your email address to continue with our AI support system.</Text>
            </div>
            <Input
              prefix={<MailOutlined />}
              placeholder="Enter your email address"
              value={tempContact}
              onChange={(e) => setTempContact(e.target.value)}
              onPressEnter={handleEmailSubmit}
              size="large"
            />
          </>
        ) : (
          <>
            <div style={{ textAlign: 'center', marginBottom: 20 }}>
              <Text>We found {userSessions.length} previous conversation(s) for {userContact}.</Text>
              <br />
              <Text type="secondary">Choose to continue a previous conversation or start fresh.</Text>
            </div>
            
            <Button
              type="primary"
              size="large"
              icon={<PlusOutlined />}
              onClick={handleNewSession}
              block
              style={{ marginBottom: 16 }}
            >
              Start New Conversation
            </Button>
            
            <Divider>Or continue a previous conversation</Divider>
            
            <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
              <List
                dataSource={userSessions}
                renderItem={(session) => (
                  <Card
                    size="small"
                    hoverable
                    onClick={() => handleSessionSelect(session.session_id)}
                    style={{ marginBottom: 8, cursor: 'pointer' }}
                    bodyStyle={{ padding: '12px' }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div style={{ flex: 1 }}>
                        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
                          <HistoryOutlined style={{ marginRight: 6, color: '#1890ff' }} />
                          <Text strong>Session {session.session_id.substring(0, 8)}...</Text>
                          <Tag color="blue" style={{ marginLeft: 8 }}>
                            {session.message_count} messages
                          </Tag>
                        </div>
                        {session.last_message && (
                          <Text ellipsis style={{ color: '#666', fontSize: '12px' }}>
                            Last: "{session.last_message.substring(0, 60)}{session.last_message.length > 60 ? '...' : ''}"
                          </Text>
                        )}
                        <div style={{ marginTop: 4, fontSize: '11px', color: '#999' }}>
                          <ClockCircleOutlined style={{ marginRight: 4 }} />
                          {formatDate(session.updated_at)}
                        </div>
                      </div>
                    </div>
                  </Card>
                )}
              />
            </div>
          </>
        )}
      </Modal>

      <Layout style={{ minHeight: '100vh' }}>
        <Sider 
          collapsible 
          collapsed={collapsed} 
          onCollapse={setCollapsed}
          theme="light"
          style={{ boxShadow: '2px 0 6px rgba(0,21,41,0.35)' }}
        >
          <div style={{ 
            height: 64, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            borderBottom: '1px solid #f0f0f0'
          }}>
            <RobotOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
            {!collapsed && (
              <Title level={4} style={{ margin: '0 0 0 8px', color: '#1890ff' }}>
                FAQ System
              </Title>
            )}
          </div>
          
          <Menu
            mode="inline"
            selectedKeys={[selectedKey]}
            onClick={({ key }) => setSelectedKey(key)}
            style={{ borderRight: 0 }}
            items={menuItems}
          />
        </Sider>

        <Layout>
          <Header style={{ 
            padding: '0 24px', 
            background: '#fff', 
            borderBottom: '1px solid #f0f0f0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <Title level={3} style={{ margin: 0 }}>
              {menuItems.find(item => item.key === selectedKey)?.label}
            </Title>
            <div>
              <Text type="secondary">
                <MailOutlined style={{ marginRight: 4 }} />
                {userContact}
              </Text>
              <Button 
                type="link" 
                size="small" 
                onClick={() => {
                  setSessionModalVisible(true);
                  setSessionStep('email');
                  setTempContact(userContact);
                }}
              >
                Change
              </Button>
            </div>
          </Header>
          
          <Content style={{ 
            margin: '24px', 
            padding: '24px',
            background: '#fff',
            minHeight: 'calc(100vh - 112px)',
            borderRadius: '8px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)'
          }}>
            <div style={{ display: selectedKey === '1' ? 'block' : 'none' }}>
              <ChatInterface userContact={userContact} sessionId={selectedSessionId} />
            </div>
            <div style={{ display: selectedKey === '2' ? 'block' : 'none' }}>
              <TicketList />
            </div>
            <div style={{ display: selectedKey === '3' ? 'block' : 'none' }}>
              <KnowledgeBaseView />
            </div>
          </Content>
        </Layout>
      </Layout>
      
      {/* Mobile Navigation - Hidden on larger screens */}
      <div className="mobile-nav">
        {menuItems.map((item) => (
          <div
            key={item.key}
            className={`mobile-nav-item ${selectedKey === item.key ? 'active' : ''}`}
            onClick={() => setSelectedKey(item.key)}
          >
            {item.icon}
            <span style={{ fontSize: '10px', marginTop: '4px' }}>
              {item.label.split(' ')[0]}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;