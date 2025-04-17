from sqlalchemy.orm import Session
from ...models.formation import Formation
from ...schemas.formation import FormationCreate, FormationUpdate

def get_formations(db: Session, skip: int = 0, limit: int = 100):
    """Récupérer toutes les formations"""
    return db.query(Formation).offset(skip).limit(limit).all()

def get_formation(db: Session, formation_id: int):
    """Récupérer une formation par son ID"""
    return db.query(Formation).filter(Formation.id == formation_id).first()

def create_formation(db: Session, formation: FormationCreate):
    """Créer une nouvelle formation"""
    db_formation = Formation(**formation.dict())
    db.add(db_formation)
    db.commit()
    db.refresh(db_formation)
    return db_formation

def update_formation(db: Session, formation_id: int, formation: FormationUpdate):
    """Mettre à jour une formation"""
    db_formation = get_formation(db, formation_id)
    if db_formation:
        update_data = formation.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_formation, key, value)
        db.commit()
        db.refresh(db_formation)
    return db_formation

def delete_formation(db: Session, formation_id: int):
    """Supprimer une formation"""
    db_formation = get_formation(db, formation_id)
    if db_formation:
        db.delete(db_formation)
        db.commit()
        return True
    return False