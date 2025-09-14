import React, { useMemo } from 'react';
import { Tabs, Descriptions, Row, Col, Card, Space, Tag, Typography, Empty } from 'antd';
import JsonValidityTag from './JsonValidityTag.jsx';

const { Text, Paragraph } = Typography;

// ---------- helpers
const titleMap = {
  document_type: 'Document Type',
  invoice_number: 'Invoice #',
  contract_number: 'Contract #',
};
function titleCase(label) {
  if (titleMap[label]) return titleMap[label];
  return label.replace(/_/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase());
}
function tryParseAmountFromString(str) {
  const m = String(str).match(/[\d\s.,]+/);
  if (!m) return null;
  const raw = m[0].replace(/\s/g, '').replace(/,(?=\d{3}\b)/g, '');
  const standardized = raw.replace(',', '.'); // best effort
  const n = Number(standardized);
  return isNaN(n) ? null : n;
}
function smartCurrencyGuess(fields, fallback) {
  const keys = Object.keys(fields);
  const key = keys.find(k => /(contract_currency|payment_currency|currency)$/i.test(k));
  const val = key ? String(fields[key]).toLowerCase() : '';
  if (val.includes('руб')) return 'RUB';
  if (val.includes('тенге') || val.includes('kzt')) return 'KZT';
  if (val.includes('usd') || val.includes('доллар')) return 'USD';
  if (val.includes('eur') || val.includes('евро')) return 'EUR';
  return fallback || (val ? val.toUpperCase() : undefined);
}
function formatAmount(value, currencyMaybe) {
  if (value == null) return '';
  if (typeof value === 'number') {
    try { return new Intl.NumberFormat('en-US', { style: 'currency', currency: currencyMaybe || 'USD' }).format(value); }
    catch { return `${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${currencyMaybe || ''}`.trim(); }
  }
  // string input
  const parsed = tryParseAmountFromString(value);
  if (parsed != null) {
    try { return new Intl.NumberFormat('en-US', { style: 'currency', currency: currencyMaybe || 'USD' }).format(parsed); }
    catch { return `${parsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${currencyMaybe || ''}`.trim(); }
  }
  // not parseable → show as-is
  return String(value);
}
function formatDate(iso) {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return String(iso ?? '');
  return d.toLocaleDateString('en-US', { day: '2-digit', month: 'short', year: 'numeric' });
}

export default function JsonPane({ result }) {
  const fields = result?.json;
  if (!fields) return <Empty description="No extracted fields yet" />;

  const keys = Object.keys(fields);

  // ---- detect doc kind from keys
  const docKind = useMemo(() => {
    const k = keys.join(' ');
    if (/contract_/i.test(k) || /contract_number/i.test(k)) return 'contract';
    if (/invoice_/i.test(k) || /invoice_number/i.test(k)) return 'invoice';
    if (/receipt/i.test(k)) return 'receipt';
    return 'document';
  }, [keys]);

  // ---- minimal required keys for validity (only if known kind)
  const requiredKeys = useMemo(() => {
    if (docKind === 'invoice') return ['date', 'total_amount', 'currency', 'invoice_number'];
    if (docKind === 'contract') return ['contract_number', 'contract_date', 'amount'];
    if (docKind === 'receipt') return ['date', 'total_amount', 'currency'];
    return null; // unknown → hide validity tag
  }, [docKind]);

  // ---- pick key facts dynamically
  const idKey = keys.find(k => /(invoice_number|contract_number|doc_number)$/i.test(k));
  const idVal = idKey ? fields[idKey] : null;

  const amountKey = keys.find(k => /(total_amount|amount|sum)$/i.test(k));
  const amountVal = amountKey ? fields[amountKey] : null;

  const currencyIso = smartCurrencyGuess(fields, fields.currency);
  const startDateKey = keys.find(k => /(contract_date|start_date|date)$/i.test(k));
  const endDateKey   = keys.find(k => /(end_date|finish_date)$/i.test(k));
  const startDateVal = startDateKey ? fields[startDateKey] : null;
  const endDateVal   = endDateKey ? fields[endDateKey] : null;

  // ---- build cards
  const cards = [];
  if (amountVal != null) {
    cards.push({
      label: 'Amount',
      value: formatAmount(amountVal, currencyIso),
      extra: currencyIso && typeof amountVal === 'string' && !/\p{Sc}/u.test(amountVal) ? '' : '',
    });
  }
  if (startDateVal) cards.push({ label: endDateVal ? 'Start / Contract Date' : 'Document Date', value: formatDate(startDateVal), small: `ISO: ${String(startDateVal)}` });
  if (endDateVal)   cards.push({ label: 'End Date', value: formatDate(endDateVal), small: `ISO: ${String(endDateVal)}` });
  if (idVal)        cards.push({ label: /contract/i.test(idKey || '') ? 'Contract #' : 'Document #', value: String(idVal) });

  const usedKeys = new Set([idKey, amountKey, startDateKey, endDateKey].filter(Boolean));

  // ---- remaining fields for the grid (sorted by label)
  const gridEntries = keys
    .filter(k => !usedKeys.has(k))
    .map(k => [titleCase(k), fields[k]])
    .sort((a, b) => a[0].localeCompare(b[0]));

  // ----- Formatted view (no copy icons here)
  const formatted = (
    <>
      <Space style={{ marginBottom: 12 }}>
        <Tag>{docKind}</Tag>
        {requiredKeys && <JsonValidityTag fields={fields} requiredKeys={requiredKeys} />}
      </Space>

      {cards.length > 0 && (
        <Row gutter={16} style={{ marginBottom: 16 }}>
          {cards.map((c, i) => (
            <Col key={i} xs={24} md={12} lg={8}>
              <Card>
                <Text type="secondary">{c.label}</Text>
                <div style={{ fontSize: 26, fontWeight: 600, marginTop: 4 }}>{c.value}</div>
                {c.small && <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>{c.small}</Text>}
              </Card>
            </Col>
          ))}
        </Row>
      )}

      <Descriptions
        bordered
        layout="vertical"
        column={{ xs: 1, sm: 2, lg: 3 }}
        labelStyle={{
          color: '#8c8c8c',
          textTransform: 'uppercase',
          letterSpacing: '.3px',
          fontSize: 12,
          fontWeight: 600,
        }}
        contentStyle={{
          fontSize: 16,
          fontWeight: 500,
          color: '#1f1f1f',
          wordBreak: 'break-word',
        }}
      >
        {gridEntries.map(([label, value]) => (
          <Descriptions.Item key={label} label={label}>
            {typeof value === 'object' ? JSON.stringify(value) : String(value)}
          </Descriptions.Item>
        ))}
      </Descriptions>
    </>
  );

  // ----- Raw JSON tab (copy whole payload)
  const raw = JSON.stringify(fields, null, 2);
  const rawView = (
    <Paragraph style={{ background: '#f6f8fa', padding: 12, borderRadius: 8, margin: 0 }} copyable={{ text: raw }}>
      <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{raw}</pre>
    </Paragraph>
  );

  return (
    <Tabs
      defaultActiveKey="formatted"
      destroyInactiveTabPane={false}
      items={[
        { key: 'formatted', label: 'Formatted', children: formatted, forceRender: true },
        { key: 'raw', label: 'Raw JSON', children: rawView, forceRender: true },
      ]}
    />
  );
}
