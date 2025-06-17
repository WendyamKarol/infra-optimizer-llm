from nodes.data_ingestion import ingest_data
from nodes.anomaly_detection import detect_anomalies_batch

def main():
    print("🚀 Test direct : analyse horaire des anomalies")

    # Étape 1 : ingestion
    data = ingest_data("rapport.json")
    print(f"📥 {len(data)} enregistrements chargés.")

    # Étape 2 : détection
    results = detect_anomalies_batch(data)

    # Étape 3 : filtrer les anomalies détectées
    anomalies = [d for d, is_anomaly in results if is_anomaly]

    # Étape 4 : affichage
    print("\n📊 Résultat de l’analyse temporelle :")
    for anomaly in anomalies:
        print(f"⛔ Anomalie détectée à {anomaly.timestamp} | CPU={anomaly.cpu_usage}%, MEM={anomaly.memory_usage}%, STATUS={anomaly.service_status}")

    if not anomalies:
        print("✅ Aucune anomalie détectée.")

if __name__ == "__main__":
    main()
