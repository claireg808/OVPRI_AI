import React, { useState } from "react";
import axios from "axios";
import "./Redline.css";
import "/home/gillaspiecl/OVPRI_AI/Frontend/src/App.css";

const RedLine: React.FC = () => {
  const [docType, setDocType] = useState("Confidentiality Agreement");
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!file) {
    alert("Please upload a document.");
    return;
  }

  setIsProcessing(true);
  setResult(null);

  const formData = new FormData();
  formData.append("file", file);
  formData.append("type", docType);

  try {
    const response = await axios.post("http://localhost:5001/redline", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    setResult(response.data.redline); // expecting your Flask endpoint to return { redline: "..." }
  } catch (error) {
    console.error("Error submitting document:", error);
    setResult("An error occurred while processing your document.");
  } finally {
    setIsProcessing(false);
  }
};


return (
    <div className="App">
      <h1 className="redline-header">OVPRI AI Document Review</h1>
      <div className="redline-container">

        {!isProcessing && !result && (
          <form className="redline-form" onSubmit={handleSubmit}>
            <label className="redline-label">
              Type of Document:
              <select
                className="redline-select"
                value={docType}
                onChange={(e) => setDocType(e.target.value)}
              >
                <option value="Confidentiality Agreement">
                  Confidentiality Agreement
                </option>
              </select>
            </label>

            <label className="redline-label">
              Upload:
              <input
                type="file"
                accept=".doc,.docx,.pdf"
                className="redline-upload"
                onChange={handleFileChange}
              />
            </label>

            <button type="submit" className="redline-submit">
              Submit
            </button>
          </form>
        )}

        {isProcessing && (
          <div className="processing-screen">
            <h2>Processing your document...</h2>
            <div className="loader"></div>
          </div>
        )}

        {result && (
          <div className="result-screen">
            <h2>Revised Document:</h2>
            <pre className="result-text">{result}</pre>
            <button onClick={() => setResult(null)}>Submit Another</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default RedLine;