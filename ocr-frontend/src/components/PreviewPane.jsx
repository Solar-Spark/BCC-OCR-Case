import React from 'react';

export default function PreviewPane({ result }) {
  if (!result) return null;
  const { url, mime } = result;

  if (mime?.startsWith('image/')) {
    return <img src={url} alt="cleaned" style={{ maxWidth: '100%', display: 'block' }} />;
  }

  if (mime === 'application/pdf') {
    return (
      <iframe
        src={url}
        title="cleaned-pdf"
        width="100%"
        height="720"
        style={{ border: 'none' }}
      />
    );
  }

  return <a href={url} target="_blank" rel="noreferrer">Download cleaned file</a>;
}
