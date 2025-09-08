import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Tag, 
  Button, 
  Space, 
  Card, 
  Typography, 
  Modal, 
  Select, 
  message,
  Tooltip,
  Badge
} from 'antd';
import { 
  EyeOutlined, 
  EditOutlined, 
  ReloadOutlined,
  ExclamationCircleOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import { Ticket } from '../types';
import { getTickets, updateTicketStatus } from '../services/api';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

const TicketList: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [updateLoading, setUpdateLoading] = useState(false);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const ticketsData = await getTickets();
      setTickets(ticketsData);
    } catch (error) {
      console.error('Error fetching tickets:', error);
      message.error('Failed to load tickets');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const handleStatusUpdate = async (ticketId: number, newStatus: 'open' | 'in_progress' | 'closed') => {
    setUpdateLoading(true);
    try {
      await updateTicketStatus(ticketId, newStatus);
      message.success(`Ticket status updated to ${newStatus}`);
      fetchTickets(); // Refresh the list
      if (selectedTicket && selectedTicket.id === ticketId) {
        setSelectedTicket({ ...selectedTicket, status: newStatus });
      }
    } catch (error) {
      console.error('Error updating ticket status:', error);
      message.error('Failed to update ticket status');
    } finally {
      setUpdateLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'red';
      case 'in_progress': return 'orange';
      case 'closed': return 'green';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open': return <ExclamationCircleOutlined />;
      case 'in_progress': return <ClockCircleOutlined />;
      case 'closed': return <CheckCircleOutlined />;
      default: return null;
    }
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
      render: (id: number) => <Text strong>#{id}</Text>,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status: string) => (
        <Tag color={getStatusColor(status)} icon={getStatusIcon(status)}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'User Question',
      dataIndex: 'user_question',
      key: 'user_question',
      ellipsis: true,
      render: (text: string) => (
        <Tooltip title={text}>
          <Text>{text.length > 50 ? `${text.substring(0, 50)}...` : text}</Text>
        </Tooltip>
      ),
    },
    {
      title: 'Contact',
      dataIndex: 'user_contact',
      key: 'user_contact',
      width: 180,
      render: (contact: string) => <Text type="secondary">{contact}</Text>,
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 120,
      render: (date: string) => (
        <Text type="secondary">
          {new Date(date).toLocaleDateString()}
        </Text>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 150,
      render: (record: Ticket) => (
        <Space>
          <Tooltip title="View Details">
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => {
                setSelectedTicket(record);
                setModalVisible(true);
              }}
            />
          </Tooltip>
          <Tooltip title="Update Status">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => {
                setSelectedTicket(record);
                setModalVisible(true);
              }}
            />
          </Tooltip>
        </Space>
      ),
    },
  ];

  const getTicketStats = () => {
    const open = tickets.filter(t => t.status === 'open').length;
    const inProgress = tickets.filter(t => t.status === 'in_progress').length;
    const closed = tickets.filter(t => t.status === 'closed').length;
    return { open, inProgress, closed };
  };

  const stats = getTicketStats();

  return (
    <div>
      {/* Header with Stats */}
      <Card style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={4} style={{ margin: 0 }}>
            🎫 Support Tickets
          </Title>
          <Button icon={<ReloadOutlined />} onClick={fetchTickets} loading={loading}>
            Refresh
          </Button>
        </div>
        
        <Space size="large">
          <Badge count={stats.open} color="red">
            <Text>Open: {stats.open}</Text>
          </Badge>
          <Badge count={stats.inProgress} color="orange">
            <Text>In Progress: {stats.inProgress}</Text>
          </Badge>
          <Badge count={stats.closed} color="green">
            <Text>Closed: {stats.closed}</Text>
          </Badge>
          <Text type="secondary">Total: {tickets.length}</Text>
        </Space>
      </Card>

      {/* Tickets Table */}
      <Table
        dataSource={tickets}
        columns={columns}
        rowKey="id"
        loading={loading}
        pagination={{
          pageSize: 10,
          showSizeChanger: true,
          showTotal: (total) => `Total ${total} tickets`,
        }}
        scroll={{ x: 800 }}
      />

      {/* Ticket Detail Modal */}
      <Modal
        title={`Ticket #${selectedTicket?.id} Details`}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setSelectedTicket(null);
        }}
        footer={[
          <Button key="close" onClick={() => setModalVisible(false)}>
            Close
          </Button>
        ]}
        width={700}
      >
        {selectedTicket && (
          <div>
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              {/* Status Update */}
              <div>
                <Text strong>Status: </Text>
                <Select
                  value={selectedTicket.status}
                  style={{ width: 120, marginLeft: 8 }}
                  loading={updateLoading}
                  onChange={(value) => handleStatusUpdate(selectedTicket.id, value)}
                >
                  <Option value="open">Open</Option>
                  <Option value="in_progress">In Progress</Option>
                  <Option value="closed">Closed</Option>
                </Select>
              </div>

              {/* Ticket Info */}
              <div>
                <Text strong>User Contact: </Text>
                <Text copyable>{selectedTicket.user_contact}</Text>
              </div>
              
              <div>
                <Text strong>Session ID: </Text>
                <Text copyable code>{selectedTicket.session_id}</Text>
              </div>

              <div>
                <Text strong>Created At: </Text>
                <Text>{new Date(selectedTicket.created_at).toLocaleString()}</Text>
              </div>

              {/* User Question */}
              <div>
                <Text strong>User Question:</Text>
                <Card size="small" style={{ marginTop: 8, backgroundColor: '#f6f6f6' }}>
                  <Paragraph>{selectedTicket.user_question}</Paragraph>
                </Card>
              </div>

              {/* AI Response */}
              <div>
                <Text strong>AI Attempted Response:</Text>
                <Card size="small" style={{ marginTop: 8, backgroundColor: '#e6f7ff' }}>
                  <Paragraph>{selectedTicket.ai_attempted_response}</Paragraph>
                </Card>
              </div>
            </Space>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default TicketList;