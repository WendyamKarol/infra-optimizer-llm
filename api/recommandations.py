from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from nodes.recommandation_async import generate_recommendations_async

router = APIRouter()

# Schéma de données attendu en entrée
class AnomalyInput(BaseModel):
    timestamp: str
    anomaly_reasons: List[str]

@router.post("/")
async def get_recommendations(anomalies: List[AnomalyInput]):
    """
    Reçoit une liste d'anomalies (timestamp + raisons),
    et génère des recommandations structurées via LLM.
    """
    all_recos = []

    for anomaly in anomalies:
        report = {
            "timestamp": anomaly.timestamp,
            "anomaly_reasons": anomaly.anomaly_reasons
        }

        recos = await generate_recommendations_async(report)
        for reco in recos:
            reco["timestamp"] = anomaly.timestamp
            all_recos.append(reco)

    return {"recommendations": all_recos}
