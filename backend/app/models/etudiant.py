from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base

class Etudiant(Base):
    """Modèle pour la table étudiant"""
    __tablename__ = "etudiant"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    departement_id = Column(Integer, ForeignKey("departement.id"))
    date_naissance = Column(Date)
    adresse = Column(Text)
    telephone = Column(String(20))
    photo_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    departement = relationship("Departement")
    formations = relationship("Formation", secondary="inscription", back_populates="etudiants")