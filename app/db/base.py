# app/db/base.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config.settings import settings

# Usar la URL de la base de datos desde las configuraciones
SQLALCHEMY_DATABASE_URL = settings.database_url

# Crear el motor de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
try:
    with engine.connect() as connection:
        print("✅ Conexión a la base de datos exitosa.")
except Exception as e:
    print(f"❌ Error al conectar con la base de datos: {e}")


# Clase base para los modelos
Base = declarative_base()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()