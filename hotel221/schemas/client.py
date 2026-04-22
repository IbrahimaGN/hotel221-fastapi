from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional


class ClientCreate(BaseModel):
    prenom: str = Field(..., min_length=2, max_length=50, description="Prénom (min 2 caractères)", example="Mamadou")
    nom: str = Field(..., min_length=2, max_length=50, description="Nom (min 2 caractères)", example="Diallo")
    email: EmailStr = Field(..., description="Email unique", example="mamadou.diallo@email.com")
    telephone: Optional[str] = Field(None, description="Téléphone (optionnel)", example="+221771234567")
    piece_identite: str = Field(..., description="Numéro de pièce d'identité unique", example="SN-2024-001")

    @field_validator("prenom", "nom")
    @classmethod
    def min_deux_caracteres(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Doit contenir au moins 2 caractères")
        return v.strip()


class ClientUpdate(BaseModel):
    prenom: Optional[str] = Field(None, min_length=2, max_length=50)
    nom: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    piece_identite: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    prenom: str
    nom: str
    email: str
    telephone: Optional[str]
    piece_identite: str

    model_config = {"from_attributes": True}
