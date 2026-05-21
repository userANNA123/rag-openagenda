# RAG OpenAgenda – Chatbot Intelligent pour Événements Culturels

## Description

Ce projet implémente un système RAG (Retrieval-Augmented Generation) permettant de recommander des événements culturels à partir des données OpenAgenda.

Le système utilise :
- FAISS pour la recherche vectorielle,
- LangChain pour orchestrer le pipeline RAG,
- Mistral AI pour générer des réponses naturelles,
- FastAPI pour exposer le système via une API REST.

---

## Architecture du projet

```text
rag-openagenda/
├── data/
├── evaluation/
├── faiss_index/
├── src/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Technologies utilisées

- Python 3.11
- LangChain
- FAISS
- HuggingFace Embeddings
- Mistral AI
- FastAPI
- Uvicorn
- Pytest

---

## Fonctionnement du système RAG

1. Collecte des événements OpenAgenda
2. Nettoyage et transformation des données
3. Génération des embeddings
4. Construction de l’index vectoriel FAISS
5. Recherche des événements pertinents
6. Génération de réponse avec Mistral

---

## Installation

### Cloner le projet

```bash
git clone https://github.com/userANNA123/rag-openagenda.git
cd rag-openagenda
```

### Créer l’environnement virtuel

```bash
python -m venv env
```

### Activer l’environnement

Windows :

```bash
env\Scripts\activate
```

Linux/Mac :

```bash
source env/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Variables d’environnement

Créer un fichier `.env` :

```env
MISTRAL_API_KEY=your_api_key
```

---

## Construction de la base vectorielle

```bash
python src/data_loader.py
python src/clean_data.py
python src/build_faiss_index.py
```

---

## Lancer le chatbot

```bash
python src/chatbot.py
```

---

## Lancer l’API FastAPI

```bash
uvicorn src.api:app --reload
```

Documentation Swagger :

```text
http://127.0.0.1:8000/docs
```

---

## Endpoints API

### POST /ask

Envoie une question au système RAG.

Exemple :

```json
{
  "question": "Quels événements sont disponibles à Paris ?"
}
```

---

### POST /rebuild

Reconstruit la base vectorielle FAISS.

---

## Tests

Lancer les tests :

```bash
python -m pytest
```

---

## Évaluation

Le projet contient un jeu de test annoté :

```text
evaluation/evaluation_dataset.json
```

Les réponses peuvent être évaluées avec :
- Exact Match
- Similarité sémantique
- Évaluation manuelle
- Ragas

---

## Docker

Construire l’image :

```bash
docker build -t rag-openagenda .
```

Lancer le conteneur :

```bash
docker run -p 8000:8000 rag-openagenda
```

---

## Perspectives d’amélioration

- Ajout de mémoire conversationnelle
- Filtrage avancé des événements
- Déploiement cloud
- Authentification API
- Évaluation automatique avec Ragas
- Interface web utilisateur

---

## Auteur

Anna Harba