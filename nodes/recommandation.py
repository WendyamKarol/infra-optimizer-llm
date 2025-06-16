import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Charger la clé API OpenAI depuis le fichier .env
load_dotenv()

# Initialisation du modèle LLM
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0
)

def generate_recommendations(anomalies: List[str]) -> str:
 
    prompt = f"""
    Tu es un expert en architecture technique et optimisation de performance.

    Voici une liste d’anomalies détectées :
    {anomalies}

    Pour chaque anomalie, fournis une recommandation technique précise.
    Formate la réponse comme un JSON de ce type :

    {{
        "anomalies": [
            {{
                "description": "CPU usage is too high.",
                "recommendation": "Répartir la charge sur plusieurs machines ou augmenter les ressources CPU."
            }}
        ]
    }}
    """

    messages = [HumanMessage(content=prompt)]
    result = llm.invoke(messages)
    return result.content

# Test local direct
if __name__ == "__main__":
    test_anomalies = [
        "CPU usage is too high.",
        "Latency is too high.",
        "API Gateway is degraded."
    ]
    print("📋 Anomalies simulées :", test_anomalies)
    print("\n🧠 Appel au LLM pour recommandations...")
    recommendations = generate_recommendations(test_anomalies)
    print("\n✅ Rapport généré :\n")
    print(recommendations)
