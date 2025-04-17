from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la connexion à MySQL
DATABASE_URL = "mysql+pymysql://root:@localhost/formations_en_ligne"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création de la SessionLocal pour la connexion à la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles SQLAlchemy
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()