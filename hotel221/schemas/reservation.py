from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
from hotel221.models.reservation import StatutReservation
from hotel221.schemas.chambre import ChambreResponse
from hotel221.schemas.client import ClientResponse


class ReservationCreate(BaseModel):
    client_id: int = Field(..., gt=0, description="ID du client", example=1)
    chambre_id: int = Field(..., gt=0, description="ID de la chambre", example=1)
    date_arrivee: datetime = Field(..., description="Date d'arrivée (>= aujourd'hui)", example="2026-06-01T00:00:00")
    date_depart: datetime = Field(..., description="Date de départ (> dateArrivee)", example="2026-06-05T00:00:00")

    @model_validator(mode="after")
    def valider_dates(self):
        if self.date_depart <= self.date_arrivee:
            raise ValueError("La date de départ doit être supérieure à la date d'arrivée")
        return self


class ReservationUpdate(BaseModel):
    statut: StatutReservation = Field(..., description="Nouveau statut")


class ReservationResponse(BaseModel):
    id: int
    client_id: int
    chambre_id: int
    date_arrivee: datetime
    date_depart: datetime
    montant: float
    statut: StatutReservation
    client: Optional[ClientResponse] = None
    chambre: Optional[ChambreResponse] = None

    model_config = {"from_attributes": True}
