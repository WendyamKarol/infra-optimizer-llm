from fastapi import APIRouter, UploadFile, File
from nodes.data_ingestion import ingest_data
from nodes.anomaly_detection import detect_anomalies_batch
import tempfile
import shutil

router = APIRouter()

@router.post("/")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """
    Analyse un fichier JSON de monitoring (format rapport.json),
    détecte les anomalies et retourne les résultats.
    """
    # Sauvegarde temporaire du fichier uploadé
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Ingestion + détection
    data = ingest_data(tmp_path)
    results = detect_anomalies_batch(data)

    # Formate les résultats pour l'API
    response = []
    for r in results:
        response.append({
            "timestamp": r["timestamp"],
            "is_anomaly": r["is_anomaly"],
            "anomaly_reasons": r["anomaly_reasons"]
        })

    return {"anomalies": response}
