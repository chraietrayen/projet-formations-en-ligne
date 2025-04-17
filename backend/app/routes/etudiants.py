from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.crud import etudiant as crud
from ..schemas.etudiant import Etudiant, EtudiantCreate, EtudiantUpdate
from ..auth import get_current_etudiant
from datetime import timedelta
from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/etudiants",
    tags=["Étudiants"],
    responses={404: {"description": "Étudiant non trouvé"}},
)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authentification et génération de token JWT.
    """
    etudiant = crud.authenticate_etudiant(db, form_data.username, form_data.password)
    if not etudiant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": etudiant.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=List[Etudiant])
def read_etudiants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère la liste des étudiants.
    """
    etudiants = crud.get_etudiants(db, skip=skip, limit=limit)
    return etudiants

@router.get("/me", response_model=Etudiant)
def read_etudiant_me(current_etudiant: Etudiant = Depends(get_current_etudiant)):
    """
    Récupère les informations de l'étudiant actuellement connecté.
    """
    return current_etudiant

@router.get("/{etudiant_id}", response_model=Etudiant)
def read_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    """
    Récupère un étudiant spécifique par son ID.
    """
    db_etudiant = crud.get_etudiant(db, etudiant_id=etudiant_id)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return db_etudiant

@router.post("/", response_model=Etudiant, status_code=status.HTTP_201_CREATED)
def create_etudiant(etudiant: EtudiantCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel étudiant (inscription).
    """
    # Vérifier si l'email existe déjà
    db_etudiant = crud.get_etudiant_by_email(db, email=etudiant.email)
    if db_etudiant:
        raise HTTPException(
            status_code=400,
            detail="Email déjà enregistré"
        )
    return crud.create_etudiant(db=db, etudiant=etudiant)

@router.put("/{etudiant_id}", response_model=Etudiant)
def update_etudiant(etudiant_id: int, etudiant: EtudiantUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un étudiant existant.
    """
    db_etudiant = crud.update_etudiant(db, etudiant_id=etudiant_id, etudiant=etudiant)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return db_etudiant

@router.delete("/{etudiant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    """
    Supprime un étudiant.
    """
    success = crud.delete_etudiant(db, etudiant_id=etudiant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return None