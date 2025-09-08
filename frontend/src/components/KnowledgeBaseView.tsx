import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Typography, 
  List, 
  Input, 
  Space, 
  Button, 
  Select, 
  message, 
  Divider,
  Tag,
  Empty
} from 'antd';
import { 
  BookOutlined, 
  SearchOutlined, 
  ReloadOutlined, 
  SwapOutlined 
} from '@ant-design/icons';
import { getKnowledgeBase, getAvailableKnowledgeBases, switchKnowledgeBase } from '../services/api';
import { KnowledgeBase } from '../types';

const { Title, Text, Paragraph } = Typography;
const { Search } = Input;
const { Option } = Select;

const KnowledgeBaseView: React.FC = () => {
  const [knowledgeBase, setKnowledgeBase] = useState<KnowledgeBase | null>(null);
  const [availableKBs, setAvailableKBs] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [switchLoading, setSwitchLoading] = useState(false);
  const [pageSize, setPageSize] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);

  const fetchKnowledgeBase = async () => {
    setLoading(true);
    try {
      const [kbData, availableData] = await Promise.all([
        getKnowledgeBase(),
        getAvailableKnowledgeBases()
      ]);
      setKnowledgeBase(kbData);
      setAvailableKBs(availableData.available_kbs);
    } catch (error) {
      console.error('Error fetching knowledge base:', error);
      message.error('Failed to load knowledge base');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKnowledgeBase();
  }, []);

  const handleSwitchKB = async (kbName: string) => {
    setSwitchLoading(true);
    try {
      await switchKnowledgeBase(kbName);
      message.success(`Switched to ${kbName}`);
      fetchKnowledgeBase();
    } catch (error) {
      console.error('Error switching knowledge base:', error);
      message.error('Failed to switch knowledge base');
    } finally {
      setSwitchLoading(false);
    }
  };

  const filteredQAPairs = knowledgeBase?.qa_pairs.filter(
    qa => 
      qa.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      qa.answer.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    setCurrentPage(1);
  };

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Title level={4} style={{ margin: 0 }}>
            📚 Knowledge Base
          </Title>
          <Space>
            <Select
              placeholder="Switch KB"
              style={{ width: 150 }}
              loading={switchLoading}
              onChange={handleSwitchKB}
            >
              {availableKBs.map(kb => (
                <Option key={kb} value={kb}>
                  <SwapOutlined /> {kb}
                </Option>
              ))}
            </Select>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={fetchKnowledgeBase} 
              loading={loading}
            >
              Refresh
            </Button>
          </Space>
        </div>
        
        <Divider />
        
        <Space direction="vertical" style={{ width: '100%' }}>
          <Search
            placeholder="Search knowledge base..."
            allowClear
            enterButton={<SearchOutlined />}
            onSearch={handleSearch}
            onChange={(e) => handleSearch(e.target.value)}
            style={{ maxWidth: 400 }}
          />
          
          <Space>
            <Tag color="blue">
              Total: {knowledgeBase?.qa_pairs.length || 0} Q&As
            </Tag>
            {searchTerm && (
              <Tag color="green">
                Found: {filteredQAPairs.length} matches
              </Tag>
            )}
          </Space>
        </Space>
      </Card>

      {filteredQAPairs.length === 0 ? (
        <Card>
          <Empty 
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              searchTerm 
                ? `No results found for "${searchTerm}"`
                : "No Q&A pairs available"
            }
          />
        </Card>
      ) : (
        <List
          dataSource={filteredQAPairs}
          renderItem={(qa, index) => (
            <List.Item>
              <Card 
                size="small" 
                style={{ width: '100%' }}
                title={
                  <Space>
                    <BookOutlined />
                    <Text strong>Q{index + 1}:</Text>
                    <Text>{qa.question}</Text>
                  </Space>
                }
              >
                <Paragraph style={{ marginBottom: 0 }}>
                  <Text strong>Answer: </Text>
                  {qa.answer}
                </Paragraph>
              </Card>
            </List.Item>
          )}
          pagination={{
            current: currentPage,
            pageSize: pageSize,
            total: filteredQAPairs.length,
            showSizeChanger: true,
            pageSizeOptions: ['10', '20', '50', '100'],
            showQuickJumper: true,
            showTotal: (total, range) => 
              `${range[0]}-${range[1]} of ${total} items`,
            onChange: (page, size) => {
              setCurrentPage(page);
              if (size && size !== pageSize) {
                setPageSize(size);
                setCurrentPage(1);
              }
            },
            onShowSizeChange: (current, size) => {
              setPageSize(size);
              setCurrentPage(1);
            }
          }}
          loading={loading}
        />
      )}
    </div>
  );
};

export default KnowledgeBaseView;