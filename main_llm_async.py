import asyncio
from nodes.data_ingestion import ingest_data
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.recommandation_async import generate_recommendations_async
import json
from pathlib import Path

CRITICAL_ISSUES = {
    "High CPU usage",
    "High latency",
    "API Gateway degraded"
}

def is_critical(anomaly: dict) -> bool:
    return any(reason in CRITICAL_ISSUES for reason in anomaly["anomaly_reasons"])

async def main():
    print("📥 Ingestion des données...")
    data_list = ingest_data("data/rapport.json")
    print(f"✅ {len(data_list)} lignes chargées\n")

    print("🔍 Détection des anomalies...")
    results = detect_anomalies_batch(data_list)

    critical_anomalies = [r for r in results if r["is_anomaly"] and is_critical(r)]

    print(f"\n⚠️ Anomalies critiques détectées : {len(critical_anomalies)}\n")

    # Appels asynchrones au LLM pour chaque anomalie critique
    tasks = [generate_recommendations_async(r) for r in critical_anomalies]
    reco_list = await asyncio.gather(*tasks)

    # Affichage combiné
    for anomaly, recos in zip(critical_anomalies, reco_list):
        print(f"\n🕒 {anomaly['timestamp']} | Raisons : {', '.join(anomaly['anomaly_reasons'])}")
        for reco in recos:
            print(f"➡️ {reco['type']}")
            print(f"   Explication : {reco['explanation']}")
            print(f"   Suggestion  : {reco['suggestion']}")

# Construction de la liste de résultats à sauvegarder
    output = []
    for anomaly, recos in zip(critical_anomalies, reco_list):
        output.append({
            "timestamp": anomaly["timestamp"],
            "anomaly_reasons": anomaly["anomaly_reasons"],
            "recommendations": recos
        })

    # Sauvegarde dans un fichier JSON
    Path("data").mkdir(exist_ok=True)
    with open("data/recommandations.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n✅ Recommandations sauvegardées dans 'data/recommandations.json'")

if __name__ == "__main__":
    asyncio.run(main())
