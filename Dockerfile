# ── Étape 1 : image de base légère Python ────────────────────────────────────
FROM python:3.11-slim

# Empêche Python de créer des fichiers .pyc et active les logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dossier de travail dans le conteneur
WORKDIR /app

# ── Étape 2 : installer les dépendances ──────────────────────────────────────
# On copie d'abord uniquement requirements.txt pour profiter du cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Étape 3 : copier le code source ──────────────────────────────────────────
COPY . .

# ── Étape 4 : exposer le port de l'API ───────────────────────────────────────
EXPOSE 8000

# ── Étape 5 : script de démarrage ────────────────────────────────────────────
# Le script attend que PostgreSQL soit prêt avant de lancer l'API
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
