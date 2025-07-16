# 🚀 Infrastructure Optimizer

**Infrastructure Optimizer** est une solution développée dans le cadre d’un POC pour une entreprise X, en réponse à une problématique concrète :  

> **Comment permettre à une PME française d’analyser automatiquement ses données de monitoring d’infrastructure (JSON), détecter des anomalies et générer des recommandations pertinentes grâce à un LLM ?**

Ce projet n’est donc pas une simple expérimentation personnelle, mais une **implémentation complète** (architecture + développement) pour répondre à un besoin réel.  

---

## 🎯 Contexte & Problématique

Une PME française souhaitait :  

- **Ingérer dynamiquement** des données de monitoring d’infrastructure au format JSON  
- **Détecter automatiquement** des anomalies (CPU, mémoire, état des services)  
- **Générer des recommandations claires et actionnables** grâce à un LLM (GPT-4o)  
- **Disposer d’une interface utilisateur interactive** pour visualiser les résultats  

---

## ✅ Ma réponse : conception & développement complet

Pour répondre à cette problématique, j’ai :  

- **Conçu une architecture modulaire multi-nœuds** : Ingestion ➝ Détection ➝ Recommandation ➝ Visualisation  
- **Choisi une stack technique moderne** :  
  - **FastAPI** pour le backend asynchrone et les endpoints REST  
  - **React + Recharts** pour une interface claire et interactive  
  - **GPT-4o** pour générer des recommandations intelligentes  
- **Développé l’application de bout en bout**, avec séparation claire des responsabilités et endpoints bien documentés  

---

## 🏗️ Architecture générale

- **Backend (FastAPI)**  
  - `POST /analyze` : détecte les anomalies dans les données JSON  
  - `POST /recommendations` : génère des recommandations structurées via GPT  
  - Asynchrone, robuste, découplé en modules testables  

- **Frontend (React)**  
  - Upload dynamique des fichiers JSON  
  - Visualisation des anomalies en graphes interactifs  
  - Consultation filtrée des recommandations  


## 🛠️ Stack technique & choix

- **Langage :** Python → flexibilité & écosystème IA riche  
- **Framework API :** FastAPI → asynchrone, léger, doc auto  
- **LLM :** GPT-4o → recommandations naturelles & adaptables  
- **Frontend :** React + Recharts → interface moderne & intuitive  

*(Les choix techniques sont justifiés dans [docs/CHOIX_TECHNIQUES.md](docs/CHOIX_TECHNIQUES.md))*  

---

## ▶️ Résultat

✅ Une solution modulaire et robuste répondant aux objectifs :  
- Détection automatique d’anomalies  
- Génération de recommandations claires  
- Interface simple pour l’utilisateur final  

---

## 📌 Roadmap

- ✅ Architecture modulaire  
- ✅ Détection d’anomalies basique  
- ✅ Recommandations via GPT  
- ⏳ Analyse prédictive avancée  
- ⏳ Dockerisation & déploiement cloud  

---

## 📜 Contexte

Projet réalisé dans le cadre d’un **POC technique** pour optimiser l’infrastructure d’une PME fictive.  

---

## 👤 Auteur

Karol NAZE  
🔗 [LinkedIn](https://www.linkedin.com/in/karol-naze/) 
