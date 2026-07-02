import enum
from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from hotel221.config.database import Base


class TypeChambre(str, enum.Enum):
    SIMPLE = "SIMPLE"
    DOUBLE = "DOUBLE"
    SUITE = "SUITE"

class StatutChambre(str, enum.Enum):
    LIBRE = "LIBRE"
    OCCUPEE = "OCCUPEE"
    MAINTENANCE = "MAINTENANCE"


class Chambre(Base):
    __tablename__ = "chambres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String, unique=True, nullable=False)
    type = Column(Enum(TypeChambre), nullable=False)
    prix_par_nuit = Column(Float, nullable=False)
    statut = Column(Enum(StatutChambre), nullable=False, default=StatutChambre.LIBRE)

    # Relation 1 → N avec Reservation
    reservations = relationship("Reservation", back_populates="chambre")
