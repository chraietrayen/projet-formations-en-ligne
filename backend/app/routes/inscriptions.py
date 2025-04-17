from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.crud import inscription as crud
from ..schemas.inscription import Inscription, InscriptionCreate, InscriptionUpdate, InscriptionDetail
from ..auth import get_current_etudiant
from ..models.etudiant import Etudiant

router = APIRouter(
    prefix="/inscriptions",
    tags=["Inscriptions"],
    responses={404: {"description": "Inscription non trouvée"}},
)

@router.get("/", response_model=List[Inscription])
def read_inscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère la liste des inscriptions.
    """
    inscriptions = crud.get_inscriptions(db, skip=skip, limit=limit)
    return inscriptions

@router.get("/me", response_model=List[Inscription])
def read_mes_inscriptions(current_etudiant: Etudiant = Depends(get_current_etudiant), db: Session = Depends(get_db)):
    """
    Récupère les inscriptions de l'étudiant connecté.
    """
    inscriptions = crud.get_inscriptions_by_etudiant(db, etudiant_id=current_etudiant.id)
    return inscriptions

@router.get("/{inscription_id}", response_model=InscriptionDetail)
def read_inscription(inscription_id: int, db: Session = Depends(get_db)):
    """
    Récupère une inscription spécifique par son ID.
    """
    db_inscription = crud.get_inscription(db, inscription_id=inscription_id)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    return db_inscription

@router.get("/formation/{formation_id}", response_model=List[Inscription])
def read_inscriptions_by_formation(formation_id: int, db: Session = Depends(get_db)):
    """
    Récupère les inscriptions pour une formation spécifique.
    """
    inscriptions = crud.get_inscriptions_by_formation(db, formation_id=formation_id)
    return inscriptions

@router.get("/etudiant/{etudiant_id}", response_model=List[Inscription])
def read_inscriptions_by_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    """
    Récupère les inscriptions pour un étudiant spécifique.
    """
    inscriptions = crud.get_inscriptions_by_etudiant(db, etudiant_id=etudiant_id)
    return inscriptions

@router.post("/", response_model=Inscription, status_code=status.HTTP_201_CREATED)
def create_inscription(
    inscription: InscriptionCreate, 
    current_etudiant: Etudiant = Depends(get_current_etudiant),
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle inscription pour l'étudiant connecté.
    """
    # Force l'ID de l'étudiant connecté pour sécuriser l'API
    inscription_data = inscription.dict()
    inscription_data["etudiant_id"] = current_etudiant.id
    
    # Vérifie si l'étudiant est déjà inscrit à cette formation
    for existing_inscription in crud.get_inscriptions_by_etudiant(db, etudiant_id=current_etudiant.id):
        if existing_inscription.formation_id == inscription.formation_id:
            raise HTTPException(
                status_code=400,
                detail="Vous êtes déjà inscrit à cette formation"
            )
    
    return crud.create_inscription(db=db, inscription=InscriptionCreate(**inscription_data))

@router.put("/{inscription_id}", response_model=Inscription)
def update_inscription(
    inscription_id: int, 
    inscription: InscriptionUpdate, 
    db: Session = Depends(get_db),
    current_etudiant: Etudiant = Depends(get_current_etudiant)
):
    """
    Met à jour une inscription existante.
    """
    # Vérifier que l'inscription appartient à l'étudiant connecté
    db_inscription = crud.get_inscription(db, inscription_id=inscription_id)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    
    if db_inscription.etudiant_id != current_etudiant.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé à cette inscription")
    
    return crud.update_inscription(db, inscription_id=inscription_id, inscription=inscription)

@router.delete("/{inscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscription(
    inscription_id: int, 
    db: Session = Depends(get_db),
    current_etudiant: Etudiant = Depends(get_current_etudiant)
):
    """
    Supprime une inscription.
    """
    # Vérifier que l'inscription appartient à l'étudiant connecté
    db_inscription = crud.get_inscription(db, inscription_id=inscription_id)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    
    if db_inscription.etudiant_id != current_etudiant.id:
        raise HTTPException(status_code=403, detail="Accès non autorisé à cette inscription")
    
    success = crud.delete_inscription(db, inscription_id=inscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    return None