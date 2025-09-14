import React from 'react';
import { Row, Col, Card, Statistic, Progress, Table, Empty, Tag } from 'antd';

export default function MetricsPane({ result }) {
  const m = result?.metrics;
  if (!m) return <Empty description="No metrics yet" />;

  const rows = Object.entries(m.fieldsF1 || {}).map(([field, f1]) => ({ key: field, field, f1 }));
  const cols = [
    { title: 'Field', dataIndex: 'field' },
    { title: 'F1-score', dataIndex: 'f1', render: (v) => (typeof v === 'number' ? v.toFixed(3) : v) },
  ];

  return (
    <>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}><Card><Statistic title="CER" value={m.cer} precision={3} /></Card></Col>
        <Col span={6}><Card><Statistic title="WER" value={m.wer} precision={3} /></Card></Col>
        <Col span={6}><Card><Statistic title="Exact Match % (docs)" value={m.exactMatchPct} suffix="%" precision={1} /></Card></Col>
        <Col span={6}><Card><Statistic title="JSON Validity" value={m.jsonValidityPct} suffix="%" precision={1} /></Card></Col>
      </Row>

      {m.noisy && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}><Card size="small" title={<Tag color="orange">Noisy subset</Tag>}><Statistic title="CER" value={m.noisy.cer} precision={3} /></Card></Col>
          <Col span={6}><Card size="small" title={<Tag color="orange">Noisy subset</Tag>}><Statistic title="WER" value={m.noisy.wer} precision={3} /></Card></Col>
        </Row>
      )}

      <Card title="Field-level F1 (macro)">
        <Progress percent={Math.round((m.macroF1 || 0) * 100)} status="active" />
        <Table size="small" columns={cols} dataSource={rows} style={{ marginTop: 16 }} pagination={false} />
      </Card>
    </>
  );
}
