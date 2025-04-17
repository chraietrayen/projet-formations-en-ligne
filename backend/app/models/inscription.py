from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from ..db.database import Base

class Inscription(Base):
    """Modèle pour la table inscription (relation entre Etudiant et Formation)"""
    __tablename__ = "inscription"
    
    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiant.id"), nullable=False)
    formation_id = Column(Integer, ForeignKey("formation.id"), nullable=False)
    date_inscription = Column(DateTime(timezone=True), server_default=func.now())
    statut = Column(String(50), default="en cours")  # en cours, terminé, abandonné
    progression = Column(Integer, default=0)  # pourcentage de progression
    
    # Contrainte d'unicité
    __table_args__ = (UniqueConstraint('etudiant_id', 'formation_id', name='unique_etudiant_formation'),)