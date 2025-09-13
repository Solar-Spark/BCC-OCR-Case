import React, { useState } from "react";

export default function UploadBox() {
  const [cleaned, setCleaned] = useState(null); // { url, mime }

  const handleChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const fd = new FormData();
    fd.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: fd,
      });
      const data = await res.json();
      console.log("upload response:", data);

      // backend returns relative path; make it absolute
      const url = `http://localhost:8000${data.cleaned_url}`;
      setCleaned({ url, mime: data.mime });
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={handleChange} />

      {cleaned && (
        <div style={{ marginTop: 16 }}>
          <h3>Cleaned Preview</h3>

          {cleaned.mime?.startsWith("image/") ? (
            <img src={cleaned.url} alt="cleaned" style={{ maxWidth: 480 }} />
          ) : cleaned.mime === "application/pdf" ? (
            <object
              data={cleaned.url}
              type="application/pdf"
              width="480"
              height="600"
            >
              <a href={cleaned.url} target="_blank" rel="noreferrer">
                Open PDF
              </a>
            </object>
          ) : (
            <a href={cleaned.url} target="_blank" rel="noreferrer">
              Download cleaned file
            </a>
          )}
        </div>
      )}
    </div>
  );
}
