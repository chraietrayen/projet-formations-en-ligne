import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Base de données
    DATABASE_URL: str = "mysql+pymysql://root:@localhost/formations_en_ligne"
    
    # Sécurité
    SECRET_KEY: str = "votre_cle_secrete_tres_longue_et_complexe_a_changer_en_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 jour
    
    # Cors
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # Frontend NextJS
        "http://localhost:4200",  # Frontend Angular
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()