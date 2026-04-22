from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from hotel221.config.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prenom = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telephone = Column(String, nullable=True)
    piece_identite = Column(String, unique=True, nullable=False)

    # Relation 1 → N avec Reservation
    reservations = relationship("Reservation", back_populates="client")
