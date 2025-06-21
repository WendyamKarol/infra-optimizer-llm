from nodes.data_ingestion import ingest_data
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.recommandation import generate_recommendations

def main():
    print("📥 Étape 1 : Ingestion des données...")
    data_list = ingest_data("data/rapport.json")
    print(f"✅ {len(data_list)} entrées ingérées.\n")

    print("🔍 Étape 2 : Détection des anomalies...")
    results = detect_anomalies_batch(data_list)

    # On filtre uniquement les anomalies
    anomalies_only = [res for res in results if res["is_anomaly"]]

    print(f"\n📊 Anomalies détectées : {len(anomalies_only)}\n")
    for result in anomalies_only:
        timestamp = result["timestamp"]
        reasons = ", ".join(result["anomaly_reasons"])

        print(f"⏱️ {timestamp} | ❌ ANOMALIE | Raisons : {reasons}")

        # 🧠 Recommandations via LLM
        print("\n📌 Recommandations :")
        recos = generate_recommendations(result)

        if recos:
            for reco in recos:
                print(f"➡️ {reco['type']}")
                print(f"   Explication : {reco['explanation']}")
                print(f"   Suggestion  : {reco['suggestion']}\n")
        else:
            print("⚠️ Aucune recommandation générée.\n")

if __name__ == "__main__":
    main()
