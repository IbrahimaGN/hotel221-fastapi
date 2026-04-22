#!/bin/sh
set -e

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       🏨 HOTEL 221 — Démarrage conteneur         ║"
echo "╚══════════════════════════════════════════════════╝"

# ── Attendre que PostgreSQL soit disponible ───────────────────────────────────
echo "⏳ Attente de PostgreSQL..."

MAX_RETRIES=30
COUNT=0

until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(os.environ.get('DATABASE_URL', ''))
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
  COUNT=$((COUNT + 1))
  if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
    echo "❌ PostgreSQL non disponible après $MAX_RETRIES tentatives. Arrêt."
    exit 1
  fi
  echo "   → Tentative $COUNT/$MAX_RETRIES — nouvelle tentative dans 2s..."
  sleep 2
done

echo "✅ PostgreSQL prêt !"
echo ""

# ── Lancer le serveur Uvicorn ─────────────────────────────────────────────────
echo "🚀 Lancement de l'API..."
exec uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
