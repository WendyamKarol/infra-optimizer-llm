from typing import List, Tuple
from data_ingestion import MonitoringData

def detect_anomaly(data: MonitoringData) -> bool:
    if data.cpu_usage > 80:
        return True
    if data.latency_ms > 200:
        return True
    if data.error_rate > 0.05:
        return True
    if data.temperature_celsius > 75:
        return True
    if data.service_status.get("api_gateway") == "degraded":
        return True
    return False

def detect_anomalies_batch(data_list: List[MonitoringData]) -> List[Tuple[MonitoringData, bool]]:
    results = []
    for data in data_list:
        anomaly = detect_anomaly(data)
        results.append((data, anomaly))
    return results
"""
if __name__ == "__main__":
    from data_ingestion import ingest_data
    data_list = ingest_data()
    results = detect_anomalies_batch(data_list)
    for d, is_anomaly in results:
        status = "❌ ANOMALIE" if is_anomaly else "✅ Normal"
        print(f"{d.timestamp} | CPU: {d.cpu_usage}% | Latency: {d.latency_ms}ms | Status: {status}")"""
