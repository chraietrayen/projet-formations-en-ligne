from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .etudiant import Etudiant
from .formation import Formation

class InscriptionBase(BaseModel):
    etudiant_id: int
    formation_id: int
    statut: Optional[str] = "en cours"
    progression: Optional[int] = 0

class InscriptionCreate(InscriptionBase):
    pass

class InscriptionUpdate(InscriptionBase):
    etudiant_id: Optional[int] = None
    formation_id: Optional[int] = None
    statut: Optional[str] = None
    progression: Optional[int] = None

class Inscription(InscriptionBase):
    id: int
    date_inscription: datetime
    
    class Config:
        orm_mode = True

class InscriptionDetail(Inscription):
    etudiant: Etudiant
    formation: Formation
    
    class Config:
        orm_mode = True