import React, { useState } from 'react'
import UploadBox from '../components/UploadBox.jsx'

export default function DocumentLab() {
  const [file, setFile] = useState(null)

  return (
    <section style={{ marginTop: 16 }}>
      <h2>Upload Document</h2>
      <UploadBox onUpload={setFile} />
      {file && (
        <div style={{ marginTop: 8 }}>
          <strong>Selected:</strong> {file.name}
        </div>
      )}
    </section>
  )
}
