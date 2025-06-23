from typing import Dict, List
from nodes.data_ingestion import MonitoringData,ingest_data

def detect_anomaly(data: MonitoringData) -> Dict:
    anomaly_reasons = []

    if data.cpu_usage > 80:
        anomaly_reasons.append("High CPU usage")
    if data.latency_ms > 200:
        anomaly_reasons.append("High latency")
    if data.error_rate > 0.05:
        anomaly_reasons.append("High error rate")
    if data.temperature_celsius > 75:
        anomaly_reasons.append("High temperature")
    if data.service_status.get("api_gateway") == "degraded":
        anomaly_reasons.append("API Gateway degraded")

    return {
        "timestamp": data.timestamp,
        "metrics": data,
        "is_anomaly": bool(anomaly_reasons),
        "anomaly_reasons": anomaly_reasons
    }

def detect_anomalies_batch(data_list: List[MonitoringData]) -> List[Dict]:
    return [detect_anomaly(data) for data in data_list]

"""# Test manuel pour executer le fichier directement
if __name__ == "__main__":

    data_list = ingest_data()
    results = detect_anomalies_batch(data_list)
    
    for result in results:
        status = "❌ ANOMALIE" if result["is_anomaly"] else "✅ Normal"
        reasons = ", ".join(result["anomaly_reasons"])
        print(f"{result['timestamp']} | Status: {status} | Reasons: {reasons}")
"""