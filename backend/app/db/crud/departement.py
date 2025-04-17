from sqlalchemy.orm import Session
from ...models.departement import Departement
from ...schemas.departement import DepartementCreate, DepartementUpdate

def get_departements(db: Session, skip: int = 0, limit: int = 100):
    """Récupérer tous les départements"""
    return db.query(Departement).offset(skip).limit(limit).all()

def get_departement(db: Session, departement_id: int):
    """Récupérer un département par son ID"""
    return db.query(Departement).filter(Departement.id == departement_id).first()

def create_departement(db: Session, departement: DepartementCreate):
    """Créer un nouveau département"""
    db_departement = Departement(**departement.dict())
    db.add(db_departement)
    db.commit()
    db.refresh(db_departement)
    return db_departement

def update_departement(db: Session, departement_id: int, departement: DepartementUpdate):
    """Mettre à jour un département"""
    db_departement = get_departement(db, departement_id)
    if db_departement:
        update_data = departement.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_departement, key, value)
        db.commit()
        db.refresh(db_departement)
    return db_departement

def delete_departement(db: Session, departement_id: int):
    """Supprimer un département"""
    db_departement = get_departement(db, departement_id)
    if db_departement:
        db.delete(db_departement)
        db.commit()
        return True
    return False