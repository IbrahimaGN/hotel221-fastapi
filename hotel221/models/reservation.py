import enum
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from hotel221.config.database import Base


class StatutReservation(str, enum.Enum):
    CONFIRMEE = "CONFIRMEE"
    ANNULEE = "ANNULEE"
    TERMINEE = "TERMINEE"


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    chambre_id = Column(Integer, ForeignKey("chambres.id"), nullable=False)
    date_arrivee = Column(DateTime, nullable=False)
    date_depart = Column(DateTime, nullable=False)
    montant = Column(Float, nullable=False)
    statut = Column(Enum(StatutReservation), nullable=False, default=StatutReservation.CONFIRMEE)

    # Relations
    client = relationship("Client", back_populates="reservations")
    chambre = relationship("Chambre", back_populates="reservations")
    services = relationship("Service", back_populates="reservation")
