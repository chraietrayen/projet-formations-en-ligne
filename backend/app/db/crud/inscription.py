from sqlalchemy.orm import Session
from ...models.inscription import Inscription
from ...schemas.inscription import InscriptionCreate, InscriptionUpdate

def get_inscriptions(db: Session, skip: int = 0, limit: int = 100):
    """Récupérer toutes les inscriptions"""
    return db.query(Inscription).offset(skip).limit(limit).all()

def get_inscription(db: Session, inscription_id: int):
    """Récupérer une inscription par son ID"""
    return db.query(Inscription).filter(Inscription.id == inscription_id).first()

def get_inscriptions_by_etudiant(db: Session, etudiant_id: int):
    """Récupérer les inscriptions d'un étudiant"""
    return db.query(Inscription).filter(Inscription.etudiant_id == etudiant_id).all()

def get_inscriptions_by_formation(db: Session, formation_id: int):
    """Récupérer les inscriptions à une formation"""
    return db.query(Inscription).filter(Inscription.formation_id == formation_id).all()

def create_inscription(db: Session, inscription: InscriptionCreate):
    """Créer une nouvelle inscription"""
    db_inscription = Inscription(**inscription.dict())
    db.add(db_inscription)
    db.commit()
    db.refresh(db_inscription)
    return db_inscription

def update_inscription(db: Session, inscription_id: int, inscription: InscriptionUpdate):
    """Mettre à jour une inscription"""
    db_inscription = get_inscription(db, inscription_id)
    if db_inscription:
        update_data = inscription.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_inscription, key, value)
        db.commit()
        db.refresh(db_inscription)
    return db_inscription

def delete_inscription(db: Session, inscription_id: int):
    """Supprimer une inscription"""
    db_inscription = get_inscription(db, inscription_id)
    if db_inscription:
        db.delete(db_inscription)
        db.commit()
        return True
    return False