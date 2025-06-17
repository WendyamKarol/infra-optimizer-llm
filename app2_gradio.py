import gradio as gr
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

FASTAPI_URL = "http://127.0.0.1:8000"

# Fonction principale d'analyse

def analyze_and_recommend(file):
    try:
        with open(file.name, "r") as f:
            records = json.load(f)
    except Exception as e:
        return f"Erreur lors du chargement JSON : {e}", "", None, None, None

    # Appel FastAPI /analyze
    response = requests.post(f"{FASTAPI_URL}/analyze", json=records)
    if response.status_code != 200:
        return f"Erreur analyse: {response.text}", "", None, None, None

    anomalies = response.json().get("anomalies", [])

    # Appel FastAPI /recommendations
    response = requests.post(f"{FASTAPI_URL}/recommendations", json=anomalies)
    if response.status_code != 200:
        return f"Erreur recommandations: {response.text}", "", None, None, None

    rec = response.json()
    summary = rec["summary"]
    tips = rec["recommandation"]

    # Génération des graphiques
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    # Ligne - évolution temporelle
    fig1, ax1 = plt.subplots()
    df.plot(x='timestamp', y=['cpu_usage', 'memory_usage', 'latency_ms', 'disk_usage'], ax=ax1)
    ax1.set_title("Évolution des métriques principales")
    ax1.set_ylabel("% / ms")
    ax1.grid()

    # Histogramme anomalies par type
    type_counts = {}
    for a in anomalies:
        for t in a.get("type", []):
            type_counts[t] = type_counts.get(t, 0) + 1
    fig2, ax2 = plt.subplots()
    if type_counts:
        ax2.bar(type_counts.keys(), type_counts.values())
        ax2.set_title("Répartition des types d'anomalies")
        ax2.set_ylabel("Occurrences")

    # Pie chart services
    service_statuses = []
    for r in records:
        if "service_status" in r:
            service_statuses.extend(list(r["service_status"].values()))
    service_counts = pd.Series(service_statuses).value_counts()
    fig3, ax3 = plt.subplots()
    if not service_counts.empty:
        ax3.pie(service_counts, labels=service_counts.index, autopct='%1.1f%%')
        ax3.set_title("Statut des services")

    return summary, tips, fig1, fig2, fig3

with gr.Blocks(css=".gr-box {width: 100% !important; max-width: none !important;}") as iface:
    gr.Markdown("## Analyse et Optimisation d'Infrastructure")
    with gr.Row():
        file_input = gr.File(label="Upload JSON de monitoring")
    with gr.Row():
        summary_output = gr.Textbox(label="Résumé des anomalies", lines=6)
        recommendation_output = gr.Textbox(label="Recommandations", lines=6)
    with gr.Row():
        graph1 = gr.Plot(label="Graphique: Évolution des métriques")
    with gr.Row():
        graph2 = gr.Plot(label="Graphique: Anomalies par type")
        graph3 = gr.Plot(label="Graphique: Statuts des services")

    file_input.change(fn=analyze_and_recommend, inputs=file_input, outputs=[summary_output, recommendation_output, graph1, graph2, graph3])

iface.launch()
