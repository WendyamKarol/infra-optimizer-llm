import { useState } from "react";
import axios from "axios";

const UploadForm = ({ onResult }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/api/chain/chain", formData);
      onResult(res.data);
    } catch (err) {
      console.error("Erreur d'upload :", err);
      alert("❌ L'analyse a échoué. Vérifie que le backend est actif.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>📤 Uploader un fichier JSON</h3>
      <input type="file" accept=".json" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyse en cours..." : "Analyser"}
      </button>
    </div>
  );
};

export default UploadForm;