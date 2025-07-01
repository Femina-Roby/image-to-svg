import React, { useState } from "react";
import { gql, useMutation } from "@apollo/client";
import { FaDownload } from "react-icons/fa";
import '../glass-ui.css';

const UPLOAD_IMAGE = gql`
  mutation UploadImage($file: Upload!) {
    uploadImage(file: $file)
  }
`;

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [uploadImage] = useMutation(UPLOAD_IMAGE);
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true); // Start loading

  try {
    const { data } = await uploadImage({ variables: { file } });
    setResult(data.uploadImage);
  } catch (error) {
    console.error("Conversion error:", error);
  }

  setLoading(false); // End loading
};

  const handleDownload = () => {
    const blob = new Blob([result], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "converted.svg";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="glass-card">
      <h2>Convert Image to SVG</h2>

      <form onSubmit={handleSubmit}>
       <div className="upload-zone" onClick={() => document.getElementById("file-upload").click()}>
        {fileName && (
  <p style={{ marginTop: "1rem", color: "#f72585", fontWeight: "bold" }}>
    Selected: {fileName}
  </p>
)}
      <p>Select or drop your image here</p>
    </div>

          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={(e) => {
            const selected = e.target.files[0];
            setFile(selected);
            setFileName(selected?.name || "");}}
            style={{ display: "none" }}
          />

        <button
  type="submit"
  className="glass-button"
  disabled={loading}
  style={loading ? { opacity: 0.6, cursor: "not-allowed" } : {}}
>
  Convert
</button>

        {loading && (
  <p style={{ marginTop: "1rem", color: "#fff" }}>
    🔄 Converting image, please wait...
  </p>
)}
      </form>

      {result && (
        <div className="glass-preview">
          <h3>SVG Preview</h3>
          <div
            style={{
              background: "#fff",
              borderRadius: "12px",
              padding: "1rem",
              maxHeight: "60vh",
              overflow: "auto",
              marginTop: "1rem",
              color: "#000",
            }}
            dangerouslySetInnerHTML={{ __html: result }}
          />

          <button onClick={handleDownload} className="glass-button" style={{ marginTop: "1rem" }}>
            <FaDownload style={{ marginRight: "6px" }} /> Download SVG
          </button>
        </div>
      )}
    </div>
  );
}