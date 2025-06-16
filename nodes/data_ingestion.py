from typing import List
import json
from pydantic import BaseModel
from pathlib import Path
#import logging

class MonitoringData(BaseModel):
    timestamp: str
    cpu_usage: float
    memory_usage: float
    latency_ms: float
    disk_usage: float
    network_in_kbps: float
    network_out_kbps: float
    io_wait: float
    thread_count: int
    active_connections: int
    error_rate: float
    uptime_seconds: int
    temperature_celsius: float
    power_consumption_watts: float
    service_status: dict

def ingest_data(path="rapport.json") -> List[MonitoringData]:
    file_path = Path(__file__).parent.parent / path

    if not file_path.exists():
        raise FileNotFoundError(f"❌Fichier introuvable à : {file_path.resolve()}")

    with open(file_path) as f:
        raw_data = json.load(f)

    if not isinstance(raw_data, list):
        raise ValueError("Le fichier JSON doit contenir une liste d'objets.")

    monitoring_objects = [MonitoringData(**entry) for entry in raw_data]
    return monitoring_objects

"""
# Test direct
if __name__ == "__main__":
    data_list = ingest_data()
    for i, data in enumerate(data_list, 1):
        print(f"Entrée {i} : {data.timestamp} | CPU : {data.cpu_usage}% | Service Status : {data.service_status}")
"""