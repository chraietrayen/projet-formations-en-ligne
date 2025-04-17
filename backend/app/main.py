from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine, Base
from .routes import departements_router, etudiants_router, formations_router, inscriptions_router
import uvicorn

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="API de Formation en Ligne",
    description="API pour la gestion des formations en ligne",
    version="1.0.0",
)

# Configuration CORS pour permettre les requêtes cross-origin
origins = [
    "http://localhost:3000",  # Frontend NextJS
    "http://localhost:4200",  # Frontend Angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(departements_router)
app.include_router(etudiants_router)
app.include_router(formations_router)
app.include_router(inscriptions_router)

# Route racine
@app.get("/", tags=["Racine"])
async def read_root():
    """
    Point d'entrée principal de l'API.
    """
    return {
        "message": "Bienvenue sur l'API de Formation en Ligne",
        "documentation": "/docs",
    }

# Point d'entrée pour exécuter l'application avec uvicorn
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)