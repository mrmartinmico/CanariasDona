from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Definimos la URL de la base de datos (un archivo local llamado canarias_dona.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./canarias_dona.db"

# 2. Creamos el "motor" que se conecta a la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos una fábrica de sesiones para hablar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creamos una clase base de la que heredarán nuestros futuros modelos (tablas)
Base = declarative_base()