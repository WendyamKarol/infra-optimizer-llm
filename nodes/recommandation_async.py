import os
import json
from typing import List, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_recommendations_async(anomaly_report: Dict) -> List[Dict]:
    reasons = anomaly_report.get("anomaly_reasons", [])
    if not reasons:
        return []

    prompt = (
        "Tu es un expert DevOps. Pour chaque anomalie listée ci-dessous, "
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
