import json
import pandas as pd
from typing import List, Dict
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.data_ingestion import ingest_data

def load_metrics_with_anomalies(json_path: str = "data/latest_uploaded.json") -> pd.DataFrame:
    """
    Charge les données JSON, détecte les anomalies et retourne un DataFrame enrichi.
    """
    data = ingest_data(json_path)
    results = detect_anomalies_batch(data)

    rows = []
    for r in results:
        # Récupération des données techniques
        metrics = r["metrics"].model_dump()  # si Pydantic, sinon vars(...)
        metrics["timestamp"] = r["timestamp"]
        metrics["is_anomaly"] = r["is_anomaly"]
        metrics["anomaly_reasons"] = r["anomaly_reasons"]
        rows.append(metrics)

    df = pd.DataFrame(rows)

    # ✅ Supprimer les doublons sur colonnes comparables uniquement
    df.drop_duplicates(
        subset=["timestamp", "cpu_usage", "latency_ms", "error_rate", "temperature_celsius"],
        inplace=True
    )

    return df

def get_metric_timeseries(metric_name: str, json_path: str = "data/latest_uploaded.json") -> Dict:
    """
    Récupère les valeurs d'une métrique sous forme exploitable pour affichage (React, Plotly, etc.)
    """
    df = load_metrics_with_anomalies(json_path)

    if metric_name not in df.columns:
        return {"error": f"Métrique '{metric_name}' non trouvée."}

    data = []
    for _, row in df.iterrows():
        data.append({
            "timestamp": row["timestamp"],
            "value": row[metric_name],
            "is_anomaly": row["is_anomaly"],
            "reasons": row["anomaly_reasons"],
        })

    return {
        "metric": metric_name,
        "data": data
    }

# 🎯 Test local dans ce fichier
if __name__ == "__main__":
    metric = "cpu_usage"  # 🔁 Change pour tester d’autres : latency_ms, error_rate, etc.
    print(f"\n📊 Aperçu de la métrique : {metric}")

    # Vérifie s'il y a des doublons de timestamps
    df = load_metrics_with_anomalies()
    print("\n⏱️ Fréquence des timestamps (doublons éventuels) :")
    print(df["timestamp"].value_counts().head())

    # Affichage formaté des 10 premiers points
    result = get_metric_timeseries(metric)
    print("\n📈 Échantillon des données :")
    for row in result["data"][:10]:
        print(f"{row['timestamp']} | {row['value']} | Anomalie: {row['is_anomaly']} | Raisons: {row['reasons']}")
