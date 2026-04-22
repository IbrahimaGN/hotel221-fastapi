from sqlalchemy.orm import Session
from hotel221.repositories.client_repo import ClientRepository
from hotel221.schemas.client import ClientCreate, ClientUpdate
from hotel221.models.client import Client
from hotel221.utils.errors import not_found, conflict
from typing import Optional, List


class ClientService:
    """Logique métier pour les clients."""

    def __init__(self, db: Session):
        self.repo = ClientRepository(db)

    def lister(self, recherche: Optional[str] = None) -> List[Client]:
        return self.repo.trouver_tous(recherche=recherche)

    def obtenir(self, client_id: int) -> Client:
        client = self.repo.trouver_par_id(client_id)
        if not client:
            not_found("Client", client_id)
        return client

    def creer(self, donnees: ClientCreate) -> Client:
        # Vérifier l'unicité de l'email
        if self.repo.trouver_par_email(donnees.email):
            conflict(f"Un client avec l'email \"{donnees.email}\" existe déjà")

        # Vérifier l'unicité de la pièce d'identité
        if self.repo.trouver_par_piece_identite(donnees.piece_identite):
            conflict(f"Un client avec la pièce d'identité \"{donnees.piece_identite}\" existe déjà")

        return self.repo.creer(donnees.model_dump())

    def mettre_a_jour(self, client_id: int, donnees: ClientUpdate) -> Client:
        client = self.obtenir(client_id)

        # Vérifier unicité email si modifié
        if donnees.email and donnees.email != client.email:
            if self.repo.trouver_par_email(donnees.email):
                conflict(f"Un client avec l'email \"{donnees.email}\" existe déjà")

        # Vérifier unicité pièce d'identité si modifiée
        if donnees.piece_identite and donnees.piece_identite != client.piece_identite:
            if self.repo.trouver_par_piece_identite(donnees.piece_identite):
                conflict(f"Un client avec la pièce d'identité \"{donnees.piece_identite}\" existe déjà")

        return self.repo.mettre_a_jour(client, donnees.model_dump(exclude_none=True))

    def supprimer(self, client_id: int) -> None:
        client = self.obtenir(client_id)

        # Interdire suppression si le client a des réservations
        if self.repo.a_des_reservations(client_id):
            conflict("Impossible de supprimer : le client a des réservations associées")

        self.repo.supprimer(client)
