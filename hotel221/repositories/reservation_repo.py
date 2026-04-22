from sqlalchemy.orm import Session, joinedload
from hotel221.models.reservation import Reservation, StatutReservation
from hotel221.models.service import Service
from typing import Optional, List


class ReservationRepository:
    """Accès base de données pour les réservations via SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def trouver_toutes(
        self,
        statut: Optional[str] = None,
        client_id: Optional[int] = None,
        chambre_id: Optional[int] = None,
    ) -> List[Reservation]:
        query = self.db.query(Reservation).options(
            joinedload(Reservation.client),
            joinedload(Reservation.chambre),
        )
        if statut:
            query = query.filter(Reservation.statut == statut)
        if client_id:
            query = query.filter(Reservation.client_id == client_id)
        if chambre_id:
            query = query.filter(Reservation.chambre_id == chambre_id)
        return query.order_by(Reservation.date_arrivee.desc()).all()

    def trouver_par_id(self, reservation_id: int) -> Optional[Reservation]:
        return (
            self.db.query(Reservation)
            .options(
                joinedload(Reservation.client),
                joinedload(Reservation.chambre),
                joinedload(Reservation.services),
            )
            .filter(Reservation.id == reservation_id)
            .first()
        )

    def creer(self, donnees: dict) -> Reservation:
        reservation = Reservation(**donnees)
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def mettre_a_jour(self, reservation: Reservation, donnees: dict) -> Reservation:
        for champ, valeur in donnees.items():
            if valeur is not None:
                setattr(reservation, champ, valeur)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def supprimer(self, reservation: Reservation) -> None:
        self.db.delete(reservation)
        self.db.commit()

    def a_des_services(self, reservation_id: int) -> bool:
        """Vérifie si la réservation a des services liés — bloque la suppression."""
        count = (
            self.db.query(Service)
            .filter(Service.reservation_id == reservation_id)
            .count()
        )
        return count > 0
