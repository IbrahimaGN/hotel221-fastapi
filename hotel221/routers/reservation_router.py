from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from hotel221.config.database import get_db
from hotel221.services.reservation_service import ReservationService
from hotel221.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationResponse
from hotel221.utils.response import send_response

router = APIRouter(prefix="/api/reservations", tags=["Réservations"])


@router.get(
    "/",
    summary="Lister toutes les réservations",
    description="Filtres optionnels : statut, client_id, chambre_id.",
)
def lister_reservations(
    statut: Optional[str] = None,
    client_id: Optional[int] = None,
    chambre_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    service = ReservationService(db)
    reservations = service.lister(statut=statut, client_id=client_id, chambre_id=chambre_id)
    data = [ReservationResponse.model_validate(r).model_dump() for r in reservations]
    return send_response("Réservations récupérées avec succès", data)


@router.get(
    "/{reservation_id}",
    summary="Récupérer une réservation par ID",
    description="Retourne la réservation avec ses détails : client, chambre et services.",
    responses={404: {"description": "Réservation introuvable"}},
)
def obtenir_reservation(reservation_id: int, db: Session = Depends(get_db)):
    service = ReservationService(db)
    reservation = service.obtenir(reservation_id)
    return send_response(
        "Réservation récupérée avec succès",
        ReservationResponse.model_validate(reservation).model_dump(),
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Créer une réservation",
    description=(
        "Vérifie l'existence du client et de la chambre. "
        "Valide dateArrivee >= aujourd'hui et dateDepart > dateArrivee. "
        "Détecte les chevauchements CONFIRMEE. "
        "Calcule le montant = nuits × prixParNuit. "
        "Crée avec statut CONFIRMEE automatiquement."
    ),
    responses={
        201: {"description": "Réservation créée avec montant calculé"},
        400: {"description": "Dates invalides"},
        404: {"description": "Client ou chambre introuvable"},
        409: {"description": "Chevauchement de réservation détecté"},
    },
)
def creer_reservation(donnees: ReservationCreate, db: Session = Depends(get_db)):
    service = ReservationService(db)
    reservation = service.creer(donnees)
    return send_response(
        "Réservation créée avec succès",
        ReservationResponse.model_validate(reservation).model_dump(),
    )


@router.put(
    "/{reservation_id}",
    summary="Modifier le statut d'une réservation",
    responses={404: {"description": "Réservation introuvable"}},
)
def mettre_a_jour_reservation(
    reservation_id: int, donnees: ReservationUpdate, db: Session = Depends(get_db)
):
    service = ReservationService(db)
    reservation = service.mettre_a_jour(reservation_id, donnees)
    return send_response(
        "Réservation mise à jour avec succès",
        ReservationResponse.model_validate(reservation).model_dump(),
    )


@router.delete(
    "/{reservation_id}",
    summary="Supprimer une réservation",
    description="Interdit si des services sont liés à cette réservation.",
    responses={
        404: {"description": "Réservation introuvable"},
        409: {"description": "Réservation avec services liés"},
    },
)
def supprimer_reservation(reservation_id: int, db: Session = Depends(get_db)):
    service = ReservationService(db)
    service.supprimer(reservation_id)
    return send_response("Réservation supprimée avec succès")
