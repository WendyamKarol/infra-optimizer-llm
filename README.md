# 🚀 Infrastructure Optimizer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Development-orange)

**Infrastructure Optimizer** est une application modulaire qui **ingère des données de monitoring JSON**, détecte automatiquement des **anomalies d’infrastructure** (CPU, mémoire, état des services) et **génère des recommandations intelligentes** pour optimiser les performances.

Elle fournit une **interface graphique interactive** en React pour visualiser les anomalies, filtrer les résultats et accéder aux recommandations générées par un LLM.

---

## 🎯 Objectifs

✅ **Analyser dynamiquement** des fichiers JSON contenant des métriques d’infrastructure  
✅ **Détecter les anomalies clés** (pannes, surcharges, dérives de performance)  
✅ **Générer des recommandations structurées** via un LLM (GPT)  
✅ Fournir une **interface simple et interactive** pour visualiser les résultats  

---

## 🏗️ Architecture

L’application est composée de deux modules principaux :  

- **Backend (FastAPI)**  
  - `POST /analyze` → Détection d’anomalies (CPU, mémoire, état des services…)  
  - `POST /recommendations` → Génération de recommandations (type, explication, solution)  
  - Orchestration des modules : ingestion, détection et génération  

- **Frontend (React)**  
  - Upload dynamique de fichiers JSON  
  - Visualisation des anomalies sous forme de graphiques interactifs  
  - Filtrage et consultation des recommandations  

### 🖼️ Schéma d’architecture

![Architecture](docs/architecture.png)

*(Ajoute une image `docs/architecture.png` pour illustrer)*

---

## 🛠️ Stack technique

- **Backend** : Python, FastAPI, Pandas  
- **Frontend** : React, Recharts, Axios  
- **IA/LLM** : OpenAI GPT pour la génération de recommandations  
- **Format des données** : JSON  

---

## 📂 Structure du projet

