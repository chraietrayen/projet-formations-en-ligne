from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.database import Base

class Formation(Base):
    """Modèle pour la table formation"""
    __tablename__ = "formation"
    
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(100), nullable=False)
    description = Column(Text)
    duree = Column(Integer, nullable=False)  # en heures
    niveau = Column(String(50))  # débutant, intermédiaire, avancé
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    etudiants = relationship("Etudiant", secondary="inscription", back_populates="formations")