from sqlalchemy.orm import Session
from datetime import datetime, timezone
from hotel221.repositories.reservation_repo import ReservationRepository
from hotel221.repositories.chambre_repo import ChambreRepository
from hotel221.repositories.client_repo import ClientRepository
from hotel221.schemas.reservation import ReservationCreate, ReservationUpdate
from hotel221.models.reservation import Reservation, StatutReservation
from hotel221.utils.errors import not_found, conflict, bad_request
from typing import Optional, List


class ReservationService:
    """Logique métier pour les réservations."""

    def __init__(self, db: Session):
        self.repo = ReservationRepository(db)
        self.chambre_repo = ChambreRepository(db)
        self.client_repo = ClientRepository(db)

    def lister(
        self,
        statut: Optional[str] = None,
        client_id: Optional[int] = None,
        chambre_id: Optional[int] = None,
    ) -> List[Reservation]:
        return self.repo.trouver_toutes(
            statut=statut, client_id=client_id, chambre_id=chambre_id
        )

    def obtenir(self, reservation_id: int) -> Reservation:
        reservation = self.repo.trouver_par_id(reservation_id)
        if not reservation:
            not_found("Réservation", reservation_id)
        return reservation

    def creer(self, donnees: ReservationCreate) -> Reservation:
        # 1. Vérifier l'existence du client
        client = self.client_repo.trouver_par_id(donnees.client_id)
        if not client:
            not_found("Client", donnees.client_id)

        # 2. Vérifier l'existence de la chambre
        chambre = self.chambre_repo.trouver_par_id(donnees.chambre_id)
        if not chambre:
            not_found("Chambre", donnees.chambre_id)

        # 3. Valider dateArrivee >= aujourd'hui
        aujourdhui = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0, tzinfo=None
        )
        arrivee = donnees.date_arrivee.replace(tzinfo=None)
        depart = donnees.date_depart.replace(tzinfo=None)

        if arrivee < aujourdhui:
            bad_request("La date d'arrivée doit être égale ou supérieure à aujourd'hui")

        # 4. Valider dateDepart > dateArrivee (déjà validé par Pydantic mais on re-vérifie)
        if depart <= arrivee:
            bad_request("La date de départ doit être supérieure à la date d'arrivée")

        # 5. Vérifier qu'aucune réservation CONFIRMEE ne chevauche les dates
        if self.chambre_repo.verifier_chevauchement(donnees.chambre_id, arrivee, depart):
            conflict("La chambre est déjà réservée (CONFIRMEE) pour ces dates")

        # 6. Calculer le montant : nombre de nuits × prix par nuit
        nb_nuits = (depart - arrivee).days
        montant = nb_nuits * chambre.prix_par_nuit

        # 7. Créer avec statut CONFIRMEE automatiquement
        return self.repo.creer({
            "client_id": donnees.client_id,
            "chambre_id": donnees.chambre_id,
            "date_arrivee": arrivee,
            "date_depart": depart,
            "montant": montant,
            "statut": StatutReservation.CONFIRMEE,
        })

    def mettre_a_jour(self, reservation_id: int, donnees: ReservationUpdate) -> Reservation:
        reservation = self.obtenir(reservation_id)
        return self.repo.mettre_a_jour(
            reservation, donnees.model_dump(exclude_none=True)
        )

    def supprimer(self, reservation_id: int) -> None:
        reservation = self.obtenir(reservation_id)

        # Interdire suppression si des services sont liés
        if self.repo.a_des_services(reservation_id):
            conflict("Impossible de supprimer : la réservation a des services associés")

        self.repo.supprimer(reservation)
