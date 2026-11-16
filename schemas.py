from pydantic import BaseModel

# Esquema base con los datos comunes
class IslaBase(BaseModel):
    nombre: str

# Esquema para crear una isla (hereda de IslaBase)
class IslaCreate(IslaBase):
    pass

# Esquema para devolver la isla desde la base de datos (incluye el ID)
class Isla(IslaBase):
    id: int

    class Config:
        from_attributes = True


# --- ESQUEMAS PARA CATEGORÍAS ---
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# --- ESQUEMAS PARA MUNICIPIOS ---
class MunicipioBase(BaseModel):
    nombre: str
    isla_id: int  # Aquí pedimos el ID de la isla a la que pertenece

class MunicipioCreate(MunicipioBase):
    pass

class Municipio(MunicipioBase):
    id: int

    class Config:
        from_attributes = True