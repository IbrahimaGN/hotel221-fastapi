from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from hotel221.config.database import get_db
from hotel221.services.chambre_service import ChambreService
from hotel221.schemas.chambre import ChambreCreate, ChambreUpdate, ChambreResponse
from hotel221.utils.response import send_response

router = APIRouter(prefix="/api/chambres", tags=["Chambres"])


@router.get(
    "/",
    summary="Lister toutes les chambres",
    description="Retourne la liste des chambres. Filtres optionnels : type, statut.",
    responses={200: {"description": "Liste des chambres"}},
)
def lister_chambres(
    type: Optional[str] = None,
    statut: Optional[str] = None,
    db: Session = Depends(get_db),
):
    service = ChambreService(db)
    chambres = service.lister(type=type, statut=statut)
    data = [ChambreResponse.model_validate(c).model_dump() for c in chambres]
    return send_response("Chambres récupérées avec succès", data)


@router.get(
    "/{chambre_id}",
    summary="Récupérer une chambre par ID",
    responses={404: {"description": "Chambre introuvable"}},
)
def obtenir_chambre(chambre_id: int, db: Session = Depends(get_db)):
    service = ChambreService(db)
    chambre = service.obtenir(chambre_id)
    return send_response("Chambre récupérée avec succès", ChambreResponse.model_validate(chambre).model_dump())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Créer une chambre",
    description="Valide le numéro (unique), le type et le prix (> 0) avant création.",
    responses={
        201: {"description": "Chambre créée avec succès"},
        409: {"description": "Numéro de chambre déjà existant"},
    },
)
def creer_chambre(donnees: ChambreCreate, db: Session = Depends(get_db)):
    service = ChambreService(db)
    chambre = service.creer(donnees)
    return send_response("Chambre créée avec succès", ChambreResponse.model_validate(chambre).model_dump())


@router.put(
    "/{chambre_id}",
    summary="Modifier une chambre",
    responses={
        404: {"description": "Chambre introuvable"},
        409: {"description": "Numéro déjà utilisé"},
    },
)
def mettre_a_jour_chambre(chambre_id: int, donnees: ChambreUpdate, db: Session = Depends(get_db)):
    service = ChambreService(db)
    chambre = service.mettre_a_jour(chambre_id, donnees)
    return send_response("Chambre mise à jour avec succès", ChambreResponse.model_validate(chambre).model_dump())


@router.delete(
    "/{chambre_id}",
    summary="Supprimer une chambre",
    description="Interdit si la chambre a des réservations CONFIRMEE.",
    responses={
        404: {"description": "Chambre introuvable"},
        409: {"description": "Chambre avec réservations CONFIRMEE"},
    },
)
def supprimer_chambre(chambre_id: int, db: Session = Depends(get_db)):
    service = ChambreService(db)
    service.supprimer(chambre_id)
    return send_response("Chambre supprimée avec succès")
