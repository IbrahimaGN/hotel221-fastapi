from sqlalchemy.orm import Session
from hotel221.models.client import Client
from hotel221.models.reservation import Reservation
from typing import Optional, List


class ClientRepository:
    """Accès base de données pour les clients via SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def trouver_tous(self, recherche: Optional[str] = None) -> List[Client]:
        query = self.db.query(Client)
        if recherche:
            terme = f"%{recherche}%"
            query = query.filter(
                Client.nom.ilike(terme)
                | Client.prenom.ilike(terme)
                | Client.email.ilike(terme)
            )
        return query.order_by(Client.nom).all()

    def trouver_par_id(self, client_id: int) -> Optional[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def trouver_par_email(self, email: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.email == email).first()

    def trouver_par_piece_identite(self, piece_identite: str) -> Optional[Client]:
        return self.db.query(Client).filter(Client.piece_identite == piece_identite).first()

    def creer(self, donnees: dict) -> Client:
        client = Client(**donnees)
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def mettre_a_jour(self, client: Client, donnees: dict) -> Client:
        for champ, valeur in donnees.items():
            if valeur is not None:
                setattr(client, champ, valeur)
        self.db.commit()
        self.db.refresh(client)
        return client

    def supprimer(self, client: Client) -> None:
        self.db.delete(client)
        self.db.commit()

    def a_des_reservations(self, client_id: int) -> bool:
        """Vérifie si le client a des réservations — bloque la suppression."""
        count = (
            self.db.query(Reservation)
            .filter(Reservation.client_id == client_id)
            .count()
        )
        return count > 0
