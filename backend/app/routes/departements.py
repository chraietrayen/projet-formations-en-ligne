from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.crud import departement as crud
from ..schemas.departement import Departement, DepartementCreate, DepartementUpdate

router = APIRouter(
    prefix="/departements",
    tags=["Départements"],
    responses={404: {"description": "Département non trouvé"}},
)

@router.get("/", response_model=List[Departement])
def read_departements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère la liste des départements.
    """
    departements = crud.get_departements(db, skip=skip, limit=limit)
    return departements

@router.get("/{departement_id}", response_model=Departement)
def read_departement(departement_id: int, db: Session = Depends(get_db)):
    """
    Récupère un département spécifique par son ID.
    """
    db_departement = crud.get_departement(db, departement_id=departement_id)
    if db_departement is None:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return db_departement

@router.post("/", response_model=Departement, status_code=status.HTTP_201_CREATED)
def create_departement(departement: DepartementCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau département.
    """
    return crud.create_departement(db=db, departement=departement)

@router.put("/{departement_id}", response_model=Departement)
def update_departement(departement_id: int, departement: DepartementUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un département existant.
    """
    db_departement = crud.update_departement(db, departement_id=departement_id, departement=departement)
    if db_departement is None:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return db_departement

@router.delete("/{departement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_departement(departement_id: int, db: Session = Depends(get_db)):
    """
    Supprime un département.
    """
    success = crud.delete_departement(db, departement_id=departement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return None