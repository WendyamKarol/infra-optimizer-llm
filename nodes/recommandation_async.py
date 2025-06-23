import os
import json
from typing import List, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Chargement des variables d'environnement (clé API notamment)
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialisation du client OpenAI de manière asynchrone avec la clé API
async def generate_recommendations_async(anomaly_report: Dict) -> List[Dict]:
    """
    Fonction asynchrone qui génère des recommandations à partir d'un rapport d'anomalies.

    Entrée :
    - anomaly_report : dictionnaire contenant une clé 'anomaly_reasons' (liste de raisons).

    Sortie :
    - Liste de recommandations formatées sous forme de dictionnaires JSON
      avec les champs : type, explanation, suggestion.
    """
    reasons = anomaly_report.get("anomaly_reasons", [])
    if not reasons:
        return []

    prompt = (
        "Tu es un expert en optimisation d'infrastucture. Pour chaque anomalie listée ci-dessous, "
        "génère une recommandation structurée au format JSON (liste de dictionnaires) avec les champs : "
        "type, explanation, suggestion. Réponds uniquement avec une liste JSON.\n\n"
        f"Anomalies détectées : {reasons}"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        start, end = content.index("["), content.rindex("]") + 1
        json_part = content[start:end]
        return json.loads(json_part)
    except Exception as e:
        print(f"❌ Erreur LLM : {e}")
        return []
