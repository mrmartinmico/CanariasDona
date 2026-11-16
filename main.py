from fastapi import FastAPI
from database import engine, Base

# Esto crea el archivo físico de la base de datos si no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CanariasDona API",
    description="Backend para la plataforma comunitaria de donación en Canarias"
)

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido al backend de CanariasDona!"}