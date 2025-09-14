import React, { useMemo } from 'react';
import { Descriptions, Statistic, Row, Col, Empty, Card, Space, Tag } from 'antd';
import JsonValidityTag from './JsonValidityTag.jsx';

export default function JsonPane({ result }) {
  const fields = result?.json;
  if (!fields) return <Empty description="No extracted fields yet" />;

  const totalAmount = fields.total_amount ?? fields.amount ?? null;
  const currency = fields.currency ?? '';
  const docDate = fields.date ?? fields.document_date ?? null;

  const docType = (fields.document_type || '').toLowerCase();
  const requiredKeys = useMemo(() => {
    if (docType.includes('invoice')) return ['document_type', 'date', 'total_amount', 'currency', 'invoice_number'];
    if (docType.includes('receipt')) return ['document_type', 'date', 'total_amount', 'currency'];
    if (docType.includes('statement')) return ['document_type', 'date'];
    return ['document_type', 'date'];
  }, [docType]);

  const shownKeys = new Set(['total_amount', 'amount', 'currency', 'date', 'document_date']);
  const otherFields = Object.entries(fields).filter(([k]) => !shownKeys.has(k));

  return (
    <>
      <Space style={{ marginBottom: 12 }}>
        <Tag>{docType || 'document'}</Tag>
        <JsonValidityTag fields={fields} requiredKeys={requiredKeys} />
      </Space>

      {(totalAmount || docDate) && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          {totalAmount && (
            <Col span={8}><Card><Statistic title="Total Amount" value={totalAmount} suffix={currency} /></Card></Col>
          )}
          {docDate && (
            <Col span={8}><Card><Statistic title="Document Date" value={docDate} /></Card></Col>
          )}
        </Row>
      )}

      <Descriptions bordered column={2} size="middle">
        {otherFields.map(([key, value]) => (
          <Descriptions.Item key={key} label={key}>
            {String(value)}
          </Descriptions.Item>
        ))}
      </Descriptions>
    </>
  );
}
