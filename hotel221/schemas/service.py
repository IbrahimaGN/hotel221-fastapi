from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ServiceCreate(BaseModel):
    reservation_id: int = Field(..., gt=0, description="ID de la réservation (doit être CONFIRMEE)", example=1)
    libelle: str = Field(..., min_length=1, description="Libellé du service", example="Petit-déjeuner")
    prix: float = Field(..., ge=0, description="Prix du service (>= 0)", example=5000)
    date: datetime = Field(..., description="Date du service", example="2026-06-02T08:00:00")

    @field_validator("libelle")
    @classmethod
    def libelle_non_vide(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Le libellé ne peut pas être vide")
        return v.strip()


class ServiceResponse(BaseModel):
    id: int
    libelle: str
    prix: float
    date: datetime
    reservation_id: int

    model_config = {"from_attributes": True}
