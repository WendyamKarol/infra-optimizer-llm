import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

# -------- Chargement et transformation des données --------
def load_data(path: str) -> pd.DataFrame:
    with open(path) as f:
        raw = json.load(f)
    
    # Transformer en DataFrame
    df = pd.DataFrame(raw)

    # Conversion du timestamp en datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Tri temporel
    df = df.sort_values('timestamp')

    return df

# -------- Affichage Streamlit --------
st.set_page_config(page_title="Monitoring Infrastructure", layout="wide")
st.title("📊 Visualisation des métriques d'infrastructure")

# Charger les données
df = load_data("rapport.json")

# Sélection des métriques à afficher
metrics = ["cpu_usage", "memory_usage", "latency_ms", "disk_usage", "io_wait", "error_rate"]
selected_metrics = st.multiselect("Choisir les métriques à afficher :", metrics, default=["cpu_usage", "memory_usage", "latency_ms"])

# Tracer les courbes
if selected_metrics:
    fig, ax = plt.subplots(figsize=(12, 5))
    for metric in selected_metrics:
        ax.plot(df['timestamp'], df[metric], label=metric)

    ax.set_xlabel("Temps")
    ax.set_ylabel("Valeur")
    ax.set_title("Évolution des métriques")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Sélectionnez au moins une métrique pour afficher le graphique.")
