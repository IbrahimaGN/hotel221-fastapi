from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from hotel221.config.database import get_db
from hotel221.services.service_service import ServiceService
from hotel221.schemas.service import ServiceCreate, ServiceResponse
from hotel221.utils.response import send_response

router = APIRouter(prefix="/api/services", tags=["Services"])


@router.get(
    "/",
    summary="Lister tous les services",
    description="Retourne tous les services. Filtre optionnel par reservation_id.",
)
def lister_services(reservation_id: Optional[int] = None, db: Session = Depends(get_db)):
    service = ServiceService(db)
    services = service.lister(reservation_id=reservation_id)
    data = [ServiceResponse.model_validate(s).model_dump() for s in services]
    return send_response("Services récupérés avec succès", data)


@router.get(
    "/{service_id}",
    summary="Récupérer un service par ID",
    responses={404: {"description": "Service introuvable"}},
)
def obtenir_service(service_id: int, db: Session = Depends(get_db)):
    svc = ServiceService(db)
    service = svc.obtenir(service_id)
    return send_response("Service récupéré avec succès", ServiceResponse.model_validate(service).model_dump())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Ajouter un service à une réservation",
    description=(
        "Vérifie l'existence de la réservation. "
        "La réservation doit être CONFIRMEE. "
        "Valide le libellé (obligatoire) et le prix (>= 0)."
    ),
    responses={
        201: {"description": "Service ajouté avec succès"},
        400: {"description": "Réservation non CONFIRMEE ou données invalides"},
        404: {"description": "Réservation introuvable"},
    },
)
def creer_service(donnees: ServiceCreate, db: Session = Depends(get_db)):
    service = ServiceService(db)
    nouveau = service.creer(donnees)
    return send_response("Service ajouté avec succès", ServiceResponse.model_validate(nouveau).model_dump())


@router.delete(
    "/{service_id}",
    summary="Supprimer un service",
    responses={404: {"description": "Service introuvable"}},
)
def supprimer_service(service_id: int, db: Session = Depends(get_db)):
    service = ServiceService(db)
    service.supprimer(service_id)
    return send_response("Service supprimé avec succès")
