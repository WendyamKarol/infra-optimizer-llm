import React from "react";

// Composant de tableau affichant les recommandations générées par le LLM
const RecommendationsTable = ({ recommendations }) => {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div style={{ marginTop: "20px" }}>
        <p>📭 Aucune recommandation disponible pour l’instant.</p>
      </div>
    );
  }

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Recommandations générées par le LLM</h3>
      <div style={{ overflowX: "auto" }}>
        <table
          border="1"
          cellPadding="8"
          style={{
            borderCollapse: "collapse",
            width: "100%",
            backgroundColor: "#fff",
            fontSize: "0.9rem",
          }}
        >
          <thead style={{ backgroundColor: "#f0f0f0" }}>
            <tr>
              <th>⏱️ Timestamp</th>
              <th>🚨 Type</th>
              <th>📖 Explication</th>
              <th>💡 Suggestion</th>
            </tr>
          </thead>
          <tbody>
            {recommendations.map((reco, index) => (
              <tr key={index}>
                <td>{reco.timestamp}</td>
                <td>{reco.type}</td>
                <td>{reco.explanation}</td>
                <td>{reco.suggestion}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecommendationsTable;
