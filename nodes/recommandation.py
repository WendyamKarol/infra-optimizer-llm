
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_anomalies(anomalies: list[dict]) -> str:
    
    if not anomalies:
        return "Aucune anomalie détectée."

    types_counter = {}
    for a in anomalies:
        for t in a.get("type", []):
            types_counter[t] = types_counter.get(t, 0) + 1

    lines = [f"- {k.upper()}: {v} occurrence(s)" for k, v in types_counter.items()]
    summary = "Résumé des anomalies détectées :\n" + "\n".join(lines)
    return summary

def generate_recommandation(anomaly_summary: str) -> str:
    prompt = f"""Tu es un ingénieur DevOps expert en performance applicative.

Voici un résumé d’anomalies détectées dans une infrastructure :

{anomaly_summary}

Donne-moi des recommandations techniques sous forme de liste, claires et concises, pour optimiser les performances de l'infrastructure. 
Retourne uniquement une liste (sans introduction ni conclusion), chaque recommandation sur une ligne."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert en infrastructure et optimisation système."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=300
    )

    text = response.choices[0].message.content.strip()
    lines = [line.strip("-• \n") for line in text.split("\n") if line.strip()]
    return lines