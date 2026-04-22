from sqlalchemy.orm import Session, joinedload
from hotel221.models.service import Service
from typing import Optional, List


class ServiceRepository:
    """Accès base de données pour les services via SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def trouver_tous(self, reservation_id: Optional[int] = None) -> List[Service]:
        query = self.db.query(Service).options(
            joinedload(Service.reservation)
        )
        if reservation_id:
            query = query.filter(Service.reservation_id == reservation_id)
        return query.order_by(Service.date.desc()).all()

    def trouver_par_id(self, service_id: int) -> Optional[Service]:
        return (
            self.db.query(Service)
            .options(joinedload(Service.reservation))
            .filter(Service.id == service_id)
            .first()
        )

    def creer(self, donnees: dict) -> Service:
        service = Service(**donnees)
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return service

    def supprimer(self, service: Service) -> None:
        self.db.delete(service)
        self.db.commit()
