import React, { useEffect, useMemo, useState } from 'react';
import { Layout, Typography, Tabs, Card, Space, Button, message, List, Tag, Popconfirm } from 'antd';
import { CloudUploadOutlined, DeleteOutlined, DownloadOutlined, HistoryOutlined, ReloadOutlined } from '@ant-design/icons';
import ErrorBoundary from './components/ErrorBoundary.jsx';
import Uploader from './components/Uploader.jsx';
import PreviewPane from './components/PreviewPane.jsx';
import JsonPane from './components/JsonPane.jsx';

const { Header, Content, Footer } = Layout;
const { Title, Text } = Typography;

const API_URL = import.meta.env?.VITE_API_URL || 'http://localhost:8000';
const HISTORY_KEY = 'ocr-history-v1';
const CURRENT_KEY = 'ocr-result';

export default function App() {
  const [result, setResult] = useState(null); // { url, mime, json, originalName, ts }
  const [history, setHistory] = useState([]);

  useEffect(() => {
    try {
      const saved = localStorage.getItem(CURRENT_KEY);
      if (saved) setResult(JSON.parse(saved));
      const hist = localStorage.getItem(HISTORY_KEY);
      if (hist) setHistory(JSON.parse(hist));
    } catch (e) {
      console.error('LocalStorage parse error', e);
    }
  }, []);

  useEffect(() => {
    try {
      if (result) {
        localStorage.setItem(CURRENT_KEY, JSON.stringify(result));
        const nextHistory = [result, ...history].slice(0, 8);
        setHistory(nextHistory);
        localStorage.setItem(HISTORY_KEY, JSON.stringify(nextHistory));
      }
    } catch (e) {
      console.error('LocalStorage write error', e);
    }
  }, [result]);

  const handleOnDone = (res) => {
    const withTs = { ...res, ts: Date.now() };
    setResult(withTs);
    message.success('Uploaded ✔');
  };

  const handleDeleteCurrent = () => {
    setResult(null);
    try { localStorage.removeItem(CURRENT_KEY); } catch {}
    message.success('Removed from session');
  };

  const handleClearHistory = () => {
    setHistory([]);
    try { localStorage.removeItem(HISTORY_KEY); } catch {}
    message.success('History cleared');
  };

  const downloadUrl = result?.url;

  const tabs = useMemo(() => ([
    { key: 'preview', label: 'Preview', children: <PreviewPane result={result} />, forceRender: true },
    { key: 'json', label: 'JSON (fields)', children: <JsonPane result={result} />, forceRender: true },
  ]), [result]);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#fff', borderBottom: '1px solid #f0f0f0' }}>
        <div className="container" style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <CloudUploadOutlined style={{ fontSize: 24 }} />
          <Title level={4} style={{ margin: 0 }}>OCR 2.0 Demo</Title>
          <Tag color="blue" style={{ marginLeft: 'auto' }}>API: {API_URL}</Tag>
        </div>
      </Header>

      <Content>
        <div className="container">
          <ErrorBoundary>
            <Card>
              <Uploader onDone={handleOnDone} />
            </Card>

            {result && (
              <Card
                className="preview"
                title={result.originalName || 'Processed Document'}
                extra={
                  <Space>
                    <Button type="default" icon={<ReloadOutlined />} onClick={() => setResult({ ...result })}>
                      Refresh
                    </Button>
                    <Button type="primary" icon={<DownloadOutlined />} href={downloadUrl} target="_blank">
                      Download
                    </Button>
                    <Popconfirm title="Remove current document from session?" onConfirm={handleDeleteCurrent} okText="Remove">
                      <Button danger icon={<DeleteOutlined />}>Delete</Button>
                    </Popconfirm>
                  </Space>
                }
              >
                <Tabs
                  defaultActiveKey="preview"
                  destroyInactiveTabPane={false}
                  items={tabs}
                />
              </Card>
            )}

            {history.length > 0 && (
              <Card
                title={<><HistoryOutlined /> <span style={{ marginLeft: 8 }}>Recent Documents</span></>}
                style={{ marginTop: 16 }}
                extra={<Button size="small" onClick={handleClearHistory}>Clear history</Button>}
              >
                <List
                  size="small"
                  dataSource={history}
                  renderItem={(it) => (
                    <List.Item
                      actions={[
                        <Button
                          key="download"
                          type="link"
                          icon={<DownloadOutlined />}
                          href={it.url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          Download
                        </Button>,
                      ]}
                    >
                      <List.Item.Meta
                        title={it.originalName || 'Document'}
                        description={new Date(it.ts).toLocaleString()}
                      />
                    </List.Item>
                  )}
                />
              </Card>
            )}
          </ErrorBoundary>
        </div>
      </Content>

      <Footer className="center">
        <Text type="secondary">© {new Date().getFullYear()} OCR Demo Team Solar Spark</Text>
      </Footer>
    </Layout>
  );
}
