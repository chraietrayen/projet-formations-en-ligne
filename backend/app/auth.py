from datetime import datetime, timedelta
from jose import JWTError, jwt # type: ignore
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from .db.database import get_db
from .db.crud.etudiant import get_etudiant_by_email
from .models.etudiant import Etudiant

# Configuration de sécurité
SECRET_KEY = "votre_cle_secrete_tres_longue_et_complexe_a_changer_en_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 jour

# Point de terminaison OAuth2 pour obtenir le token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Créer un token d'accès JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_etudiant(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Récupérer l'étudiant actuel à partir du token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identification impossible",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    etudiant = get_etudiant_by_email(db, email=email)
    if etudiant is None:
        raise credentials_exception
    return etudiant