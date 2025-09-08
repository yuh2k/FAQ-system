import React, { useState } from 'react';
import { Layout, Menu, Input, Button, Modal, Typography, message } from 'antd';
import { 
  MessageOutlined, 
  FileTextOutlined, 
  BookOutlined, 
  MailOutlined,
  RobotOutlined 
} from '@ant-design/icons';
import ChatInterface from './components/ChatInterface';
import TicketList from './components/TicketList';
import KnowledgeBaseView from './components/KnowledgeBaseView';
import './App.css';

const { Header, Sider, Content } = Layout;
const { Title, Text } = Typography;

const App: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [userContact, setUserContact] = useState('');
  const [contactModalVisible, setContactModalVisible] = useState(true);
  const [tempContact, setTempContact] = useState('');

  const handleContactSubmit = () => {
    if (!tempContact.trim()) {
      message.error('Please enter your contact information');
      return;
    }
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(tempContact)) {
      message.error('Please enter a valid email address');
      return;
    }

    setUserContact(tempContact);
    setContactModalVisible(false);
    message.success('Welcome to FAQ System!');
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
            Welcome to FAQ System
          </div>
        }
        open={contactModalVisible}
        onOk={handleContactSubmit}
        closable={false}
        maskClosable={false}
        okText="Start Chat"
        cancelButtonProps={{ style: { display: 'none' } }}
      >
        <div style={{ textAlign: 'center', marginBottom: 16 }}>
          <Text>Please provide your contact information to get started with our AI support system.</Text>
        </div>
        <Input
          prefix={<MailOutlined />}
          placeholder="Enter your email address"
          value={tempContact}
          onChange={(e) => setTempContact(e.target.value)}
          onPressEnter={handleContactSubmit}
          size="large"
        />
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
                onClick={() => setContactModalVisible(true)}
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
              <ChatInterface userContact={userContact} />
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
    </div>
  );
};

export default App;