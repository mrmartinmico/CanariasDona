from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas

# Crea las tablas físicas en SQLite a partir de models.py
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

# --- INICIO ---

@app.get("/", tags=["Inicio"], summary="Mensaje de bienvenida")
def read_root():
    return {"mensaje": "¡Bienvenido al backend de CanariasDona!"}

# --- CRUD DE ISLAS ---

@app.post("/islas/", response_model=schemas.Isla, tags=["Islas"], summary="Crear una isla")
def create_isla(isla: schemas.IslaCreate, db: Session = Depends(get_db)):
    db_isla = models.Isla(nombre=isla.nombre)
    db.add(db_isla)
    db.commit()
    db.refresh(db_isla)
    return db_isla

@app.get("/islas/", response_model=list[schemas.Isla], tags=["Islas"], summary="Listar todas las islas")
def read_islas(db: Session = Depends(get_db)):
    return db.query(models.Isla).all()

@app.put("/islas/{isla_id}", response_model=schemas.Isla, tags=["Islas"], summary="Actualizar una isla")
def update_isla(isla_id: int, isla_actualizada: schemas.IslaCreate, db: Session = Depends(get_db)):
    db_isla = db.query(models.Isla).filter(models.Isla.id == isla_id).first()
    if not db_isla:
        raise HTTPException(status_code=404, detail="Isla no encontrada")
    db_isla.nombre = isla_actualizada.nombre
    db.commit()
    db.refresh(db_isla)
    return db_isla

@app.delete("/islas/{isla_id}", tags=["Islas"], summary="Eliminar una isla")
def delete_isla(isla_id: int, db: Session = Depends(get_db)):
    db_isla = db.query(models.Isla).filter(models.Isla.id == isla_id).first()
    if not db_isla:
        raise HTTPException(status_code=404, detail="Isla no encontrada")
    db.delete(db_isla)
    db.commit()
    return {"mensaje": f"Isla {isla_id} eliminada correctamente"}

# --- CRUD DE MUNICIPIOS ---

@app.post("/municipios/", response_model=schemas.Municipio, tags=["Municipios"], summary="Crear un municipio")
def create_municipio(municipio: schemas.MunicipioCreate, db: Session = Depends(get_db)):
    db_municipio = models.Municipio(nombre=municipio.nombre, isla_id=municipio.isla_id)
    db.add(db_municipio)
    db.commit()
    db.refresh(db_municipio)
    return db_municipio

@app.get("/municipios/", response_model=list[schemas.Municipio], tags=["Municipios"], summary="Listar todos los municipios")
def read_municipios(db: Session = Depends(get_db)):
    return db.query(models.Municipio).all()

@app.put("/municipios/{municipio_id}", response_model=schemas.Municipio, tags=["Municipios"], summary="Actualizar un municipio")
def update_municipio(municipio_id: int, municipio_actualizado: schemas.MunicipioCreate, db: Session = Depends(get_db)):
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id == municipio_id).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    db_municipio.nombre = municipio_actualizado.nombre
    db_municipio.isla_id = municipio_actualizado.isla_id
    db.commit()
    db.refresh(db_municipio)
    return db_municipio

@app.delete("/municipios/{municipio_id}", tags=["Municipios"], summary="Eliminar un municipio")
def delete_municipio(municipio_id: int, db: Session = Depends(get_db)):
    db_municipio = db.query(models.Municipio).filter(models.Municipio.id == municipio_id).first()
    if not db_municipio:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    db.delete(db_municipio)
    db.commit()
    return {"mensaje": f"Municipio {municipio_id} eliminado correctamente"}

# --- CRUD DE CATEGORÍAS ---

@app.post("/categorias/", response_model=schemas.Categoria, tags=["Categorías"], summary="Crear una categoría")
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = models.Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.get("/categorias/", response_model=list[schemas.Categoria], tags=["Categorías"], summary="Listar todas las categorías")
def read_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()

@app.put("/categorias/{categoria_id}", response_model=schemas.Categoria, tags=["Categorías"], summary="Actualizar una categoría")
def update_categoria(categoria_id: int, categoria_actualizada: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db_categoria.nombre = categoria_actualizada.nombre
    db_categoria.descripcion = categoria_actualizada.descripcion
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.delete("/categorias/{categoria_id}", tags=["Categorías"], summary="Eliminar una categoría")
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_categoria)
    db.commit()
    return {"mensaje": f"Categoría {categoria_id} eliminada correctamente"}

# --- CRUD DE ARTÍCULOS (HU-03) ---

@app.post("/articulos/", response_model=schemas.Articulo, tags=["Artículos"], summary="Publicar un artículo donado")
def create_articulo(articulo: schemas.ArticuloCreate, db: Session = Depends(get_db)):
    db_articulo = models.Articulo(
        titulo=articulo.titulo,
        descripcion=articulo.descripcion,
        categoria_id=articulo.categoria_id,
        municipio_id=articulo.municipio_id,
        estado="Disponible"
    )
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    return db_articulo

@app.get("/articulos/", response_model=list[schemas.Articulo], tags=["Artículos"], summary="Listar artículos")
def read_articulos(solo_disponibles: bool = False, db: Session = Depends(get_db)):
    query = db.query(models.Articulo)
    if solo_disponibles:
        query = query.filter(models.Articulo.estado == "Disponible")
    return query.all()

@app.put("/articulos/{articulo_id}", response_model=schemas.Articulo, tags=["Artículos"], summary="Actualizar un artículo")
def update_articulo(articulo_id: int, articulo_actualizado: schemas.ArticuloCreate, db: Session = Depends(get_db)):
    db_articulo = db.query(models.Articulo).filter(models.Articulo.id == articulo_id).first()
    if not db_articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    db_articulo.titulo = articulo_actualizado.titulo
    db_articulo.descripcion = articulo_actualizado.descripcion
    db_articulo.categoria_id = articulo_actualizado.categoria_id
    db_articulo.municipio_id = articulo_actualizado.municipio_id
    db.commit()
    db.refresh(db_articulo)
    return db_articulo

@app.delete("/articulos/{articulo_id}", tags=["Artículos"], summary="Eliminar un artículo")
def delete_articulo(articulo_id: int, db: Session = Depends(get_db)):
    db_articulo = db.query(models.Articulo).filter(models.Articulo.id == articulo_id).first()
    if not db_articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    db.delete(db_articulo)
    db.commit()
    return {"mensaje": f"Artículo {articulo_id} eliminado correctamente"}