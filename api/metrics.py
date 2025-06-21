from fastapi import APIRouter
from fastapi.responses import JSONResponse
from nodes.visualization import get_metric_timeseries

router = APIRouter()

@router.get("/metric/{metric_name}")
def fetch_metric(metric_name: str):
    """
    Récupère la série temporelle d'une métrique spécifique.
    Si latest_uploaded.json est introuvable, on prend data/rapport.json
    """
    try:
        return JSONResponse(content=get_metric_timeseries(metric_name, json_path="data/latest_uploaded.json"))
    except FileNotFoundError:
        print("Fichier latest_uploaded.json introuvable. Repli sur rapport.json.")
        return JSONResponse(content=get_metric_timeseries(metric_name, json_path="data/rapport.json"))
