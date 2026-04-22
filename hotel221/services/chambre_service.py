from sqlalchemy.orm import Session
from hotel221.repositories.chambre_repo import ChambreRepository
from hotel221.schemas.chambre import ChambreCreate, ChambreUpdate
from hotel221.models.chambre import Chambre
from hotel221.utils.errors import not_found, conflict
from typing import Optional, List


class ChambreService:
    """Logique métier pour les chambres."""

    def __init__(self, db: Session):
        self.repo = ChambreRepository(db)

    def lister(self, type: Optional[str] = None, statut: Optional[str] = None) -> List[Chambre]:
        return self.repo.trouver_toutes(type=type, statut=statut)

    def obtenir(self, chambre_id: int) -> Chambre:
        chambre = self.repo.trouver_par_id(chambre_id)
        if not chambre:
            not_found("Chambre", chambre_id)
        return chambre

    def creer(self, donnees: ChambreCreate) -> Chambre:
        # Vérifier l'unicité du numéro
        existant = self.repo.trouver_par_numero(donnees.numero)
        if existant:
            conflict(f"Une chambre avec le numéro \"{donnees.numero}\" existe déjà")

        return self.repo.creer(donnees.model_dump())

    def mettre_a_jour(self, chambre_id: int, donnees: ChambreUpdate) -> Chambre:
        chambre = self.obtenir(chambre_id)

        # Vérifier l'unicité du numéro si modifié
        if donnees.numero:
            existant = self.repo.trouver_par_numero(donnees.numero)
            if existant and existant.id != chambre_id:
                conflict(f"Une chambre avec le numéro \"{donnees.numero}\" existe déjà")

        return self.repo.mettre_a_jour(chambre, donnees.model_dump(exclude_none=True))

    def supprimer(self, chambre_id: int) -> None:
        chambre = self.obtenir(chambre_id)

        # Interdire suppression si réservations CONFIRMEE existent
        if self.repo.a_des_reservations_confirmees(chambre_id):
            conflict("Impossible de supprimer : la chambre a des réservations confirmées en cours")

        self.repo.supprimer(chambre)
