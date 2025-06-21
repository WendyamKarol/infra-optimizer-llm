from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.recommandations import router as recommendations_router
from api.chain import router as chain_router
# Import du routeur depuis le dossier api
from api.analyze import router as analyze_router
from api.metrics import router as metrics_router

# Création de l'application FastAPI
app = FastAPI(
    title="Infrastructure Optimizer",
    description="API pour analyser des données techniques et détecter les anomalies.",
    version="1.0.0"
)

# Middleware CORS pour permettre l'accès depuis un frontend (React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion du routeur "analyze" dans l'application
app.include_router(analyze_router, prefix="/analyze", tags=["Analyse"])
app.include_router(recommendations_router, prefix="/recommendations", tags=["Recommandations"])
app.include_router(chain_router, prefix="/api/chain", tags=["Analyse + Recommandations"])
app.include_router(metrics_router, prefix="/api")

