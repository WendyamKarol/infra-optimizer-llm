import { useState } from "react";
import UploadForm from "./components/UploadForm";
import MetricChart from "./components/MetricChart";
import RecommendationsTable from "./components/RecommendationsTable";

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [selectedMetric, setSelectedMetric] = useState("cpu_usage");

  return (
    <div className="App" style={{ padding: "20px" }}>
      <h1>📊 Infrastructure Dashboard</h1>
      <UploadForm onResult={(res) => setRecommendations(res.recommendations || [])} />
      <MetricChart metricName={selectedMetric} onMetricChange={setSelectedMetric} />
      <RecommendationsTable recommendations={recommendations} />
    </div>
  );
}

export default App;
