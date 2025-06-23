from fastapi import APIRouter, UploadFile, File
from typing import Dict
from nodes.data_ingestion import ingest_data
from nodes.anomaly_detection import detect_anomalies_batch
from nodes.recommandation_async import generate_recommendations_async

import os
import json
import tempfile
import shutil
import asyncio

router = APIRouter()

@router.post("/chain")
async def analyze_and_recommend(file: UploadFile = File(...)) -> Dict:
    """
    Reçoit un fichier JSON, détecte les anomalies, filtre celles pertinentes,
    génère les recommandations LLM de manière parallèle (async),
    et sauvegarde les résultats dans data/recommendations.json.
    """
    # Etape 1 : Sauvegarde temporaire du fichier uploadé
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp:
        shutil.copyfileobj(file.file, temp)
        temp_path = temp.name

    # Etape 1 bis : Sauvegarde standard pour visualisation
    shutil.copy(temp_path, "data/latest_uploaded.json")

    # Etape 2 : Ingestion
    data = ingest_data(temp_path)

    # Etape 3 : Détection des anomalies
    results = detect_anomalies_batch(data)

    # Etape 4 : Filtrage uniquement des anomalies
    filtered = [
        {
            "timestamp": r["timestamp"],
            "anomaly_reasons": r["anomaly_reasons"]
        }
        for r in results if r["is_anomaly"]
    ]

    # Etape 5 : Génération en parallèle des recommandations
    tasks = [generate_recommendations_async(anomaly) for anomaly in filtered]
    results = await asyncio.gather(*tasks)

    # Etape 6 : Fusion timestamp + recommandations 
    all_recos = []
    for anomaly, recos in zip(filtered, results):
        for reco in recos:
            reco["timestamp"] = anomaly["timestamp"]
            all_recos.append(reco)

    # Etape 7 : Sauvegarde locale JSON
    output_path = os.path.join("data", "recommendations.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"recommendations": all_recos}, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement JSON : {e}")

    return {"recommendations": all_recos}
