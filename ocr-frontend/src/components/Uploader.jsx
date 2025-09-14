import React, { useState } from 'react';
import { Upload, message, Spin } from 'antd';
import { FileTextOutlined, ArrowUpOutlined } from '@ant-design/icons';

const { Dragger } = Upload;
const API_URL = import.meta.env?.VITE_API_URL || 'http://localhost:8000';

export default function Uploader({ onDone }) {
  const [loading, setLoading] = useState(false);

  const beforeUpload = (file) => {
    const okType = ['application/pdf', 'image/png', 'image/jpeg'].includes(file.type);
    if (!okType) { message.error('Only PDF, JPG, and PNG files are allowed.'); return Upload.LIST_IGNORE; }
    const okSize = file.size / 1024 / 1024 < 20;
    if (!okSize) { message.error('File must be smaller than 20MB.'); return Upload.LIST_IGNORE; }
    return true;
  };

  const customRequest = async ({ file, onSuccess, onError }) => {
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('file', file);

      const res = await fetch(`${API_URL}/upload`, { method: 'POST', body: fd });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || 'Upload failed');

      const result = {
        url: `${API_URL}${data.cleaned_url}`,
        mime: data.mime || 'application/octet-stream',
        json: data.fields || null,
        originalName: file.name,
      };
      onSuccess?.(data, file);
      onDone?.(result);
    } catch (e) {
      console.error(e);
      message.error(e.message || 'Upload error');
      onError?.(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Spin spinning={loading} tip="Processing file...">
      <Dragger
          name="file"
          multiple={false}
          accept=".pdf,.png,.jpg,.jpeg"
          beforeUpload={beforeUpload}
          customRequest={customRequest}
          showUploadList={false}
          className="uploader-card"
        >
          <div className="uploader-center">
            <div className="uploader-illustration">
              <FileTextOutlined className="doc" />
              <span className="badge"><ArrowUpOutlined /></span>
            </div>

            <div className="uploader-text">
              <div className="title">Drag-and-drop a PDF or JPG/PNG here</div>
              <div className="subtitle">or click to upload. Max 20 MB.</div>
            </div>
          </div>
        </Dragger>

    </Spin>
  );
}
