from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Isla(Base):
    __tablename__ = "islas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    
    # Relación: Una isla tiene muchos municipios
    municipios = relationship("Municipio", back_populates="isla")

class Municipio(Base):
    __tablename__ = "municipios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    isla_id = Column(Integer, ForeignKey("islas.id"))
    
    # Relación: Un municipio pertenece a una isla
    isla = relationship("Isla", back_populates="municipios")

class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)

class Articulo(Base):
    __tablename__ = "articulos"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=False)
    estado = Column(String, default="Disponible", nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    municipio_id = Column(Integer, ForeignKey("municipios.id"), nullable=False)
    
    # Relaciones con tablas maestras
    categoria = relationship("Categoria")
    municipio = relationship("Municipio")