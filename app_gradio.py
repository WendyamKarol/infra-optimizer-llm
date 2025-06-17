import gradio as gr
import requests
import json

FASTAPI_URL = "http://127.0.0.1:8000"

def analyze_and_recommend(file):
    try:
        with open(file.name, "r") as f:
            records = json.load(f)  # ✅ CORRECT : lire un fichier directement
    except Exception as e:
        return f"Erreur lors du chargement JSON : {e}", ""

    # Analyse via FastAPI
    response = requests.post(f"{FASTAPI_URL}/analyze", json=records)
    if response.status_code != 200:
        return f"Erreur analyse: {response.text}", ""

    anomalies = response.json().get("anomalies", [])

    # Recommandation via FastAPI
    response = requests.post(f"{FASTAPI_URL}/recommendations", json=anomalies)
    if response.status_code != 200:
        return f"Erreur recommandations: {response.text}", ""

    rec = response.json()
    return rec["summary"], rec["recommandation"]


iface = gr.Interface(
    fn=analyze_and_recommend,
    inputs=gr.File(label="Upload JSON de monitoring"),
    outputs=[
        gr.Textbox(label="Résumé des anomalies"),
        gr.Textbox(label="Recommandations")
    ],
    title="Analyse et Optimisation d'Infrastructure"
)

iface.launch()
