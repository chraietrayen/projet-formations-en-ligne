from sqlalchemy.orm import Session
from ...models.etudiant import Etudiant
from ...schemas.etudiant import EtudiantCreate, EtudiantUpdate
from passlib.context import CryptContext # type: ignore

# Configuration du hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_etudiants(db: Session, skip: int = 0, limit: int = 100):
    """Récupérer tous les étudiants"""
    return db.query(Etudiant).offset(skip).limit(limit).all()

def get_etudiant(db: Session, etudiant_id: int):
    """Récupérer un étudiant par son ID"""
    return db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()

def get_etudiant_by_email(db: Session, email: str):
    """Récupérer un étudiant par son email"""
    return db.query(Etudiant).filter(Etudiant.email == email).first()

def create_etudiant(db: Session, etudiant: EtudiantCreate):
    """Créer un nouvel étudiant"""
    # Hachage du mot de passe
    hashed_password = pwd_context.hash(etudiant.password)
    # Création de l'étudiant avec le mot de passe haché
    db_etudiant = Etudiant(**etudiant.dict(exclude={"password"}), password=hashed_password)
    db.add(db_etudiant)
    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant

def update_etudiant(db: Session, etudiant_id: int, etudiant: EtudiantUpdate):
    """Mettre à jour un étudiant"""
    db_etudiant = get_etudiant(db, etudiant_id)
    if db_etudiant:
        update_data = etudiant.dict(exclude_unset=True)
        # Si un nouveau mot de passe est fourni, le hacher
        if "password" in update_data and update_data["password"]:
            update_data["password"] = pwd_context.hash(update_data["password"])
        for key, value in update_data.items():
            setattr(db_etudiant, key, value)
        db.commit()
        db.refresh(db_etudiant)
    return db_etudiant

def delete_etudiant(db: Session, etudiant_id: int):
    """Supprimer un étudiant"""
    db_etudiant = get_etudiant(db, etudiant_id)
    if db_etudiant:
        db.delete(db_etudiant)
        db.commit()
        return True
    return False

def verify_password(plain_password, hashed_password):
    """Vérifier si un mot de passe correspond au hachage"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_etudiant(db: Session, email: str, password: str):
    """Authentifier un étudiant"""
    etudiant = get_etudiant_by_email(db, email)
    if not etudiant or not verify_password(password, etudiant.password):
        return False
    return etudiant