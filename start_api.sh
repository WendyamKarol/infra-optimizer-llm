#!/bin/bash

PORT=8000
MODULE="main_api:app"

# Vérifie si un processus utilise déjà le port
PID=$(lsof -t -i:$PORT)

if [ -n "$PID" ]; then
  echo "Port $PORT déjà utilisé par le PID $PID. On le termine..."
  kill -9 $PID
  sleep 1
fi

# Lance Uvicorn sur le bon port
echo "🚀 Démarrage de l’API sur http://127.0.0.1:$PORT"
uvicorn $MODULE --reload --port $PORT
