from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepartementBase(BaseModel):
    nom: str
    description: Optional[str] = None

class DepartementCreate(DepartementBase):
    pass

class DepartementUpdate(DepartementBase):
    pass

class Departement(DepartementBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True