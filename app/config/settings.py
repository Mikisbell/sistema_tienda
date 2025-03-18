from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Settings(BaseSettings):
    database_url: str

    # Configuración para cargar las variables de entorno
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Crear una instancia de Settings
settings = Settings()