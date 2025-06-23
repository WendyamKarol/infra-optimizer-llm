from nodes.data_ingestion import ingest_data
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.recommandation_RealTime import generate_recommendations

def main():
    # Étape 1 : Chargement des données depuis un fichier JSON
    print("📥 Étape 1 : Ingestion des données...")
    data_list = ingest_data("data/rapport.json")
    print(f"✅ {len(data_list)} entrées ingérées.\n")

    # Étape 2 : Détection des anomalies via règles métier
    print("🔍 Étape 2 : Détection des anomalies...")
    results = detect_anomalies_batch(data_list)

    # On filtre uniquement les anomalies
    anomalies_only = [res for res in results if res["is_anomaly"]]

    print(f"\n📊 Anomalies détectées : {len(anomalies_only)}\n")

    # Pour chaque anomalie, affichage et génération de recommandations
    for result in anomalies_only:
        timestamp = result["timestamp"]
        reasons = ", ".join(result["anomaly_reasons"])

        print(f"⏱️ {timestamp} | ❌ ANOMALIE | Raisons : {reasons}")

        # Étape 3 : Génération des recommandations via un LLM
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
