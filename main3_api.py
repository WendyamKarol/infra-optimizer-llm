from fastapi import FastAPI, Query
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.data_ingestion import MonitoringData
from nodes.recommandation import summarize_anomalies, generate_recommandation
from typing import List

app = FastAPI()

@app.post("/full-analysis")
def full_analysis(data: List[MonitoringData]):
    raw_anomalies = detect_anomalies_batch(data)

    structured = []
    for record, is_anomaly in raw_anomalies:
        if is_anomaly:
            structured.append({
                "timestamp": record.timestamp,
                "type": record.detected_types,
                "cpu": record.cpu_usage,
                "memory": record.memory_usage,
                "latency": record.latency_ms,
                "disk": record.disk_usage,
                "service_status": record.service_status
            })

    summary = summarize_anomalies(structured)
    recommendation = generate_recommandation(summary)

    return {
        "summary": summary,
        "recommendation": recommendation,
        "anomalies": structured
    }
