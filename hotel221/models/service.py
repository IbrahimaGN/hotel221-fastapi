from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from hotel221.config.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    libelle = Column(String, nullable=False)
    prix = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)

    # Relation N → 1 avec Reservation
    reservation = relationship("Reservation", back_populates="services")
