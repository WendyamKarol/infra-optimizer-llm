from fastapi import FastAPI, Query
from typing import Optional, List
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.data_ingestion import MonitoringData
from pydantic import BaseModel
from typing import Dict
from nodes.recommandation import summarize_anomalies, generate_recommandation
from nodes.utils import save_to_json

app = FastAPI()

class MonitoringRecord(BaseModel):
    timestamp: str
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    latency_ms: Optional[float] = None
    disk_usage: Optional[float] = None
    network_in_kbps: Optional[float] = None
    network_out_kbps: Optional[float] = None
    io_wait: Optional[float] = None
    thread_count: Optional[int] = None
    active_connections: Optional[int] = None
    error_rate: Optional[float] = None
    uptime_seconds: Optional[int] = None
    temperature_celsius: Optional[float] = None
    power_consumption_watts: Optional[float] = None
    service_status: Optional[Dict[str, str]] = None

@app.post("/analyze")
def analyze(
    data: List[MonitoringRecord],
    filter: Optional[str] = Query(default=None, description="Types d'anomalies à filtrer séparés par des virgules (ex: cpu,memory,disk)")
):
    records = [MonitoringData(**item.dict()) for item in data]
    results = detect_anomalies_batch(records)

    # 🔄 Normaliser le filtre en liste de types
    filter_types = [f.strip().lower() for f in filter.split(",")] if filter else []

    anomalies = []
    for d, is_anomaly in results:
        if not is_anomaly:
            continue

        anomaly_types = []

        if d.cpu_usage and d.cpu_usage > 90:
            anomaly_types.append("cpu")
        if d.memory_usage and d.memory_usage > 90:
            anomaly_types.append("memory")
        if d.latency_ms and d.latency_ms > 300:
            anomaly_types.append("latency")
        if d.disk_usage and d.disk_usage > 90:
            anomaly_types.append("disk")
        if d.service_status and any(status != "online" for status in d.service_status.values()):
            anomaly_types.append("service")

        if filter_types and not any(t in filter_types for t in anomaly_types):
            continue

        anomalies.append({
            "timestamp": d.timestamp,
            "type": anomaly_types,
            "cpu": d.cpu_usage,
            "memory": d.memory_usage,
            "latency": d.latency_ms,
            "disk": d.disk_usage,
            "service_status": d.service_status
        })
    
    # 💾 Sauvegarder les anomalies détectées
    save_to_json(anomalies, "anomalies")

    return {
        "filter": filter_types or "all",
        "count": len(anomalies),
        "anomalies": anomalies
    }

@app.post("/recommandations")
def get_recommandation(
    anomalies: List[dict]
):
    summary = summarize_anomalies(anomalies)
    suggestion = generate_recommandation(summary)

    # 💾 Sauvegarder les recommandations générées
    save_to_json({
        "summary": summary,
        "recommandation": suggestion
    }, "recommandations")

    return {
        "summary": summary,
        "recommandation": suggestion
    }