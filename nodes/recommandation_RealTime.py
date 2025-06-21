import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_recommendations(anomaly_report: Dict) -> List[Dict]:
    reasons = anomaly_report.get("anomaly_reasons", [])
    if not reasons:
        return []

    prompt = (
        "Tu es un expert DevOps specialisé en optimisation d'infrastructure. Pour chaque anomalie technique listée ci-dessous, "
        "génère une recommandation structurée au format JSON avec les champs : type, explanation, suggestion.\n\n"
        f"Anomalies détectées : {reasons}\n\n"
        "Exemple de sortie attendue :\n"
        "[{\"type\": \"High CPU usage\", \"explanation\": \"...\", \"suggestion\": \"...\"}]"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    # Affichage de la réponse brute du LLM
    print("\n📝 Contenu brut renvoyé par GPT :")
    print(content)

    try:
        # Nettoyage : suppression des balises ```json ou ```
        content_cleaned = content.replace("```json", "").replace("```", "").strip()

        # Détection du premier crochet ouvrant
        start_idx = content_cleaned.index("[")
        end_idx = content_cleaned.rindex("]") + 1
        json_part = content_cleaned[start_idx:end_idx]
        return json.loads(json_part)
    except Exception as e:
        print(f"\n❌ Échec du parsing JSON même après nettoyage : {e}")
        return []

"""
# Test local
if __name__ == "__main__":
    test_anomaly_report = {
        "timestamp": "2023-10-01T12:00:00Z",
        "anomaly_reasons": [
            "High CPU usage",
            "High latency",
            "API Gateway degraded"
        ]
    }

    print(f"📥 Test de génération de recommandations pour anomalies : {test_anomaly_report['anomaly_reasons']}\n")
    recos = generate_recommendations(test_anomaly_report)

    if recos:
        print("📌 Recommandations générées :\n")
        for reco in recos:
            print(f"➡️ {reco['type']}:")
            print(f"   Explication : {reco['explanation']}")
            print(f"   Suggestion  : {reco['suggestion']}\n")
    else:
        print("❌ Aucune recommandation générée.")"""