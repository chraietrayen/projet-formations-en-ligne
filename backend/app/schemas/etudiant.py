from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from .departement import Departement

class EtudiantBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    departement_id: Optional[int] = None
    date_naissance: Optional[date] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    photo_url: Optional[str] = None

class EtudiantCreate(EtudiantBase):
    password: str

class EtudiantUpdate(EtudiantBase):
    password: Optional[str] = None

class Etudiant(EtudiantBase):
    id: int
    created_at: datetime
    departement: Optional[Departement] = None
    
    class Config:
        orm_mode = True