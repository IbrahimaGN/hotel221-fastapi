from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from hotel221.config.database import engine, Base
from hotel221.config.settings import settings

# Import des modèles pour que SQLAlchemy crée les tables
import hotel221.models.chambre      # noqa
import hotel221.models.client       # noqa
import hotel221.models.reservation  # noqa
import hotel221.models.service      # noqa

# Import des routers
from hotel221.routers.chambre_router     import router as chambre_router
from hotel221.routers.client_router      import router as client_router
from hotel221.routers.reservation_router import router as reservation_router
from hotel221.routers.service_router     import router as service_router

# ── Création des tables au démarrage ──────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Application FastAPI ───────────────────────────────────────────────────────
app = FastAPI(
    title="🏨 HOTEL 221 — API Hôtelière",
    description=(
        "API REST pour la gestion des chambres, clients, réservations et services "
        "de l'hôtel HOTEL 221.\n\n"
        "**Livrable 1** — Architecture en couches : routers → services → repositories → SQLAlchemy → PostgreSQL"
    ),
    version="1.0.0",
    contact={"name": "HOTEL 221", "email": "hotel221@tech221.sn"},
    docs_url="/api-docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── Middleware CORS ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Gestion globale des erreurs de validation Pydantic ────────────────────────
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        f"{' → '.join(str(loc) for loc in err['loc'])}: {err['msg']}"
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Données invalides",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details,
        },
    )

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(chambre_router)
app.include_router(client_router)
app.include_router(reservation_router)
app.include_router(service_router)


#── Route racine ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Racine"], summary="Page d'accueil de l'API")
def racine():
    return {
        "success": True,
        "message": "🏨 HOTEL 221 API — Opérationnelle",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "documentation": "/api-docs",
        "redoc": "/redoc",
    }

@app.get("/health", tags=["Racine"], summary="Health check")
def health():
    return {
        "success": True,
        "message": "API en bonne santé",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "env": settings.ENV,
    }

# ── Démarrage ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("\n╔══════════════════════════════════════════════════╗")
    print("║       🏨 HOTEL 221 — API Hôtelière v1.0.0        ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  ✅ Serveur démarré sur le port : {settings.PORT}            ║")
    print(f"║  🌐 URL     : http://localhost:{settings.PORT}                ║")
    print(f"║  📚 Docs    : http://localhost:{settings.PORT}/api-docs       ║")
    print(f"║  📖 ReDoc   : http://localhost:{settings.PORT}/redoc          ║")
    print(f"║  ❤️  Health  : http://localhost:{settings.PORT}/health         ║")
    print("╚══════════════════════════════════════════════════╝\n")
    uvicorn.run("main:app", host="127.0.0.1", port=settings.PORT, reload=True)
