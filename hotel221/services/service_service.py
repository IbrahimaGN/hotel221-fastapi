from sqlalchemy.orm import Session
from hotel221.repositories.service_repo import ServiceRepository
from hotel221.repositories.reservation_repo import ReservationRepository
from hotel221.schemas.service import ServiceCreate
from hotel221.models.service import Service
from hotel221.models.reservation import StatutReservation
from hotel221.utils.errors import not_found, bad_request
from typing import Optional, List


class ServiceService:
    """Logique métier pour les services supplémentaires."""

    def __init__(self, db: Session):
        self.repo = ServiceRepository(db)
        self.reservation_repo = ReservationRepository(db)

    def lister(self, reservation_id: Optional[int] = None) -> List[Service]:
        return self.repo.trouver_tous(reservation_id=reservation_id)

    def obtenir(self, service_id: int) -> Service:
        service = self.repo.trouver_par_id(service_id)
        if not service:
            not_found("Service", service_id)
        return service

    def creer(self, donnees: ServiceCreate) -> Service:
        # 1. Vérifier l'existence de la réservation
        reservation = self.reservation_repo.trouver_par_id(donnees.reservation_id)
        if not reservation:
            not_found("Réservation", donnees.reservation_id)

        # 2. Vérifier que la réservation est CONFIRMEE
        if reservation.statut != StatutReservation.CONFIRMEE:
            bad_request(
                f"Impossible d'ajouter un service : la réservation doit être CONFIRMEE "
                f"(statut actuel : {reservation.statut.value})"
            )

        return self.repo.creer(donnees.model_dump())

    def supprimer(self, service_id: int) -> None:
        service = self.obtenir(service_id)
        self.repo.supprimer(service)
