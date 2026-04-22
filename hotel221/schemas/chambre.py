from pydantic import BaseModel, Field, field_validator
from typing import Optional
from hotel221.models.chambre import TypeChambre, StatutChambre


class ChambreCreate(BaseModel):
    numero: str = Field(..., min_length=1, description="Numéro unique de la chambre", example="101")
    type: TypeChambre = Field(..., description="Type : SIMPLE, DOUBLE ou SUITE", example="SIMPLE")
    prix_par_nuit: float = Field(..., gt=0, description="Prix par nuit (doit être > 0)", example=45000)
    statut: Optional[StatutChambre] = Field(StatutChambre.LIBRE, description="Statut de la chambre")

    @field_validator("numero")
    @classmethod
    def numero_non_vide(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Le numéro de chambre ne peut pas être vide")
        return v.strip()


class ChambreUpdate(BaseModel):
    numero: Optional[str] = Field(None, min_length=1)
    type: Optional[TypeChambre] = None
    prix_par_nuit: Optional[float] = Field(None, gt=0)
    statut: Optional[StatutChambre] = None


class ChambreResponse(BaseModel):
    id: int
    numero: str
    type: TypeChambre
    prix_par_nuit: float
    statut: StatutChambre

    model_config = {"from_attributes": True}
