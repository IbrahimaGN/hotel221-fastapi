from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from hotel221.config.database import get_db
from hotel221.services.client_service import ClientService
from hotel221.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from hotel221.utils.response import send_response

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.get(
    "/",
    summary="Lister tous les clients",
    description="Retourne la liste des clients. Filtre optionnel par recherche texte (nom, prénom, email).",
)
def lister_clients(recherche: Optional[str] = None, db: Session = Depends(get_db)):
    service = ClientService(db)
    clients = service.lister(recherche=recherche)
    data = [ClientResponse.model_validate(c).model_dump() for c in clients]
    return send_response("Clients récupérés avec succès", data)


@router.get(
    "/{client_id}",
    summary="Récupérer un client par ID",
    responses={404: {"description": "Client introuvable"}},
)
def obtenir_client(client_id: int, db: Session = Depends(get_db)):
    service = ClientService(db)
    client = service.obtenir(client_id)
    return send_response("Client récupéré avec succès", ClientResponse.model_validate(client).model_dump())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Créer un client",
    description="Valide email (unique), pièce d'identité (unique), prénom et nom (min 2 car.).",
    responses={
        201: {"description": "Client créé avec succès"},
        409: {"description": "Email ou pièce d'identité déjà utilisé"},
    },
)
def creer_client(donnees: ClientCreate, db: Session = Depends(get_db)):
    service = ClientService(db)
    client = service.creer(donnees)
    return send_response("Client créé avec succès", ClientResponse.model_validate(client).model_dump())


@router.put(
    "/{client_id}",
    summary="Modifier un client",
    responses={
        404: {"description": "Client introuvable"},
        409: {"description": "Email ou pièce d'identité déjà utilisé"},
    },
)
def mettre_a_jour_client(client_id: int, donnees: ClientUpdate, db: Session = Depends(get_db)):
    service = ClientService(db)
    client = service.mettre_a_jour(client_id, donnees)
    return send_response("Client mis à jour avec succès", ClientResponse.model_validate(client).model_dump())


@router.delete(
    "/{client_id}",
    summary="Supprimer un client",
    description="Interdit si le client a des réservations.",
    responses={
        404: {"description": "Client introuvable"},
        409: {"description": "Client avec réservations"},
    },
)
def supprimer_client(client_id: int, db: Session = Depends(get_db)):
    service = ClientService(db)
    service.supprimer(client_id)
    return send_response("Client supprimé avec succès")
