import React from 'react';
import { Tag, Tooltip } from 'antd';

export default function JsonValidityTag({ fields, requiredKeys = [] }) {
  if (!fields) return null;
  const missing = requiredKeys.filter((k) => !(k in fields) || fields[k] === null || fields[k] === '');
  if (missing.length === 0) return <Tag color="green">JSON valid</Tag>;
  return (
    <Tooltip title={`Missing: ${missing.join(', ')}`}>
      <Tag color="red">JSON invalid</Tag>
    </Tooltip>
  );
}
