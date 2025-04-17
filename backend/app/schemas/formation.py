from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FormationBase(BaseModel):
    titre: str
    description: Optional[str] = None
    duree: int
    niveau: Optional[str] = None
    image_url: Optional[str] = None

class FormationCreate(FormationBase):
    pass

class FormationUpdate(FormationBase):
    pass

class Formation(FormationBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True