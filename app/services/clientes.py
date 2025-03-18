# Importa el modelo Cliente desde app.models.clientes
from app.models.clientes import Cliente

# Importa SessionLocal desde app.db.session para manejar la sesión de la base de datos
from app.db.session import SessionLocal

# Función para crear un nuevo cliente
def crear_cliente(nombre: str, email: str):
    """
    Crea un nuevo cliente en la base de datos.

    Parámetros:
    - nombre (str): Nombre del cliente.
    - email (str): Correo electrónico del cliente.

    Retorna:
    - El objeto Cliente creado.
    """
    # Crea una nueva sesión de base de datos
    db = SessionLocal()

    # Crea una instancia del modelo Cliente con los datos proporcionados
    cliente = Cliente(nombre=nombre, email=email)

    # Agrega el cliente a la sesión
    db.add(cliente)

    # Guarda los cambios en la base de datos
    db.commit()

    # Actualiza la instancia del cliente con los datos generados por la base de datos (por ejemplo, el ID)
    db.refresh(cliente)

    # Cierra la sesión de la base de datos
    db.close()

    # Retorna el cliente creado
    return cliente