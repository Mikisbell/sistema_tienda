# Importa Column, Integer y String de SQLAlchemy para definir las columnas de la tabla
from sqlalchemy import Column, Integer, String

# Importa Base desde app.db.base para heredar el modelo
from app.db.base import Base

# Define el modelo Cliente
class Cliente(Base):
    """
    Modelo que representa la tabla 'clientes' en la base de datos.
    """
    # Nombre de la tabla en la base de datos
    __tablename__ = "clientes"

    # Columna 'id': Clave primaria y autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Columna 'nombre': Nombre del cliente (no puede ser nulo)
    nombre = Column(String, nullable=False)

    # Columna 'email': Correo electrónico del cliente (único y no puede ser nulo)
    email = Column(String, unique=True, nullable=False)