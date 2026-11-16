from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas

# Esto lee el archivo models.py y crea las tablas físicas en SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CanariasDona API",
    description="Backend para la plataforma comunitaria de donación en Canarias"
)

# Dependencia para conectarse a la Base de Datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido al backend de CanariasDona!"}

# --- CRUD DE ISLAS ---

# 1. Crear una Isla (POST)
@app.post("/islas/", response_model=schemas.Isla)
def create_isla(isla: schemas.IslaCreate, db: Session = Depends(get_db)):
    db_isla = models.Isla(nombre=isla.nombre)
    db.add(db_isla)
    db.commit()
    db.refresh(db_isla)
    return db_isla

# 2. Leer todas las Islas (GET)
@app.get("/islas/", response_model=list[schemas.Isla])
def read_islas(db: Session = Depends(get_db)):
    islas = db.query(models.Isla).all()
    return islas

# 3. Actualizar una Isla (PUT)
@app.put("/islas/{isla_id}", response_model=schemas.Isla)
def update_isla(isla_id: int, isla_actualizada: schemas.IslaCreate, db: Session = Depends(get_db)):
    db_isla = db.query(models.Isla).filter(models.Isla.id == isla_id).first()
    if db_isla:
        db_isla.nombre = isla_actualizada.nombre
        db.commit()
        db.refresh(db_isla)
        return db_isla
    return {"error": "Isla no encontrada"}

# 4. Borrar una Isla (DELETE)
@app.delete("/islas/{isla_id}")
def delete_isla(isla_id: int, db: Session = Depends(get_db)):
    db_isla = db.query(models.Isla).filter(models.Isla.id == isla_id).first()
    if db_isla:
        db.delete(db_isla)
        db.commit()
        return {"mensaje": f"Isla {isla_id} eliminada correctamente"}
    return {"error": "Isla no encontrada"}

# --- CRUD DE CATEGORÍAS ---

@app.post("/categorias/", response_model=schemas.Categoria)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = models.Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.get("/categorias/", response_model=list[schemas.Categoria])
def read_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()

# --- CRUD DE MUNICIPIOS ---

@app.post("/municipios/", response_model=schemas.Municipio)
def create_municipio(municipio: schemas.MunicipioCreate, db: Session = Depends(get_db)):
    db_municipio = models.Municipio(nombre=municipio.nombre, isla_id=municipio.isla_id)
    db.add(db_municipio)
    db.commit()
    db.refresh(db_municipio)
    return db_municipio

@app.get("/municipios/", response_model=list[schemas.Municipio])
def read_municipios(db: Session = Depends(get_db)):
    return db.query(models.Municipio).all()