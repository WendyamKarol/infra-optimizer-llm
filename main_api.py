from fastapi import FastAPI, Query
from typing import Optional, List
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.data_ingestion import MonitoringData
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API d'analyse des anomalies – en ligne 🚀"}

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
    filter: Optional[str] = Query(default=None, description="Type d'anomalie à filtrer (cpu, memory, latency, disk, service)")
):
    records = [MonitoringData(**item.dict()) for item in data]
    results = detect_anomalies_batch(records)

    anomalies = []
    for d, is_anomaly in results:
        if not is_anomaly:
            continue

        # ⚙️ Appliquer le filtre si spécifié
        if filter == "cpu" and (not d.cpu_usage or d.cpu_usage <= 90):
            continue
        if filter == "memory" and (not d.memory_usage or d.memory_usage <= 90):
            continue
        if filter == "latency" and (not d.latency_ms or d.latency_ms <= 300):
            continue
        if filter == "disk" and (not d.disk_usage or d.disk_usage <= 90):
            continue
        if filter == "service" and all(v == "online" for v in d.service_status.values()):
            continue

        anomalies.append({
            "timestamp": d.timestamp,
            "cpu": d.cpu_usage,
            "memory": d.memory_usage,
            "latency": d.latency_ms,
            "disk": d.disk_usage,
            "service_status": d.service_status
        })

    return {
        "filter": filter or "all",
        "count": len(anomalies),
        "anomalies": anomalies
    }
