from sqlalchemy.orm import Session
from hotel221.models.chambre import Chambre, StatutChambre
from hotel221.models.reservation import Reservation, StatutReservation
from typing import Optional, List
from datetime import datetime


class ChambreRepository:
    """Accès base de données pour les chambres via SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def trouver_toutes(self, type: Optional[str] = None, statut: Optional[str] = None) -> List[Chambre]:
        query = self.db.query(Chambre)
        if type:
            query = query.filter(Chambre.type == type)
        if statut:
            query = query.filter(Chambre.statut == statut)
        return query.order_by(Chambre.numero).all()

    def trouver_par_id(self, chambre_id: int) -> Optional[Chambre]:
        return self.db.query(Chambre).filter(Chambre.id == chambre_id).first()

    def trouver_par_numero(self, numero: str) -> Optional[Chambre]:
        return self.db.query(Chambre).filter(Chambre.numero == numero).first()

    def creer(self, donnees: dict) -> Chambre:
        chambre = Chambre(**donnees)
        self.db.add(chambre)
        self.db.commit()
        self.db.refresh(chambre)
        return chambre

    def mettre_a_jour(self, chambre: Chambre, donnees: dict) -> Chambre:
        for champ, valeur in donnees.items():
            if valeur is not None:
                setattr(chambre, champ, valeur)
        self.db.commit()
        self.db.refresh(chambre)
        return chambre

    def supprimer(self, chambre: Chambre) -> None:
        self.db.delete(chambre)
        self.db.commit()

    def a_des_reservations_confirmees(self, chambre_id: int) -> bool:
        """Vérifie si la chambre a des réservations CONFIRMEE — bloque la suppression."""
        count = (
            self.db.query(Reservation)
            .filter(
                Reservation.chambre_id == chambre_id,
                Reservation.statut == StatutReservation.CONFIRMEE,
            )
            .count()
        )
        return count > 0

    def verifier_chevauchement(
        self,
        chambre_id: int,
        date_arrivee: datetime,
        date_depart: datetime,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """Détecte les chevauchements de réservations CONFIRMEE sur une chambre."""
        query = self.db.query(Reservation).filter(
            Reservation.chambre_id == chambre_id,
            Reservation.statut == StatutReservation.CONFIRMEE,
            Reservation.date_arrivee < date_depart,
            Reservation.date_depart > date_arrivee,
        )
        if exclude_id:
            query = query.filter(Reservation.id != exclude_id)
        return query.count() > 0
