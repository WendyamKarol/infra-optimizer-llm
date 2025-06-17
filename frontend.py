import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.title("🔍 Analyse d'infrastructure & recommandations IA")

uploaded_file = st.file_uploader("📁 Upload un fichier JSON de monitoring", type="json")

if uploaded_file:
    data = json.load(uploaded_file)

    filter_option = st.selectbox(
        "🎯 Type d'anomalie à filtrer",
        options=["Toutes", "cpu", "memory", "latency", "disk", "service"]
    )

    if st.button("🚀 Analyser les anomalies"):
        params = {}
        if filter_option.lower() != "toutes":
            params["filter"] = filter_option.lower()

        response = requests.post(f"{API_URL}/analyze", params=params, json=data)

        if response.status_code == 200:
            result = response.json()
            st.subheader(f"📊 {result['count']} anomalies détectées")

            for a in result["anomalies"]:
                st.json(a)

            if st.button("💡 Générer des recommandations IA"):
                reco_resp = requests.post(f"{API_URL}/recommendations", json=result["anomalies"])

                if reco_resp.status_code == 200:
                    reco = reco_resp.json()
                    st.subheader("🧠 Résumé des anomalies")
                    st.text(reco["summary"])
                    st.subheader("✅ Recommandations")
                    for r in reco["recommandation"].split("\n"):
                        if r.strip():
                            st.markdown(f"- {r}")
                else:
                    st.error("Erreur lors de la génération des recommandations.")
        else:
            st.error(f"Erreur d’analyse ({response.status_code})")
