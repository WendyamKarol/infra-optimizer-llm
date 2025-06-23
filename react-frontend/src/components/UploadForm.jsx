import { useState } from "react";
import axios from "axios";

// Composant de formulaire pour uploader un fichier JSON et lancer l'analyse
const UploadForm = ({ onResult }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fonction exécutée lors du clic sur le bouton d'upload
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

   // Préparation du fichier à envoyer au backend
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Appel à l'API backend FastAPI (POST /api/chain/chain)
      const res = await axios.post("http://localhost:8000/api/chain/chain", formData);
      // Transmission des résultats (recommandations) au composant parent
      onResult(res.data);
    } catch (err) {
      console.error("Erreur d'upload :", err);
      alert("❌ L'analyse a échoué. Vérifie que le backend est actif.");
    } finally {
      setLoading(false); // Réinitialisation de l'état de chargement
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