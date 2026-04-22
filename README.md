# 🏨 HOTEL 221 — API FastAPI + Docker

API REST pour la gestion des chambres, clients, réservations et services de l'hôtel HOTEL 221.


---

## 🐳 Démarrage avec Docker (recommandé)

### Prérequis
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé

### Lancer le projet en une commande

```bash
# 1. Copier le fichier d'environnement Docker
cp .env.docker .env

# 2. Construire et lancer les conteneurs (API + PostgreSQL)
docker-compose up --build
```

Docker va automatiquement :
- Créer un conteneur PostgreSQL avec la base hotel221
- Construire et lancer le conteneur FastAPI
- Attendre que PostgreSQL soit prêt avant de démarrer l'API
- Créer toutes les tables au démarrage

### Accès

| URL | Description |
|-----|-------------|
| http://localhost:8000/api-docs | Swagger UI interactif |
| http://localhost:8000/redoc   | ReDoc (lecture seule)  |
| http://localhost:8000/health  | Health check           |

---

## 🛠️ Commandes Docker utiles

```bash
# Lancer en arrière-plan
docker-compose up -d --build

# Voir les logs
docker-compose logs -f
docker-compose logs -f api
docker-compose logs -f db

# Arrêter
docker-compose down

# Arrêter ET supprimer les données PostgreSQL
docker-compose down -v

# Shell dans le conteneur API
docker exec -it hotel221_api sh

# psql dans PostgreSQL
docker exec -it hotel221_db psql -U postgres -d hotel221
```

---

## 🚀 Démarrage sans Docker

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
