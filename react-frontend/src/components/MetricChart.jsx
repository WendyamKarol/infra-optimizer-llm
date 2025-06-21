import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Dot,
} from "recharts";

const AVAILABLE_METRICS = [
  "cpu_usage",
  "latency_ms",
  "error_rate",
  "temperature_celsius",
  "memory_usage",
  "disk_usage",
];

const MetricChart = ({ refreshKey }) => {
  const [metricName, setMetricName] = useState("cpu_usage");
  const [data, setData] = useState([]);
  const [selectedReasons, setSelectedReasons] = useState([]);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/api/metric/${metricName}`)
      .then((res) => {
        setData(res.data.data);
      })
      .catch((err) => {
        console.error("Erreur chargement métrique :", err);
      });
  }, [metricName, refreshKey]);

  const renderDot = (props) => {
    const { cx, cy, payload } = props;
    return payload.is_anomaly ? (
      <Dot cx={cx} cy={cy} r={6} fill="red" stroke="black" strokeWidth={1} />
    ) : null;
  };

  const handleAnalyzePoint = async (timestamp) => {
    try {
      const res = await axios.get(
        `http://localhost:8000/analyze?timestamp=${timestamp}`
      );
      if (res.data.is_anomaly) {
        alert(
          `📌 Résultat pour ${timestamp}\nAnomalie : Oui\nRaisons : ${res.data.anomaly_reasons.join(", ")}`
        );
        setSelectedReasons(res.data.anomaly_reasons);
      } else {
        alert(`📌 Résultat pour ${timestamp}\nAnomalie : Non`);
        setSelectedReasons([]);
      }
    } catch (err) {
      console.error("Erreur lors de l'analyse:", err);
      alert("Erreur lors de l'analyse.");
    }
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const point = payload[0].payload;
      return (
        <div style={{ background: "white", border: "1px solid #ccc", padding: 10 }}>
          <p>
            <strong>Timestamp:</strong> {point.timestamp}
          </p>
          <p>
            <strong>Valeur:</strong> {point.value}
          </p>
          {point.is_anomaly && (
            <>
              <p style={{ color: "red" }}>
                <strong>Anomalie détectée</strong>
              </p>
              <button onClick={() => handleAnalyzePoint(point.timestamp)}>
                Analyser ce point
              </button>
            </>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <h3>📊 Analyse des métriques</h3>
      <div style={{ marginBottom: "1em" }}>
        <label>
          Choisir une métrique :
          <select
            value={metricName}
            onChange={(e) => setMetricName(e.target.value)}
            style={{ marginLeft: "1em" }}
          >
            {AVAILABLE_METRICS.map((metric) => (
              <option key={metric} value={metric}>
                {metric}
              </option>
            ))}
          </select>
        </label>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            angle={-35}
            textAnchor="end"
            interval="preserveStartEnd"
            minTickGap={20}
          />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
            dot={renderDot}
          />
        </LineChart>
      </ResponsiveContainer>

      {selectedReasons.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h4>🧐 Raisons de l'anomalie</h4>
          {selectedReasons.map((reason, idx) => (
            <div
              key={idx}
              style={{
                display: "inline-block",
                background: "#fdd",
                color: "#900",
                padding: "4px 10px",
                margin: "5px",
                borderRadius: "5px",
              }}
            >
              {reason}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MetricChart;
