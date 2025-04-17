from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.crud import formation as crud
from ..schemas.formation import Formation, FormationCreate, FormationUpdate

router = APIRouter(
    prefix="/formations",
    tags=["Formations"],
    responses={404: {"description": "Formation non trouvée"}},
)

@router.get("/", response_model=List[Formation])
def read_formations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère la liste des formations.
    """
    formations = crud.get_formations(db, skip=skip, limit=limit)
    return formations

@router.get("/{formation_id}", response_model=Formation)
def read_formation(formation_id: int, db: Session = Depends(get_db)):
    """
    Récupère une formation spécifique par son ID.
    """
    db_formation = crud.get_formation(db, formation_id=formation_id)
    if db_formation is None:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return db_formation

@router.post("/", response_model=Formation, status_code=status.HTTP_201_CREATED)
def create_formation(formation: FormationCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle formation.
    """
    return crud.create_formation(db=db, formation=formation)

@router.put("/{formation_id}", response_model=Formation)
def update_formation(formation_id: int, formation: FormationUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une formation existante.
    """
    db_formation = crud.update_formation(db, formation_id=formation_id, formation=formation)
    if db_formation is None:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return db_formation

@router.delete("/{formation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    """
    Supprime une formation.
    """
    success = crud.delete_formation(db, formation_id=formation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return None